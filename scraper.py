#!/usr/bin/env python3
"""
Reddit Monitor Agent for Spend Slow
Monitors subreddits for impulse buying and shopping addiction posts
Scores posts and drafts responses using GPT-4
"""

import os
import json
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
from openai import OpenAI

# Configuration
SUBREDDITS = [
    'nobuy',
    'shoppingaddiction',
    'debtfree',
    'personalfinance',
    'frugal',
    'minimalism'
]

# Keywords to filter for in broader subreddits
FILTER_KEYWORDS = [
    'impulse buy', 'impulse purchase', 'impulse spending',
    'can\'t stop spending', 'can\'t stop buying',
    'shopping addiction', 'compulsive buying',
    'can\'t save money', 'unable to save',
    'buying things i don\'t need',
    'overspending', 'overspent',
    'retail therapy',
    'shopping habit', 'spending habit',
    'buy too much', 'spent too much'
]

# High-value indicators for scoring
HIGH_VALUE_PHRASES = {
    'asking_for_help': [
        'what app', 'recommend an app', 'looking for app',
        'need help', 'please help', 'can someone help',
        'what should i do', 'how do i stop',
        'looking for tools', 'need accountability'
    ],
    'high_spending': [
        r'\$\d{3,}', r'\d{3,}\s*dollars', r'\d{3,}\s*bucks',
        'hundreds of dollars', 'thousands of dollars',
        'spent.*\$\d{3,}', 'spending.*\$\d{3,}'
    ],
    'starting_challenge': [
        'starting no buy', 'beginning no buy',
        'day 1', 'first day', 'just started',
        'trying to stop', 'committed to'
    ]
}

class RedditScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def scrape_subreddit(self, subreddit, time_filter='week', limit=50):
        """Scrape posts from a subreddit"""
        posts = []
        url = f'https://old.reddit.com/r/{subreddit}/new/.json?limit={limit}'
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Calculate post age
                created_utc = post_data['created_utc']
                post_age = datetime.now() - datetime.fromtimestamp(created_utc)
                
                # Filter by time
                if time_filter == 'day' and post_age > timedelta(days=1):
                    continue
                elif time_filter == 'week' and post_age > timedelta(weeks=1):
                    continue
                elif time_filter == 'month' and post_age > timedelta(days=30):
                    continue
                
                posts.append({
                    'id': post_data['id'],
                    'title': post_data['title'],
                    'selftext': post_data.get('selftext', ''),
                    'author': post_data['author'],
                    'subreddit': subreddit,
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'created_utc': created_utc,
                    'score': post_data['score'],
                    'num_comments': post_data['num_comments'],
                    'age_hours': post_age.total_seconds() / 3600
                })
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")
        
        return posts
    
    def should_include_post(self, post, subreddit):
        """Determine if post should be included based on keywords"""
        # Always include posts from primary subreddits
        if subreddit in ['nobuy', 'shoppingaddiction']:
            return True
        
        # For other subreddits, check if keywords match
        text = f"{post['title']} {post['selftext']}".lower()
        return any(keyword in text for keyword in FILTER_KEYWORDS)

class PostScorer:
    def __init__(self):
        pass
    
    def calculate_score(self, post):
        """Calculate score for a post (0-100)"""
        score = 0
        text = f"{post['title']} {post['selftext']}".lower()
        
        # 1. Intent to Change (30 points)
        asking_for_help = any(phrase in text for phrase in HIGH_VALUE_PHRASES['asking_for_help'])
        if asking_for_help:
            score += 30
        elif any(word in text for word in ['help', 'advice', 'tips', 'suggestions']):
            score += 20
        elif any(word in text for word in ['struggling', 'problem', 'issue', 'addiction']):
            score += 10
        
        # 2. Financial Impact (25 points)
        spending_amounts = re.findall(r'\$(\d+)', text)
        if spending_amounts:
            max_amount = max([int(x) for x in spending_amounts])
            if max_amount >= 500:
                score += 25
            elif max_amount >= 200:
                score += 15
            elif max_amount >= 100:
                score += 10
            else:
                score += 5
        elif any(phrase in text for phrase in ['debt', 'broke', 'can\'t afford', 'financial trouble']):
            score += 10
        
        # 3. Openness to Tools/Apps (20 points)
        if any(phrase in text for phrase in ['what app', 'recommend app', 'looking for app']):
            score += 20
        elif any(word in text for word in ['app', 'tool', 'software', 'tracker']):
            score += 15
        elif any(phrase in text for phrase in HIGH_VALUE_PHRASES['starting_challenge']):
            score += 10
        
        # 4. Recency & Engagement (15 points)
        if post['age_hours'] < 24:
            score += 15
        elif post['age_hours'] < 72:
            score += 10
        else:
            score += 5
        
        # Bonus for engagement
        if post['num_comments'] > 10:
            score += 5
        
        # 5. Pain Level (10 points)
        pain_indicators = [
            'hate myself', 'disgusted', 'ashamed', 'embarrassed',
            'destroying', 'ruining', 'can\'t stop', 'out of control',
            'relationship', 'marriage', 'divorce'
        ]
        if any(indicator in text for indicator in pain_indicators):
            score += 10
        elif any(word in text for word in ['guilt', 'shame', 'regret', 'anxiety']):
            score += 7
        else:
            score += 3
        
        return min(score, 100)  # Cap at 100
    
    def get_score_breakdown(self, post, score):
        """Get detailed breakdown of score"""
        text = f"{post['title']} {post['selftext']}".lower()
        breakdown = []
        
        # Check for high spender flag
        spending_amounts = re.findall(r'\$(\d+)', text)
        if spending_amounts:
            max_amount = max([int(x) for x in spending_amounts])
            if max_amount >= 500:
                breakdown.append(f"⚠️ HIGH SPENDER: Mentions ${max_amount}")
        
        # Check for app interest
        if any(phrase in text for phrase in ['what app', 'recommend app', 'looking for app']):
            breakdown.append("🎯 Asking for app recommendations")
        
        # Check for help seeking
        if any(phrase in text for phrase in HIGH_VALUE_PHRASES['asking_for_help']):
            breakdown.append("💬 Actively seeking help")
        
        # Recency
        if post['age_hours'] < 24:
            breakdown.append(f"🕐 Posted {int(post['age_hours'])} hours ago")
        
        return breakdown

class ResponseDrafter:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def draft_response(self, post, is_dm=False):
        """Draft a response using GPT-4"""
        
        post_text = f"Title: {post['title']}\n\nContent: {post['selftext']}"
        
        if is_dm:
            prompt = f"""You are reaching out to a Reddit user who is struggling with impulse buying or shopping addiction. 

THE POST:
{post_text}

YOUR TASK:
Write a warm, empathetic private message (DM) to this person. 

GUIDELINES:
- Be genuinely empathetic and understanding
- Acknowledge their specific struggle mentioned in their post
- Naturally mention Spend Slow as a tool that might help them
- Explain briefly: Spend Slow helps people add items they want to buy and set cooldown periods (1, 3, or 7 days) before purchasing
- Keep it conversational and authentic (NOT salesy)
- Mention there's a free option available
- Max 150 words

Write the DM:"""
        else:
            prompt = f"""You are commenting on a Reddit post from someone struggling with impulse buying or shopping addiction.

THE POST:
{post_text}

YOUR TASK:
Write an empathetic, helpful public comment.

GUIDELINES:
- Be supportive and understanding
- Reference their specific situation
- Share that you've built a tool called Spend Slow that helps with this exact problem
- Briefly explain: lets you add items and set cooldown periods (1, 3, or 7 days) to avoid impulse purchases
- Mention it has a free option
- Keep it natural and conversational (NOT an advertisement)
- Max 100 words
- End with offering to share more info if they're interested

Write the comment:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful, empathetic person who genuinely wants to help others struggling with shopping addiction. You are NOT a salesperson."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error drafting response: {e}")
            return "[Error generating response]"

def main():
    print("🚀 Starting Reddit Monitor Agent...")
    print(f"📅 Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    scraper = RedditScraper()
    scorer = PostScorer()
    
    # Get OpenAI API key
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    drafter = ResponseDrafter(openai_api_key)
    
    # Scrape all subreddits
    all_posts = []
    for subreddit in SUBREDDITS:
        print(f"📡 Scraping r/{subreddit}...")
        posts = scraper.scrape_subreddit(subreddit, time_filter='month', limit=100)
        
        # Filter posts
        filtered_posts = [p for p in posts if scraper.should_include_post(p, subreddit)]
        all_posts.extend(filtered_posts)
        print(f"   Found {len(filtered_posts)} relevant posts")
    
    print(f"\n📊 Total posts collected: {len(all_posts)}")
    
    # Score all posts
    print("\n🔢 Scoring posts...")
    scored_posts = []
    for post in all_posts:
        score = scorer.calculate_score(post)
        breakdown = scorer.get_score_breakdown(post, score)
        
        post['score_value'] = score
        post['score_breakdown'] = breakdown
        scored_posts.append(post)
    
    # Sort by score and get top 20
    scored_posts.sort(key=lambda x: x['score_value'], reverse=True)
    top_20 = scored_posts[:20]
    
    print(f"✅ Top 20 posts selected (scores: {top_20[0]['score_value']}-{top_20[-1]['score_value']})")
    
    # Draft responses for top 20
    print("\n✍️  Drafting responses with GPT-4...")
    results = []
    
    for i, post in enumerate(top_20, 1):
        print(f"   Drafting {i}/20...", end='\r')
        
        # Draft both public comment and DM
        public_response = drafter.draft_response(post, is_dm=False)
        dm_response = drafter.draft_response(post, is_dm=True)
        
        results.append({
            'rank': i,
            'score': post['score_value'],
            'post_id': post['id'],
            'title': post['title'],
            'content': post['selftext'][:500],  # Truncate long posts
            'author': post['author'],
            'subreddit': post['subreddit'],
            'url': post['url'],
            'created': datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d %H:%M'),
            'age_hours': int(post['age_hours']),
            'engagement': {
                'upvotes': post['score'],
                'comments': post['num_comments']
            },
            'score_breakdown': post['score_breakdown'],
            'responses': {
                'public_comment': public_response,
                'dm': dm_response
            }
        })
        
        time.sleep(1)  # Rate limit OpenAI calls
    
    print("\n✅ All responses drafted!")
    
    # Save results
    output = {
        'generated_at': datetime.now().isoformat(),
        'total_posts_scanned': len(all_posts),
        'top_opportunities': results
    }
    
    output_dir = '/home/claude/reddit-monitor-agent/data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = f'{output_dir}/report.json'
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Report saved to: {output_file}")
    print(f"\n🎉 Done! Check the dashboard to review opportunities.")
    
    # Print summary
    print("\n" + "="*60)
    print("📈 SUMMARY")
    print("="*60)
    print(f"Total posts scanned: {len(all_posts)}")
    print(f"Top 20 selected")
    print(f"Score range: {top_20[0]['score_value']} - {top_20[-1]['score_value']}")
    print(f"\nHighest scoring post:")
    print(f"  Score: {top_20[0]['score_value']}/100")
    print(f"  Subreddit: r/{top_20[0]['subreddit']}")
    print(f"  Title: {top_20[0]['title'][:60]}...")
    print("="*60)

if __name__ == '__main__':
    main()

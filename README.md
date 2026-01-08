# Spend Slow - Reddit Monitor Agent

🎯 **Automated Reddit monitoring system that finds potential customers and drafts personalized responses**

---

## 📋 What This Does

Every day at 8:00 AM, this system automatically:
1. ✅ Scrapes 6 subreddits (r/nobuy, r/shoppingaddiction, r/debtfree, r/personalfinance, r/frugal, r/minimalism)
2. ✅ Filters for posts about impulse buying and shopping addiction
3. ✅ Scores each post (0-100) based on conversion potential
4. ✅ Selects the top 20 opportunities
5. ✅ Uses GPT-4 to draft personalized responses (both public comments and DMs)
6. ✅ Updates your web dashboard with results

You just open the dashboard, review the opportunities, and copy/paste the responses to Reddit!

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `reddit-monitor-agent` (or anything you want)
3. Make it **Private** (to protect your API keys)
4. Click "Create repository"

### Step 2: Upload Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. On your new repository page, click "uploading an existing file"
2. Drag and drop ALL these files:
   - `scraper.py`
   - `requirements.txt`
   - `dashboard/index.html`
   - `.github/workflows/daily-scrape.yml`
3. Click "Commit changes"

**Option B: Using Git Command Line**

```bash
# In Terminal (Mac) or Command Prompt (Windows)
cd /path/to/downloaded/files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/reddit-monitor-agent.git
git push -u origin main
```

### Step 3: Add Your OpenAI API Key

1. In your GitHub repository, click "Settings"
2. Click "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Name: `OPENAI_API_KEY`
5. Value: [Paste your OpenAI API key]
6. Click "Add secret"

### Step 4: Enable GitHub Pages (for Dashboard)

1. In your repository, click "Settings"
2. Click "Pages" (left sidebar)
3. Under "Source", select "main" branch
4. Under "Folder", select "/dashboard"
5. Click "Save"
6. Wait 1-2 minutes, then you'll see: "Your site is live at https://YOUR_USERNAME.github.io/reddit-monitor-agent/"

### Step 5: Run It!

**Test it manually first:**

1. Go to "Actions" tab in your repository
2. Click "Daily Reddit Monitor"
3. Click "Run workflow" → "Run workflow"
4. Wait 3-5 minutes for it to complete
5. Visit your dashboard URL: `https://YOUR_USERNAME.github.io/reddit-monitor-agent/`

**If it worked, you'll see:**
- ✅ Top 20 ranked Reddit posts
- ✅ Score for each post
- ✅ Drafted responses ready to copy

---

## 🎯 How to Use the Dashboard

### Each Morning:

1. Open your dashboard URL
2. Review the top 20 opportunities
3. Click "View Details & Responses" on posts you want to engage with
4. Copy the drafted response (public comment or DM)
5. Click "View on Reddit" to open the post
6. Paste and send your response!

### What You'll See:

**Post Card Shows:**
- Rank (#1-20)
- Score (0-100)
- Post title and preview
- Subreddit, author, post age
- Why it's ranked high (e.g., "⚠️ HIGH SPENDER: Mentions $800")

**Responses:**
- **Public Comment**: Short, empathetic comment mentioning Spend Slow
- **DM**: Longer, more personal direct message

---

## ⚙️ Customization

### Change the Schedule

Edit `.github/workflows/daily-scrape.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # 8:00 AM UTC
```

Convert to your timezone:
- 8 AM EST = `0 13 * * *`
- 8 AM PST = `0 16 * * *`
- 8 AM GMT = `0 8 * * *`

### Add More Subreddits

Edit `scraper.py`, line 16:

```python
SUBREDDITS = [
    'nobuy',
    'shoppingaddiction',
    'debtfree',
    'personalfinance',
    'frugal',
    'minimalism',
    'budgetfood',  # Add your own!
]
```

### Adjust Scoring Weights

Edit `scraper.py`, `PostScorer.calculate_score()` method to change point values.

---

## 💰 Cost Breakdown

| Item | Cost |
|------|------|
| GitHub (hosting + automation) | **FREE** |
| OpenAI API (GPT-4) | ~$0.50-1.00/day |
| Reddit scraping | **FREE** |
| **Total per month** | **~$15-30** |

**Note**: You're already paying for OpenAI Pro, so the API calls are essentially free/included!

---

## 🔧 Troubleshooting

### "No data available" on dashboard
- Make sure the GitHub Action ran successfully (check "Actions" tab)
- Make sure `dashboard/data/report.json` exists in your repo
- Wait 1-2 minutes after the action completes

### GitHub Action fails
- Check you added `OPENAI_API_KEY` secret correctly
- Click on the failed action to see error logs
- Make sure you uploaded all files correctly

### Dashboard not loading
- Make sure GitHub Pages is enabled
- Check the URL is correct: `https://YOUR_USERNAME.github.io/reddit-monitor-agent/`
- Wait 1-2 minutes after enabling Pages

### OpenAI API errors
- Check your API key is valid
- Make sure you have credits/billing enabled on OpenAI
- Check the error message in GitHub Actions logs

---

## 🎓 Understanding the Scoring System

Posts are scored 0-100 based on:

1. **Intent to Change (30 points)**
   - Explicitly asking for help: 30 pts
   - Expressing desire to change: 20 pts
   - Just venting frustration: 10 pts

2. **Financial Impact (25 points)**
   - Spending $500+/month: 25 pts
   - Spending $200-500/month: 15 pts
   - Mentions debt but no amount: 10 pts

3. **Openness to Tools/Apps (20 points)**
   - Asking for app recommendations: 20 pts
   - Mentions using other apps: 15 pts
   - Open to trying new things: 10 pts

4. **Recency & Engagement (15 points)**
   - Posted within 24 hours: 15 pts
   - Posted within 3 days: 10 pts
   - Has lots of comments: +5 bonus

5. **Pain Level (10 points)**
   - Extreme distress: 10 pts
   - Moderate distress: 7 pts
   - Mild concern: 3 pts

**Special Flags:**
- ⚠️ HIGH SPENDER: Mentions $500+
- 🎯 Asking for apps
- 💬 Seeking help

---

## 📊 Next Steps

### Week 1-2: Learn the System
- Review the dashboard daily
- See which posts convert best
- Refine your messaging

### Week 3-4: Optimize
- Adjust scoring weights based on what works
- Test different response styles
- Track which subreddits perform best

### Future: Scale to Full Agent
Once you're comfortable, we can upgrade to:
- ✅ Automatic posting (with your approval)
- ✅ Real-time monitoring (hourly instead of daily)
- ✅ Conversation tracking
- ✅ A/B testing different responses

---

## 🆘 Support

If you run into issues:
1. Check the GitHub Actions logs for errors
2. Review the troubleshooting section above
3. Make sure all files are uploaded correctly
4. Verify your API keys are set as secrets

---

## 📝 File Structure

```
reddit-monitor-agent/
├── scraper.py                    # Main Python script
├── requirements.txt              # Python dependencies
├── dashboard/
│   └── index.html               # React dashboard
├── .github/
│   └── workflows/
│       └── daily-scrape.yml     # GitHub Actions automation
├── data/
│   └── report.json              # Generated daily (auto-created)
└── README.md                    # This file
```

---

## 🎉 You're All Set!

Your Reddit monitor is now fully automated. Every morning at 8 AM, it will:
1. Scan Reddit for opportunities
2. Score and rank them
3. Draft personalized responses
4. Update your dashboard

Just check the dashboard daily and engage with the top opportunities!

**Dashboard URL**: `https://YOUR_USERNAME.github.io/reddit-monitor-agent/`

**Questions?** Re-read this guide or check the troubleshooting section.

Good luck growing Spend Slow! 🚀

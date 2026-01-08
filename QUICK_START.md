# 🚀 QUICK START CHECKLIST

Follow these steps in order:

## ✅ Step 1: Create GitHub Account (if needed)
- [ ] Go to https://github.com/signup
- [ ] Create free account

## ✅ Step 2: Create New Repository
- [ ] Go to https://github.com/new
- [ ] Name: `reddit-monitor-agent`
- [ ] Make it **Private**
- [ ] Click "Create repository"

## ✅ Step 3: Upload Files
- [ ] Click "uploading an existing file" on your new repo
- [ ] Drag ALL files from the `reddit-monitor-agent` folder
- [ ] Click "Commit changes"

## ✅ Step 4: Add OpenAI API Key
- [ ] In repo, click "Settings"
- [ ] Click "Secrets and variables" → "Actions"
- [ ] Click "New repository secret"
- [ ] Name: `OPENAI_API_KEY`
- [ ] Value: [Your OpenAI API key]
- [ ] Click "Add secret"

## ✅ Step 5: Enable GitHub Pages
- [ ] In repo, click "Settings" → "Pages"
- [ ] Source: "main" branch
- [ ] Folder: "/dashboard"
- [ ] Click "Save"
- [ ] Copy your site URL (shown after save)

## ✅ Step 6: Test Run
- [ ] Go to "Actions" tab
- [ ] Click "Daily Reddit Monitor"
- [ ] Click "Run workflow" button (top right)
- [ ] Click green "Run workflow" button
- [ ] Wait 3-5 minutes

## ✅ Step 7: Check Dashboard
- [ ] Open your GitHub Pages URL
- [ ] Should see: https://YOUR_USERNAME.github.io/reddit-monitor-agent/
- [ ] You should see top 20 Reddit posts!

---

## 🎯 Your Dashboard URL

After setup, save this URL:

```
https://YOUR_USERNAME.github.io/reddit-monitor-agent/
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## ⏰ Automatic Schedule

Once set up, the system runs automatically at **8:00 AM UTC** every day.

To change the time, edit `.github/workflows/daily-scrape.yml`

---

## 💡 Using the Dashboard

1. Open your dashboard URL each morning
2. Review top 20 posts (sorted by score)
3. Click "View Details & Responses" on interesting posts
4. Copy the drafted response
5. Click "View on Reddit"
6. Paste and send!

---

## ❓ Problems?

- Dashboard shows "No data" → Wait 1-2 minutes after first run
- Action failed → Check you added the `OPENAI_API_KEY` secret
- Can't find dashboard → Make sure GitHub Pages is enabled in Settings

---

**Total setup time: 10-15 minutes**

**Daily time commitment: 15-30 minutes** (reviewing dashboard and sending responses)

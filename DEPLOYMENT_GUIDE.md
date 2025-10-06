# 🚀 Deployment Guide - AI Multi-Agent Coding Assistant

This guide will help you deploy your AI Multi-Agent Coding Assistant to GitHub and various cloud platforms.

---

## 📋 Table of Contents

1. [Push to GitHub](#push-to-github)
2. [Deploy to Streamlit Cloud](#deploy-to-streamlit-cloud)
3. [Deploy to Heroku](#deploy-to-heroku)
4. [Deploy to Railway](#deploy-to-railway)
5. [Deploy to Render](#deploy-to-render)

---

## 🐙 Push to GitHub

### Step 1: Initialize Git Repository

Open your terminal in the project directory and run:

```bash
cd c:\multiagent
git init
```

### Step 2: Add All Files

```bash
git add .
```

### Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: AI Multi-Agent Coding Assistant with professional blue UI"
```

### Step 4: Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git
```

### Step 5: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

### ✅ Done! Your code is now on GitHub!

Visit: `https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant`

---

## ☁️ Deploy to Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is the easiest and fastest way to deploy your chatbot!

### Prerequisites
- GitHub account
- Repository pushed to GitHub
- Google Gemini API key

### Step-by-Step Instructions

1. **Go to Streamlit Cloud**
   - Visit: [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in with GitHub"

2. **Create New App**
   - Click "New app" button
   - Select your repository: `AI-multi-agent-coding-assistant`
   - Branch: `main`
   - Main file path: `chatbot_ui.py`

3. **Configure Secrets**
   - Click "Advanced settings"
   - In the "Secrets" section, add:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

### 🎉 Your chatbot is now live and accessible worldwide!

---

## 🟣 Deploy to Heroku

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository

### Step 1: Create Procfile

Create a file named `Procfile` (no extension) in your project root:

```
web: streamlit run chatbot_ui.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2: Create runtime.txt

Create `runtime.txt` to specify Python version:

```
python-3.12.0
```

### Step 3: Login to Heroku

```bash
heroku login
```

### Step 4: Create Heroku App

```bash
heroku create your-ai-coding-assistant
```

### Step 5: Set Environment Variables

```bash
heroku config:set GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 6: Deploy

```bash
git push heroku main
```

### Step 7: Open Your App

```bash
heroku open
```

---

## 🚂 Deploy to Railway

Railway offers easy deployment with GitHub integration.

### Step 1: Sign Up
- Go to [railway.app](https://railway.app)
- Sign in with GitHub

### Step 2: Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose `AI-multi-agent-coding-assistant`

### Step 3: Configure
- Railway will auto-detect it's a Python app
- Add environment variable:
  - Key: `GOOGLE_API_KEY`
  - Value: `your_actual_api_key_here`

### Step 4: Set Start Command
- Go to Settings → Deploy
- Custom Start Command: `streamlit run chatbot_ui.py --server.port=$PORT --server.address=0.0.0.0`

### Step 5: Deploy
- Click "Deploy"
- Your app will be live in minutes!

---

## 🎨 Deploy to Render

Render provides free hosting for web services.

### Step 1: Sign Up
- Go to [render.com](https://render.com)
- Sign in with GitHub

### Step 2: Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository

### Step 3: Configure Service
- **Name**: `ai-coding-assistant`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run chatbot_ui.py --server.port=$PORT --server.address=0.0.0.0`

### Step 4: Add Environment Variables
- Click "Environment"
- Add variable:
  - Key: `GOOGLE_API_KEY`
  - Value: `your_actual_api_key_here`

### Step 5: Deploy
- Click "Create Web Service"
- Wait for deployment to complete

---

## 🔒 Security Best Practices

### Never Commit Your API Key!

✅ **DO:**
- Use `.env` file locally (already in `.gitignore`)
- Use environment variables on cloud platforms
- Use secrets management in Streamlit Cloud

❌ **DON'T:**
- Commit `.env` file to GitHub
- Hardcode API keys in your code
- Share your API key publicly

### Verify .gitignore

Make sure your `.gitignore` includes:
```
.env
.env.local
*.env
```

---

## 🧪 Testing Your Deployment

After deployment, test these features:

1. ✅ App loads without errors
2. ✅ API key is configured (check sidebar)
3. ✅ Can send a message
4. ✅ Agents respond correctly
5. ✅ UI looks professional (blue theme)
6. ✅ Code blocks are hidden
7. ✅ API key is secured (shows dots)

---

## 🐛 Troubleshooting Deployment

### Streamlit Cloud Issues

**Problem**: App won't start
- **Solution**: Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Check Python version compatibility

**Problem**: API key not working
- **Solution**: Verify secrets are formatted correctly in TOML format
- No quotes around the key in secrets

### Heroku Issues

**Problem**: Application error
- **Solution**: Check logs with `heroku logs --tail`
- Verify Procfile is correct
- Check PORT environment variable is used

### General Issues

**Problem**: Import errors
- **Solution**: Make sure `requirements.txt` is complete
- Run `pip freeze > requirements.txt` locally

**Problem**: Slow performance
- **Solution**: Free tiers have limited resources
- Consider upgrading to paid tier for better performance

---

## 📊 Monitoring Your Deployment

### Streamlit Cloud
- View logs in the dashboard
- Monitor app health
- Check usage statistics

### Heroku
```bash
heroku logs --tail
heroku ps
```

### Railway
- View logs in the dashboard
- Monitor resource usage

### Render
- View logs in the service dashboard
- Check deployment status

---

## 🔄 Updating Your Deployment

### For All Platforms

1. **Make changes locally**
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
3. **Push to GitHub**:
   ```bash
   git push origin main
   ```

### Auto-Deploy
- **Streamlit Cloud**: Auto-deploys on push to main
- **Railway**: Auto-deploys on push
- **Render**: Auto-deploys on push
- **Heroku**: May need manual deploy or enable auto-deploy

---

## 💰 Cost Comparison

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Streamlit Cloud** | ✅ Yes | Easy, Python-focused | Limited resources |
| **Heroku** | ✅ Yes (limited) | Reliable, popular | Sleeps after 30 min |
| **Railway** | ✅ $5 credit | Modern, fast | Credit runs out |
| **Render** | ✅ Yes | Good free tier | Can be slow |

### Recommendation
🌟 **Start with Streamlit Cloud** - It's specifically designed for Streamlit apps and offers the best experience!

---

## 🎓 Next Steps

After deployment:

1. ✅ Share your app URL with others
2. ✅ Add custom domain (paid plans)
3. ✅ Monitor usage and performance
4. ✅ Collect user feedback
5. ✅ Iterate and improve

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

---

## 🎉 Congratulations!

Your AI Multi-Agent Coding Assistant is now deployed and accessible to the world! 🚀

**Need help?** Check the main README.md or create an issue on GitHub.

---

**Made with ❤️ using Streamlit, AutoGen, and Google Gemini**
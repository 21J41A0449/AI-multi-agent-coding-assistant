# 🖥️ Push to GitHub Using GitHub Desktop

## Step 1: Install GitHub Desktop

1. Download from: https://desktop.github.com/
2. Install and sign in with your GitHub account

## Step 2: Add Your Project

1. Open GitHub Desktop
2. Click **File** → **Add Local Repository**
3. Click **Choose...** and select: `c:\multiagent`
4. Click **Add Repository**

## Step 3: Create Repository on GitHub Desktop

If it says "This directory does not appear to be a Git repository":

1. Click **Create a repository**
2. Name: `AI-multi-agent-coding-assistant`
3. Description: `AI Multi-Agent Coding Assistant powered by Google Gemini`
4. Keep "Initialize this repository with a README" **UNCHECKED**
5. Git Ignore: None (we already have .gitignore)
6. License: None
7. Click **Create Repository**

## Step 4: Make Initial Commit

1. You'll see all your files listed in the left panel
2. In the bottom left, enter commit message:
   ```
   Initial commit: AI Multi-Agent Coding Assistant
   ```
3. Click **Commit to main**

## Step 5: Publish to GitHub

1. Click **Publish repository** button at the top
2. Repository name: `AI-multi-agent-coding-assistant`
3. Description: `AI Multi-Agent Coding Assistant powered by Google Gemini`
4. **UNCHECK** "Keep this code private" (if you want it public)
5. Click **Publish Repository**

## ✅ Done!

Your project is now on GitHub at:
```
https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant
```

## Next Steps: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select repository: `AI-multi-agent-coding-assistant`
5. Main file: `chatbot_ui.py`
6. Click **Advanced settings**
7. Add secret:
   ```
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
8. Click **Deploy!**

Your app will be live in 2-3 minutes! 🎉

---

## Future Updates

When you make changes to your code:

1. Open GitHub Desktop
2. It will show changed files
3. Enter a commit message describing your changes
4. Click **Commit to main**
5. Click **Push origin** button at the top

That's it! Your changes are now on GitHub and will auto-deploy to Streamlit Cloud.
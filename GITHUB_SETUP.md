# 🐙 GitHub Setup Guide

Follow these steps to push your AI Multi-Agent Coding Assistant to GitHub.

---

## 📋 Prerequisites

- ✅ Git installed on your computer ([Download Git](https://git-scm.com/downloads))
- ✅ GitHub account ([Sign up](https://github.com/signup))
- ✅ Repository created on GitHub: `AI-multi-agent-coding-assistant`

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Open Terminal/PowerShell

Navigate to your project directory:

```bash
cd c:\multiagent
```

### Step 2: Initialize Git Repository

```bash
git init
```

**Expected output:**
```
Initialized empty Git repository in c:/multiagent/.git/
```

### Step 3: Configure Git (First Time Only)

If you haven't configured Git before:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Add All Files

```bash
git add .
```

This stages all files for commit (except those in `.gitignore`).

### Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: AI Multi-Agent Coding Assistant with professional blue UI"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: AI Multi-Agent Coding Assistant
 XX files changed, XXXX insertions(+)
```

### Step 6: Add Remote Repository

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git
```

### Step 7: Verify Remote

```bash
git remote -v
```

**Expected output:**
```
origin  https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git (fetch)
origin  https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git (push)
```

### Step 8: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

**You may be prompted to:**
- Enter GitHub username
- Enter GitHub password (or personal access token)

### ✅ Done! Your code is now on GitHub!

Visit your repository:
```
https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant
```

---

## 🔐 Authentication Options

### Option 1: HTTPS with Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy the token
5. Use token as password when pushing

### Option 2: SSH Key

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. Add SSH key to GitHub:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - GitHub → Settings → SSH and GPG keys → New SSH key

3. Change remote to SSH:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/AI-multi-agent-coding-assistant.git
   ```

---

## 🔄 Making Updates

After making changes to your code:

### Quick Update

```bash
git add .
git commit -m "Description of your changes"
git push
```

### Or Use the Batch File (Windows)

Double-click: `push_to_github.bat`

---

## 📁 What Gets Pushed?

### ✅ Included Files:
- `chatbot_ui.py` - Main chatbot interface
- `multi_agent_coder.py` - CLI version
- `requirements.txt` - Dependencies
- `.env.example` - Environment template
- `.gitignore` - Git ignore rules
- `README.md` - Documentation
- All markdown documentation files
- `run_chatbot.bat` - Launcher script
- `Procfile` - Heroku configuration
- `runtime.txt` - Python version

### ❌ Excluded Files (in .gitignore):
- `.env` - Your API key (NEVER commit this!)
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.vscode/` - IDE settings
- `*.log` - Log files

---

## 🐛 Troubleshooting

### Problem: "git: command not found"

**Solution:** Install Git from [git-scm.com](https://git-scm.com/downloads)

### Problem: "remote origin already exists"

**Solution:** Remove and re-add:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git
```

### Problem: "failed to push some refs"

**Solution:** Pull first, then push:
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Problem: Authentication failed

**Solution:** Use Personal Access Token instead of password:
1. Generate token on GitHub
2. Use token as password when prompted

### Problem: "src refspec main does not match any"

**Solution:** Make sure you've committed something:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## 📊 Verify Your Push

After pushing, check on GitHub:

1. ✅ All files are visible
2. ✅ `.env` is NOT visible (good!)
3. ✅ README.md displays correctly
4. ✅ File count matches your local files (minus ignored files)

---

## 🎯 Next Steps

After pushing to GitHub:

1. ✅ Add a nice README banner/logo
2. ✅ Add topics/tags to your repository
3. ✅ Enable GitHub Pages (optional)
4. ✅ Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)
5. ✅ Share your repository!

---

## 📚 Useful Git Commands

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### Undo Last Commit (keep changes)
```bash
git reset --soft HEAD~1
```

### Discard Local Changes
```bash
git checkout -- .
```

### Create New Branch
```bash
git checkout -b feature-name
```

### Switch Branch
```bash
git checkout main
```

---

## 🔒 Security Checklist

Before pushing, verify:

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] `.gitignore` is properly configured
- [ ] Sensitive data is excluded

### Double-Check .env is Ignored

```bash
git status
```

If you see `.env` in the list, it's NOT ignored! Fix immediately:

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 🎉 Success!

Your AI Multi-Agent Coding Assistant is now on GitHub! 🚀

**Repository URL:**
```
https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant
```

**Next:** Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)

---

## 💡 Pro Tips

1. **Commit Often** - Small, frequent commits are better than large ones
2. **Write Good Commit Messages** - Describe what changed and why
3. **Use Branches** - Create branches for new features
4. **Pull Before Push** - Always pull latest changes before pushing
5. **Review Changes** - Use `git diff` to review before committing

---

## 📞 Need Help?

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Made with ❤️ for the AI Multi-Agent Coding Assistant**
# 🚀 Quick Start Guide - AI Multi-Agent Chatbot

## ✨ What You Have

A beautiful web-based chatbot interface where three AI agents collaborate to write code for you:
- 🔍 **Researcher** - Plans the solution
- 💻 **Coder** - Writes the code  
- ✅ **Tester** - Reviews and validates

## 🎯 How to Run

### Option 1: Double-click the batch file
```
run_chatbot.bat
```

### Option 2: Run from PowerShell
```powershell
python -m streamlit run c:\multiagent\chatbot_ui.py
```

### Option 3: Run from Command Prompt
```cmd
python -m streamlit run c:\multiagent\chatbot_ui.py
```

## 🌐 Access the Chatbot

After running, your browser will automatically open to:
```
http://localhost:8501
```

If it doesn't open automatically, just copy that URL into your browser.

## 💬 How to Use

1. **Type your request** in the chat input at the bottom
2. **Press Enter** or click the send button
3. **Watch the agents collaborate** in real-time
4. **Copy the code** from the chat when ready

## 📝 Example Prompts

Try these to get started:

```
Create a simple calculator in Python
```

```
Build a todo list app with Flask
```

```
Write a password generator with GUI
```

```
Make a web scraper for news articles
```

```
Create a Rock Paper Scissors game
```

## ⚙️ Settings (Sidebar)

- **API Key**: Your Google Gemini API key (already loaded from .env)
- **Active Agents**: See which agents are working
- **Clear Chat**: Start a fresh conversation

## 🛑 How to Stop

Press `Ctrl+C` in the terminal/PowerShell window where Streamlit is running.

## 🎨 Features

✅ Beautiful chat interface  
✅ Real-time agent collaboration  
✅ Syntax-highlighted code  
✅ Chat history  
✅ Easy to use  
✅ Powered by Google Gemini 2.5 Flash  

## 🐛 Troubleshooting

**Port already in use?**
```powershell
python -m streamlit run c:\multiagent\chatbot_ui.py --server.port 8502
```
Then open: http://localhost:8502

**Can't see the agents talking?**
- Make sure you have a valid Google API key
- Check your internet connection
- Look for error messages in the chat

**Streamlit not found?**
```powershell
python -m pip install --user streamlit
```

## 📚 More Info

See `README_CHATBOT.md` for detailed documentation.

---

**Enjoy your AI coding assistant!** 🤖✨
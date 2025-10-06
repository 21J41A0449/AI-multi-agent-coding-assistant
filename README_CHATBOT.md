# 🤖 AI Multi-Agent Coding Assistant - Chatbot Interface

A beautiful web-based chatbot interface for your multi-agent coding system powered by Google Gemini.

## 🚀 Quick Start

### 1. Run the Chatbot Interface

```powershell
streamlit run c:\multiagent\chatbot_ui.py
```

### 2. Open in Browser

The app will automatically open in your default browser at `http://localhost:8501`

### 3. Start Chatting!

Type your coding request in the chat input and watch the three AI agents collaborate:
- 🔍 **Researcher** - Analyzes and plans
- 💻 **Coder** - Writes the code
- ✅ **Tester** - Reviews and validates

## 📋 Features

✅ **Beautiful Web Interface** - Modern, responsive chat UI  
✅ **Real-time Agent Collaboration** - See each agent's contribution  
✅ **Syntax Highlighting** - Code is displayed with proper formatting  
✅ **Chat History** - Keep track of all your conversations  
✅ **Easy API Key Management** - Enter your key in the sidebar  
✅ **Clear Chat** - Start fresh anytime  

## 💡 Example Prompts

Try asking:
- "Create a calculator app in Python"
- "Build a todo list with Flask"
- "Write a web scraper for news articles"
- "Make a Rock Paper Scissors game"
- "Create a password generator"
- "Build a simple chatbot"

## 🔧 Configuration

Your Google API key is automatically loaded from the `.env` file. You can also:
- Enter it manually in the sidebar
- Change it anytime without restarting

## 📁 Files

- `chatbot_ui.py` - Main Streamlit chatbot interface
- `multi_agent_coder.py` - Original command-line version
- `.env` - Your API key configuration

## 🎨 Interface Features

### Sidebar
- API key input (with password masking)
- Active agents information
- Clear chat history button
- System information

### Main Chat Area
- User messages (👤)
- Researcher messages (🔍)
- Coder messages (💻)
- Tester messages (✅)
- Loading spinner during processing
- Success/error notifications

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal to stop the Streamlit server.

## 🐛 Troubleshooting

**Port already in use?**
```powershell
streamlit run c:\multiagent\chatbot_ui.py --server.port 8502
```

**API key not working?**
- Check that your `.env` file has no quotes around the key
- Try entering the key manually in the sidebar

**Agents not responding?**
- Verify your internet connection
- Check that your Google API key is valid
- Look at the error message for details

## 🎯 Tips

1. **Be Specific** - The more detailed your request, the better the results
2. **Watch the Agents** - Learn from how they break down and solve problems
3. **Save Your Code** - Copy the generated code from the chat
4. **Iterate** - Ask follow-up questions to refine the solution

Enjoy your AI coding assistant! 🚀
# 🤖 AI Multi-Agent Coding Assistant

A powerful multi-agent system powered by Google Gemini that collaborates to write code for you!

## ✨ What's New - FIXED!

✅ **ModelInfo Error Resolved** - The "Missing required field 'family'" error has been fixed!  
✅ **Web Chatbot Interface** - Beautiful Streamlit-based chat UI  
✅ **Pure Gemini Integration** - Uses only Google Gemini (no OpenAI needed)  
✅ **Three Specialized Agents** - Researcher, Coder, and Tester working together  

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-multi-agent-coding-assistant.git
cd AI-multi-agent-coding-assistant
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up API Key
1. Copy `.env.example` to `.env`
2. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Add your key to `.env`:
```env
GOOGLE_API_KEY=your_api_key_here
```

### 4️⃣ Start the Web Chatbot

**Option A: Double-click the batch file (Windows)**
```
run_chatbot.bat
```

**Option B: Run from command line**
```bash
streamlit run chatbot_ui.py
```

### 5️⃣ Access in Browser

The chatbot will automatically open at: **http://localhost:8501**

### 6️⃣ Start Chatting!

Type your coding request and watch the agents collaborate in real-time!

---

## 📁 Project Structure

```
AI-multi-agent-coding-assistant/
│
├── 🌟 START_HERE.txt          # Quick start instructions
├── 🚀 run_chatbot.bat         # One-click launcher (Windows)
│
├── 💬 chatbot_ui.py           # Web chatbot interface (Streamlit)
├── 🖥️  multi_agent_coder.py   # Command-line version
│
├── 🔧 .env.example            # Environment variables template
├── 📦 requirements.txt        # Python dependencies
├── 🚫 .gitignore              # Git ignore rules
│
├── 📚 README.md               # This file
├── 📖 README_CHATBOT.md       # Detailed chatbot docs
├── 🎯 QUICK_START.md          # Quick start guide
├── 🔧 FIX_SUMMARY.md          # Technical fix details
│
└── 🧪 test_*.py               # Test scripts
```

---

## 🤖 The Three Agents

### 🔍 Researcher
- Analyzes your coding request
- Breaks down the problem
- Creates a detailed plan
- Identifies requirements and challenges

### 💻 Coder
- Reviews the Researcher's plan
- Writes clean, efficient code
- Follows best practices
- Includes helpful comments

### ✅ Tester
- Reviews the Coder's work
- Checks for bugs and issues
- Validates requirements
- Approves or suggests improvements

---

## 💡 Example Prompts

Try these to see the agents in action:

```
Create a calculator app in Python
```

```
Build a Flask web app with a todo list
```

```
Write a password generator with a GUI
```

```
Make a Rock Paper Scissors game
```

```
Create a web scraper for news articles
```

```
Build a simple chatbot using Python
```

```
Write a file organizer script
```

---

## 🎨 Features

### Web Chatbot Interface
✅ Beautiful, modern chat UI  
✅ Real-time agent collaboration  
✅ Syntax-highlighted code blocks  
✅ Chat history  
✅ Easy API key management  
✅ Clear chat button  
✅ Responsive design  

### Multi-Agent System
✅ Three specialized AI agents  
✅ Round-robin collaboration  
✅ Automatic task completion  
✅ Powered by Google Gemini 2.5 Flash  
✅ No OpenAI API needed  

---

## ⚙️ Configuration

### API Key

Your Google Gemini API key is stored in `.env`:

```env
GOOGLE_API_KEY=your_key_here
```

**Important:** No quotes around the key!

### Model Configuration

Currently using: **gemini-2.5-flash**

To change the model, edit these files:
- `chatbot_ui.py` (line 155)
- `multi_agent_coder.py` (line 49)

---

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- Google Gemini API key

### Dependencies

Already installed:
```
autogen-agentchat
autogen-ext[gemini]
python-dotenv
streamlit
```

To reinstall if needed:
```powershell
pip install -r requirements.txt
```

---

## 🎯 Usage

### Web Chatbot (Recommended)

1. **Start the server:**
   ```bash
   streamlit run chatbot_ui.py
   ```

2. **Open browser:** http://localhost:8501

3. **Type your request** in the chat input

4. **Watch the agents collaborate** in real-time

5. **Copy the generated code** from the chat

### Command-Line Version

1. **Run the script:**
   ```bash
   python multi_agent_coder.py
   ```

2. **Enter your coding task** when prompted

3. **Watch the conversation** in the terminal

---

## 🛑 Stopping the Server

Press **Ctrl+C** in the terminal window where Streamlit is running.

---

## 🐛 Troubleshooting

### Port Already in Use?
```bash
streamlit run chatbot_ui.py --server.port 8502
```
Then open: http://localhost:8502

### API Key Not Working?
- Check that `.env` has no quotes around the key
- Verify the key is valid at: https://aistudio.google.com/apikey
- Try entering the key manually in the sidebar

### Agents Not Responding?
- Check your internet connection
- Verify your API key is valid
- Look for error messages in the chat or terminal

### Streamlit Not Found?
```bash
pip install streamlit
```

### Import Errors?
```bash
pip install autogen-agentchat autogen-ext[gemini] python-dotenv streamlit
```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub** (see instructions below)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `AI-multi-agent-coding-assistant`
6. Main file path: `chatbot_ui.py`
7. Add your `GOOGLE_API_KEY` in "Advanced settings" → "Secrets"
8. Click "Deploy"!

### Deploy to Other Platforms

- **Heroku**: Use `Procfile` with `web: streamlit run chatbot_ui.py`
- **Railway**: Connect GitHub repo and set start command
- **Render**: Deploy as web service with build command `pip install -r requirements.txt`

---

## 📊 System Requirements

- **OS:** Windows 11 (also works on Windows 10, macOS, Linux)
- **Python:** 3.12+ (tested on 3.12)
- **RAM:** 4GB minimum, 8GB recommended
- **Internet:** Required for Gemini API calls

---

## 🔧 Technical Details

### Architecture
- **Framework:** AutoGen 0.4.7+
- **Model:** Google Gemini 2.5 Flash
- **API:** Gemini OpenAI-compatible endpoint
- **UI:** Streamlit
- **Pattern:** Round-robin group chat

### Model Configuration
```python
ModelInfo(
    family="gemini-2.5-flash",
    vision=True,
    function_calling=True,
    json_output=True,
    structured_output=True
)
```

### Agent Flow
```
User Input → Researcher → Coder → Tester → Output
              ↓           ↓        ↓
           (Plan)     (Code)   (Review)
```

---

## 📚 Documentation

- **Quick Start:** `QUICK_START.md`
- **Chatbot Guide:** `README_CHATBOT.md`
- **Fix Details:** `FIX_SUMMARY.md`
- **Start Instructions:** `START_HERE.txt`

---

## 🎓 Tips for Best Results

1. **Be Specific** - The more details you provide, the better the code
2. **Watch the Process** - Learn from how the agents break down problems
3. **Iterate** - Ask follow-up questions to refine the solution
4. **Save Your Code** - Copy the generated code to your projects
5. **Experiment** - Try different types of coding tasks

---

## 🌟 What Makes This Special?

✨ **Pure Gemini** - No OpenAI API needed  
✨ **Multi-Agent Collaboration** - Three specialized agents working together  
✨ **Beautiful UI** - Modern web-based chat interface  
✨ **Real-Time Streaming** - See the agents think and collaborate  
✨ **Easy to Use** - Just type what you want and get code  
✨ **Fully Local** - Runs on your machine (API calls to Gemini only)  

---

## 📝 Version History

### v2.0 (Current) - January 6, 2025
- ✅ Fixed ModelInfo error (added required fields)
- ✅ Added Streamlit web chatbot interface
- ✅ Improved error handling
- ✅ Added comprehensive documentation
- ✅ Created one-click launcher

### v1.0 - Previous
- ✅ Initial multi-agent system
- ✅ Command-line interface
- ✅ Gemini integration

---

## 🤝 Support

If you encounter issues:

1. Check `FIX_SUMMARY.md` for common fixes
2. Review `QUICK_START.md` for setup help
3. Verify your API key is valid
4. Check your internet connection

---

## 📄 License

This project is for educational and personal use.

---

## 🎉 Enjoy Your AI Coding Assistant!

Start creating amazing code with your team of AI agents! 🚀

**Ready to begin?** → Open `START_HERE.txt` or run `run_chatbot.bat`

---

**Made with ❤️ using Google Gemini and AutoGen**
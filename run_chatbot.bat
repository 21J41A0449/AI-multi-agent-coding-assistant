@echo off
echo Starting AI Multi-Agent Coding Assistant...
echo.
echo The chatbot will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python -m streamlit run chatbot_ui.py
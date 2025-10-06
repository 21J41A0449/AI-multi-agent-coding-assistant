@echo off
echo ========================================
echo   GitHub Repository Initialization
echo   AI Multi-Agent Coding Assistant
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo This script will help you push your project to GitHub.
echo.
echo Prerequisites:
echo   1. Git is installed
echo   2. You have a GitHub account
echo   3. You created a repository named: AI-multi-agent-coding-assistant
echo.
pause

echo.
echo Step 1: Initializing Git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git initialization failed. Is Git installed?
    pause
    exit /b 1
)
echo SUCCESS!
echo.

echo Step 2: Configuring Git (if needed)...
echo.
set /p git_name="Enter your name (for Git commits): "
set /p git_email="Enter your email: "

git config user.name "%git_name%"
git config user.email "%git_email%"
echo Git configured!
echo.

echo Step 3: Adding files to Git...
git add .
echo Files added!
echo.

echo Step 4: Creating initial commit...
git commit -m "Initial commit: AI Multi-Agent Coding Assistant with professional blue UI"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)
echo Commit created!
echo.

echo Step 5: Setting up remote repository...
echo.
set /p github_username="Enter your GitHub username: "

git remote add origin https://github.com/%github_username%/AI-multi-agent-coding-assistant.git
echo Remote repository configured!
echo.

echo Step 6: Pushing to GitHub...
echo You may be prompted for your GitHub credentials.
echo.
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Project pushed to GitHub!
    echo ========================================
    echo.
    echo Your repository is now live at:
    echo https://github.com/%github_username%/AI-multi-agent-coding-assistant
    echo.
    echo Next steps:
    echo   1. Visit your repository on GitHub
    echo   2. Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)
    echo   3. Share your project!
) else (
    echo.
    echo ========================================
    echo   Push failed - Manual steps needed
    echo ========================================
    echo.
    echo Please check:
    echo   1. Repository exists on GitHub
    echo   2. You have internet connection
    echo   3. Your GitHub credentials are correct
    echo.
    echo Try pushing manually:
    echo   git push -u origin main
)

echo.
pause
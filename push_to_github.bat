@echo off
echo ========================================
echo   Pushing to GitHub
echo   AI Multi-Agent Coding Assistant
echo ========================================
echo.

cd /d "%~dp0"

set GIT="C:\Program Files\Git\bin\git.exe"

echo Step 1: Configuring Git (first time only)...
echo.
set /p USERNAME="Enter your GitHub username: "
set /p EMAIL="Enter your email: "

%GIT% config --global user.name "%USERNAME%"
%GIT% config --global user.email "%EMAIL%"

echo.
echo Step 2: Initializing Git repository...
%GIT% init
if errorlevel 1 (
    echo ERROR: Git initialization failed
    pause
    exit /b 1
)

echo.
echo Step 3: Adding all files...
%GIT% add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo.
echo Step 4: Creating initial commit...
%GIT% commit -m "Initial commit: AI Multi-Agent Coding Assistant"
if errorlevel 1 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)

echo.
echo Step 5: Adding remote repository...
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
%GIT% remote add origin https://github.com/%GITHUB_USERNAME%/AI-multi-agent-coding-assistant.git
if errorlevel 1 (
    echo Note: Remote might already exist, trying to continue...
)

echo.
echo Step 6: Pushing to GitHub...
echo You may be prompted for your GitHub credentials.
echo NOTE: Use a Personal Access Token instead of password!
echo.
%GIT% push -u origin main
if errorlevel 1 (
    echo.
    echo Trying 'master' branch instead...
    %GIT% branch -M main
    %GIT% push -u origin main
)

echo.
echo ========================================
echo   SUCCESS! Project pushed to GitHub
echo ========================================
echo.
echo Your repository: https://github.com/%GITHUB_USERNAME%/AI-multi-agent-coding-assistant
echo.
echo Next step: Deploy to Streamlit Cloud
echo Visit: https://share.streamlit.io
echo.
pause
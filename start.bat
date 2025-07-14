@echo off
cd /d "%~dp0"
echo Starting QuickCommand AI Assistant...
echo.

:: Check if .env file exists
if not exist .env (
    echo ⚠️  Configuration file (.env) not found!
    echo.
    echo To get started:
    echo 1. Copy .env.example to .env
    echo 2. Edit .env and add your OpenAI API key
    echo 3. Run this script again
    echo.
    echo For now, starting with fallback mode (no AI)...
    echo.
)

:: Start the application using py command
py quickcommand.py %*

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error starting QuickCommand. Please check:
    echo - Python is installed
    echo - Dependencies are installed (run setup.bat)  
    echo - Configuration is correct
    pause
)

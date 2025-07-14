@echo off
echo QuickCommand AI Assistant Setup
echo ===============================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Failed to install dependencies. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To get started:
echo 1. Copy .env.example to .env
echo 2. Add your OpenAI API key to the .env file
echo 3. Run: python quickcommand.py
echo.
pause

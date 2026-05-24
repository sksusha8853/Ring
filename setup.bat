@echo off
REM QR Contact App - Setup Script (Windows)

echo.
echo 🚀 QR Contact App - Setup Script (Windows)
echo ==========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python version: %PYTHON_VERSION%

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
cd backend
pip install -q -r requirements.txt
cd ..
echo ✓ Dependencies installed

REM Create .env file
echo.
echo Checking environment configuration...
if not exist .env (
    copy .env.example .env
    echo ✓ .env file created
    echo ⚠️  Please update .env with your settings
) else (
    echo ✓ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Make sure MongoDB is running
echo 2. Run: run.bat
echo    Or start manually:
echo    - Backend: cd backend ^& python main.py
echo    - Frontend: cd frontend ^& python -m http.server 8001
echo.
pause

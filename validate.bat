@echo off
REM QR Contact App - Validation Script (Windows)

echo.
echo 🔍 QR Contact App - Setup Validation
echo ====================================
echo.

set ERRORS=0
set WARNINGS=0

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    set /a ERRORS+=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python %%i
)

REM Check virtual environment
echo.
echo Checking virtual environment...
if not exist venv (
    echo ⚠️ Virtual environment not created (run setup.bat first)
    set /a WARNINGS+=1
) else (
    echo ✅ Virtual environment exists
)

REM Check backend files
echo.
echo Checking backend files...
if exist "backend\main.py" (echo ✅ backend\main.py) else (
    echo ❌ backend\main.py missing
    set /a ERRORS+=1
)
if exist "backend\config.py" (echo ✅ backend\config.py) else (
    echo ❌ backend\config.py missing
    set /a ERRORS+=1
)
if exist "backend\requirements.txt" (echo ✅ backend\requirements.txt) else (
    echo ❌ backend\requirements.txt missing
    set /a ERRORS+=1
)

REM Check frontend files
echo.
echo Checking frontend files...
if exist "frontend\index.html" (echo ✅ frontend\index.html) else (
    echo ❌ frontend\index.html missing
    set /a ERRORS+=1
)
if exist "frontend\style.css" (echo ✅ frontend\style.css) else (
    echo ❌ frontend\style.css missing
    set /a ERRORS+=1
)
if exist "frontend\script.js" (echo ✅ frontend\script.js) else (
    echo ❌ frontend\script.js missing
    set /a ERRORS+=1
)

REM Check .env
echo.
echo Checking environment configuration...
if exist ".env" (
    echo ✅ .env file exists
) else (
    echo ⚠️ .env file not found (copy from .env.example)
    set /a WARNINGS+=1
)

REM Summary
echo.
echo ====================================
if %ERRORS% equ 0 (
    if %WARNINGS% equ 0 (
        echo ✅ All checks passed! Ready to run.
        echo.
        echo Next steps:
        echo 1. Start MongoDB
        echo 2. Run: run.bat
        echo 3. Open: http://localhost:8001
    ) else (
        echo ⚠️ Setup complete with %WARNINGS% warnings
        echo You can still run, but check the warnings above.
    )
) else (
    echo ❌ Setup incomplete: %ERRORS% errors, %WARNINGS% warnings
    echo Please fix the errors above.
)

pause

@echo off
REM QR Contact App - Run Script (Windows)

echo.
echo 🚀 Starting QR Contact App...
echo =============================
echo.

REM Check if venv exists
if not exist venv (
    echo ❌ Virtual environment not found. Run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create logs directory
if not exist .logs mkdir .logs

echo Starting services...
echo 🔵 Backend: http://localhost:8000
echo 🟢 Frontend: http://localhost:8001
echo ------------------------------------
echo.

REM Start backend
cd backend
echo Starting backend...
start "QR Contact App - Backend" python main.py

REM Wait a moment
timeout /t 2 /nobreak

REM Start frontend
cd ..\frontend
echo Starting frontend...
start "QR Contact App - Frontend" python -m http.server 8001

cd ..

echo.
echo ✅ Services started!
echo.
echo Open your browser: http://localhost:8001
echo.
echo Close the command windows to stop services
pause

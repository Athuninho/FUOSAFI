@echo off
REM FUOSAFI One-Click Startup Script for Windows
echo ========================================================
echo  Launching FUOSAFI - Coastal Pollution Reporting System
echo ========================================================
echo.

if not exist "%~dp0venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at: %~dp0venv
    echo Please make sure the venv directory exists.
    pause
    exit /b 1
)

echo Starting Streamlit server...
"%~dp0venv\Scripts\python.exe" -m streamlit run "%~dp0app.py"
pause

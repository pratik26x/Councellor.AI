@echo off
title Counsellor.AI Server
echo ============================================
echo   Counsellor.AI - A Rising Education Initiative
echo ============================================
echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Download from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.
echo Starting server...
echo Open your browser at: http://127.0.0.1:5000
echo Press CTRL+C to stop the server.
echo.
cd /d "%~dp0backend"
python main.py
pause

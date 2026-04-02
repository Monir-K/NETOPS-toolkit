@echo off
title NetOps Toolkit — By M Kamjo
color 0A
echo.
echo  ====================================================
echo   NetOps Toolkit — Ping + Email Backend
echo   By M Kamjo
echo  ====================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found. Download from python.org
    pause & exit
)

echo  Starting server on http://localhost:5199 ...
echo.
echo  After server starts, double-click launch-edge.bat
echo  Browser opens in InPrivate/incognito mode.
echo.
echo  *** URL: http://localhost:5199 ***
echo.
echo  Keep this window open. Press Ctrl+C to stop.
echo  ====================================================
echo.

python "%~dp0ping_server.py"
pause

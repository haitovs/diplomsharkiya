@echo off
title Sharkiya Event Discovery - Launcher
color 0A

echo.
echo  ========================================
echo   🎟️  SHARKIYA EVENT DISCOVERY v2.0
echo  ========================================
echo.
echo  Starting applications...
echo.
echo  📱 User App:    http://localhost:8502
echo  🔧 Admin Panel: http://localhost:8503
echo.
echo  Admin Login: admin / admin123
echo.
echo  ========================================
echo  Press Ctrl+C to stop all applications
echo  ========================================
echo.

cd /d "%~dp0"

REM Start User App in a new window
start "User App - Local Events" cmd /k "streamlit run main.py --server.port 8502"

REM Wait 2 seconds before starting admin
timeout /t 2 /nobreak >nul

REM Start Admin Panel in a new window
start "Admin Panel - Local Events" cmd /k "streamlit run admin.py --server.port 8503"

REM Wait 3 seconds then open browser
timeout /t 3 /nobreak >nul

REM Open both apps in browser
start http://localhost:8502
start http://localhost:8503

echo.
echo  ✅ Both applications started!
echo.
echo  Close this window to keep apps running,
echo  or close the individual app windows to stop them.
echo.
pause

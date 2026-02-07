@echo off
REM ========================================
REM  Sharkiya Event Discovery - Simple Launcher
REM  Checks for Python and runs the app
REM ========================================

echo.
echo ========================================
echo   SHARKIYA EVENT DISCOVERY
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if required packages are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    echo This only needs to happen once.
    echo.
    pip install streamlit streamlit-folium folium pandas
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
    echo.
    echo Packages installed successfully!
    echo.
)

echo Starting application...
echo.
echo The app will open in your browser at:
echo   http://localhost:8502
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run main.py --server.port=8502 --browser.gatherUsageStats=false

pause

#!/bin/bash

# Sharkiya Event Discovery - Unified Launcher

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python 3
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python 3 is not installed or not in PATH."
    exit 1
fi

# Check Python version (simple check)
$PYTHON_CMD -c "import sys; exit(0) if sys.version_info >= (3, 8) else exit(1)"
if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3.8 or higher is required."
    exit 1
fi

echo "✅ Python environment found: $($PYTHON_CMD --version)"

# Check if requirements are installed (basic check for streamlit)
if ! $PYTHON_CMD -c "import streamlit" >/dev/null 2>&1; then
    echo "📦 Dependencies missing. Installing..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install dependencies."
        exit 1
    fi
    echo "✅ Dependencies installed."
else
    echo "✅ Dependencies already installed."
fi

# Run the application
echo "🚀 Starting Sharkiya Event Discovery..."
echo "📂 Working directory: $(pwd)/src"

# Navigate to src directory to run the app
cd src

# Run streamlit
# Run streamlit
$PYTHON_CMD -m streamlit run "0_🏠_Home.py" --server.port=8502 --browser.gatherUsageStats=false

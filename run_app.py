"""
PyInstaller entry point for Sharkiya Event Discovery
This wrapper launches the Streamlit app programmatically
"""

import os
import sys
from pathlib import Path
import subprocess

def main():
    """Launch the Streamlit application."""
    
    # Get the application directory
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = Path(sys._MEIPASS)
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    # Set working directory
    os.chdir(app_dir)
    
    # Get main.py path
    main_py = app_dir / "main.py"
    
    if not main_py.exists():
        print(f"Error: main.py not found at {main_py}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("=" * 50)
    print("  🎟️  SHARKIYA EVENT DISCOVERY")
    print("=" * 50)
    print()
    print("Starting application...")
    print("The app will open in your browser automatically.")
    print()
    print("📱 User App: http://localhost:8502")
    print()
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    print()
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(main_py),
            "--server.port=8502",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()

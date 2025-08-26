#!/usr/bin/env python3
"""
Deployment script for the SQL Query Enhancement Streamlit App
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def check_environment_variables():
    """Check if required environment variables are set."""
    required_vars = []
    optional_vars = [
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    print("🔍 Checking environment variables...")
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    if missing_required:
        print(f"❌ Missing required environment variables: {missing_required}")
        sys.exit(1)
    
    available_optional = [var for var in optional_vars if os.getenv(var)]
    if available_optional:
        print(f"✅ Found API keys: {available_optional}")
    else:
        print("⚠️  No API keys found. Some features may not work.")
    
    print("✅ Environment check completed")

def create_data_directory():
    """Create necessary data directories."""
    print("📁 Creating data directories...")
    directories = ["Data", "saved_json", "saved_plots", "temporary"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_streamlit_app(port=8501, host="localhost"):
    """Run the Streamlit app."""
    print(f"🚀 Starting Streamlit app on {host}:{port}")
    print("📱 Open your browser and navigate to the URL shown below")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(port),
            "--server.address", host,
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start Streamlit app: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Deploy SQL Query Enhancement Streamlit App")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the app on (default: 8501)")
    parser.add_argument("--host", default="localhost", help="Host to bind to (default: localhost)")
    parser.add_argument("--skip-install", action="store_true", help="Skip package installation")
    parser.add_argument("--skip-checks", action="store_true", help="Skip environment checks")
    
    args = parser.parse_args()
    
    print("🤖 SQL Query Enhancement App Deployment")
    print("=" * 50)
    
    if not args.skip_checks:
        check_python_version()
        check_environment_variables()
    
    if not args.skip_install:
        install_requirements()
    
    create_data_directory()
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    
    run_streamlit_app(args.port, args.host)

if __name__ == "__main__":
    main()

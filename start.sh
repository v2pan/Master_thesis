#!/bin/bash

# SQL Query Enhancement App Startup Script

echo "🤖 SQL Query Enhancement App"
echo "============================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version detected"

# Install requirements if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p Data saved_json saved_plots temporary

# Set default port
PORT=${1:-8501}

echo "🚀 Starting Streamlit app on port $PORT..."
echo "📱 Open your browser and go to: http://localhost:$PORT"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run the app
streamlit run app.py --server.port $PORT --server.address localhost


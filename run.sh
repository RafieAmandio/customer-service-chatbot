#!/bin/bash

# Activate virtual environment and run the chatbot server

echo "🚀 Starting Customer Service Chatbot Backend..."
echo "📦 Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

echo "🔧 Virtual environment activated: $(which python)"
echo "📋 Python version: $(python --version)"

# Start the server
echo "🌟 Starting FastAPI server..."
python main.py 
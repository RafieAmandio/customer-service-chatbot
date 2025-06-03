#!/bin/bash

# Setup script for Customer Service Chatbot Backend

echo "🔧 Setting up Customer Service Chatbot Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "OPENAI_MODEL=gpt-4" >> .env
    echo "EMBEDDING_MODEL=text-embedding-ada-002" >> .env
    echo "CHROMA_PERSIST_DIRECTORY=./chroma_db" >> .env
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: ./run.sh (to start the server)"
echo "3. Run: python sample_data.py (to add sample products)"
echo "4. Visit: http://localhost:8000/docs (for API documentation)" 
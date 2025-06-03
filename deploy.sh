#!/bin/bash

# Customer Service Chatbot - Deployment Script

set -e  # Exit on any error

echo "🚀 Customer Service Chatbot - Deployment Script"
echo "================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OpenAI API key not found in environment variables."
    read -p "Please enter your OpenAI API key: " OPENAI_API_KEY
    export OPENAI_API_KEY
fi

echo "📋 Environment Setup:"
echo "   OpenAI API Key: ${OPENAI_API_KEY:0:8}..."
echo "   API URL: http://localhost:8000"
echo ""

# Build and run with Docker Compose
echo "🔨 Building and starting the application..."
docker-compose up --build -d

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if the service is running
if curl -f http://localhost:8000/ &> /dev/null; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🌐 Available endpoints:"
    echo "   • API: http://localhost:8000"
    echo "   • Documentation: http://localhost:8000/docs"
    echo "   • Health check: http://localhost:8000/"
    echo ""
    echo "📖 To populate with sample data, run:"
    echo "   docker-compose exec chatbot-api python sample_data.py"
    echo ""
    echo "🔍 To view logs:"
    echo "   docker-compose logs -f chatbot-api"
    echo ""
    echo "🛑 To stop the application:"
    echo "   docker-compose down"
else
    echo "❌ Service failed to start. Checking logs..."
    docker-compose logs chatbot-api
    exit 1
fi 
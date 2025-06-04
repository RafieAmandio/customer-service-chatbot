#!/bin/bash

# Customer Service Chatbot - Production Deployment Script

set -e  # Exit on any error

echo "🚀 Customer Service Chatbot - Production Deployment"
echo "===================================================="

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

# Set deployment configuration
export AUTO_POPULATE_DATA=true
export OPENAI_MODEL=gpt-4
export EMBEDDING_MODEL=text-embedding-ada-002

echo "📋 Production Environment Setup:"
echo "   OpenAI API Key: ${OPENAI_API_KEY:0:8}..."
echo "   OpenAI Model: $OPENAI_MODEL"
echo "   Auto-populate Data: $AUTO_POPULATE_DATA"
echo "   API URL: http://localhost:8000"
echo ""

# Build and run with production Docker Compose
echo "🔨 Building and starting the production application..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 15

# Check if the service is running
if curl -f http://localhost:8000/ &> /dev/null; then
    echo "✅ Application is running successfully!"
    
    # Check if sample data was loaded
    sleep 5
    PRODUCT_COUNT=$(curl -s http://localhost:8000/products | python -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")
    echo "📦 Found $PRODUCT_COUNT products in the database"
    
    echo ""
    echo "🌐 Available endpoints:"
    echo "   • API: http://localhost:8000"
    echo "   • Documentation: http://localhost:8000/docs"
    echo "   • Health check: http://localhost:8000/"
    echo "   • Products: http://localhost:8000/products"
    echo "   • Statistics: http://localhost:8000/stats"
    echo ""
    echo "🔍 To view logs:"
    echo "   docker-compose -f docker-compose.prod.yml logs -f chatbot-api"
    echo ""
    echo "🛑 To stop the application:"
    echo "   docker-compose -f docker-compose.prod.yml down"
    echo ""
    echo "🔄 To manually populate data (if needed):"
    echo "   docker-compose -f docker-compose.prod.yml --profile init up data-init"
else
    echo "❌ Service failed to start. Checking logs..."
    docker-compose -f docker-compose.prod.yml logs chatbot-api
    exit 1
fi 
#!/bin/bash

# Initialize sample data for Customer Service Chatbot
# This script waits for the API to be ready and then populates sample data

echo "🔄 Waiting for API to be ready..."

# Wait for the API to be available
for i in {1..30}; do
    if curl -f http://localhost:8000/ &> /dev/null; then
        echo "✅ API is ready!"
        break
    fi
    echo "⏳ Waiting for API... (attempt $i/30)"
    sleep 2
done

# Check if API is still not ready
if ! curl -f http://localhost:8000/ &> /dev/null; then
    echo "❌ API is not responding after 60 seconds"
    exit 1
fi

# Check if data already exists
PRODUCT_COUNT=$(curl -s http://localhost:8000/products | python -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")

if [ "$PRODUCT_COUNT" -eq "0" ]; then
    echo "📚 No products found. Populating sample data..."
    python sample_data.py
    echo "✅ Sample data initialization complete!"
else
    echo "📊 Found $PRODUCT_COUNT existing products. Skipping data population."
fi 
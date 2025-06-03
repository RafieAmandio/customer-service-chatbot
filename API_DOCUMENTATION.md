# Customer Service Chatbot API Documentation

## Overview

A FastAPI-based backend service for an intelligent customer service chatbot that provides product recommendations and handles customer inquiries. The system uses OpenAI's GPT models for conversation and ChromaDB for vector-based product search.

**Base URL:** `http://localhost:8000`  
**API Version:** 1.0.0  
**Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive Swagger UI)

## Features

- 🤖 Intelligent conversation management with memory
- 🔍 Semantic product search using OpenAI embeddings
- 💡 AI-powered product recommendations
- 📦 Complete product catalog management
- 📊 Business context and company information
- 🎯 Confidence scoring for recommendations

---

## Authentication

Currently, no authentication is required. For production use, implement API key authentication or OAuth.

## Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

---

## API Endpoints

### Health Check

#### `GET /`
**Description:** Health check endpoint to verify API status.

**Response:**
```json
{
  "message": "Customer Service Chatbot API",
  "status": "running",
  "timestamp": "2024-01-20T10:30:00"
}
```

---

## Chat Endpoints

### Send Message to Chatbot

#### `POST /chat`
**Description:** Send a message to the chatbot and receive an intelligent response with optional product recommendations.

**Request Body:**
```json
{
  "message": "I need a laptop for business work under $1500",
  "conversation_id": "optional-conversation-id",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "response": "I'd recommend the Dell XPS 13 Plus for $1299.99. It's perfect for business professionals with its 12th Gen Intel Core i7 processor...",
  "conversation_id": "conv_123456789",
  "suggested_products": [
    {
      "id": "laptop-002",
      "name": "Dell XPS 13 Plus",
      "description": "Ultra-portable business laptop...",
      "category": "Laptops",
      "price": 1299.99,
      "features": ["12th Gen Intel Core i7", "16GB RAM"],
      "specifications": {...},
      "availability": true
    }
  ],
  "confidence_score": 0.95
}
```

### Get Chat History

#### `GET /chat/history/{conversation_id}`
**Description:** Retrieve conversation history for a specific conversation.

**Parameters:**
- `conversation_id` (path): The conversation identifier

**Response:**
```json
{
  "conversation_id": "conv_123456789",
  "messages": [
    {
      "role": "user",
      "content": "I need a laptop",
      "timestamp": "2024-01-20T10:30:00"
    },
    {
      "role": "assistant", 
      "content": "I'd be happy to help you find the perfect laptop...",
      "timestamp": "2024-01-20T10:30:05"
    }
  ]
}
```

### Clear Conversation

#### `DELETE /chat/{conversation_id}`
**Description:** Clear/delete a conversation and its history.

**Response:**
```json
{
  "message": "Conversation cleared successfully"
}
```

---

## Product Management Endpoints

### Add Product

#### `POST /products`
**Description:** Add a new product to the catalog.

**Request Body:**
```json
{
  "id": "laptop-007",
  "name": "Surface Laptop 5",
  "description": "Sleek and powerful laptop perfect for business professionals",
  "category": "Laptops",
  "price": 1399.99,
  "features": [
    "12th Gen Intel Core i7 processor",
    "13.5-inch PixelSense touchscreen"
  ],
  "specifications": {
    "processor": "Intel Core i7-1255U",
    "memory": "16GB LPDDR5x",
    "storage": "512GB SSD"
  },
  "availability": true
}
```

**Response:**
```json
{
  "message": "Product added successfully",
  "product_id": "laptop-007"
}
```

### Get All Products

#### `GET /products`
**Description:** Retrieve all products from the catalog.

**Response:**
```json
[
  {
    "id": "laptop-001",
    "name": "MacBook Pro 14-inch M3 Pro",
    "description": "Premium laptop designed for professionals...",
    "category": "Laptops",
    "price": 1999.99,
    "features": [...],
    "specifications": {...},
    "availability": true
  }
]
```

### Update Product

#### `PUT /products/{product_id}`
**Description:** Update an existing product.

**Parameters:**
- `product_id` (path): The product identifier

**Request Body:** Same as POST /products

### Delete Product

#### `DELETE /products/{product_id}`
**Description:** Delete a product from the catalog.

**Response:**
```json
{
  "message": "Product deleted successfully"
}
```

---

## Search and Recommendation Endpoints

### Search Products

#### `POST /products/search`
**Description:** Search for products using semantic search or category filtering.

**Request Body:**
```json
{
  "query": "lightweight laptop for travel",
  "category": "Laptops",
  "price_range": [1000, 2000],
  "limit": 5
}
```

**Response:**
```json
{
  "query": "lightweight laptop for travel",
  "results": [
    {
      "product": {...},
      "similarity_score": 0.89
    }
  ]
}
```

### Get Recommendations

#### `POST /recommendations`
**Description:** Get AI-powered product recommendations with reasoning.

**Parameters:**
- `query` (query): Search query
- `limit` (query): Number of recommendations (default: 5)

**Response:**
```json
{
  "products": [...],
  "reasoning": "Based on your need for business work, I recommend these laptops because...",
  "match_score": 0.92
}
```

### Get Categories

#### `GET /categories`
**Description:** Get all available product categories.

**Response:**
```json
{
  "categories": ["Laptops", "Smartphones", "Monitors", "Accessories"]
}
```

---

## Utility Endpoints

### Bulk Add Products

#### `POST /products/bulk`
**Description:** Add multiple products in a single request.

**Request Body:**
```json
[
  {product1},
  {product2},
  ...
]
```

### Get Statistics

#### `GET /stats`
**Description:** Get API and catalog statistics.

**Response:**
```json
{
  "total_products": 10,
  "available_products": 9,
  "categories": 4,
  "conversations_active": 5,
  "category_list": ["Laptops", "Smartphones", "Monitors", "Accessories"]
}
```

---

## Data Models

### Product
```json
{
  "id": "string",
  "name": "string", 
  "description": "string",
  "category": "string",
  "price": "number",
  "features": ["string"],
  "specifications": {"key": "value"},
  "availability": "boolean"
}
```

### ChatRequest
```json
{
  "message": "string",
  "conversation_id": "string (optional)",
  "user_id": "string (optional)"
}
```

### ChatResponse
```json
{
  "response": "string",
  "conversation_id": "string",
  "suggested_products": ["Product (optional)"],
  "confidence_score": "number (optional)"
}
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `404`: Not Found  
- `500`: Internal Server Error

**Error Response Format:**
```json
{
  "detail": "Error description"
}
```

---

## Example Use Cases

### 1. Customer Asking About Company
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your company"}'
```

### 2. Product Search with Budget
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a laptop under $1500"}'
```

### 3. Adding a New Product
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d @add_product_example.json
```

### 4. Searching Products
```bash
curl -X POST "http://localhost:8000/products/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "gaming laptop", "limit": 3}'
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

1. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

### Using Docker Directly

```bash
# Build the image
docker build -t chatbot-api .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  -v chatbot_data:/app/chroma_db \
  --name chatbot-api \
  chatbot-api
```

---

## Development Setup

1. **Clone and setup:**
```bash
git clone <repository>
cd be-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment configuration:**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. **Run the server:**
```bash
python main.py
# Or use: uvicorn main:app --reload
```

4. **Populate with sample data:**
```bash
python sample_data.py
```

## Testing

Run comprehensive tests:
```bash
python test_chatbot.py
```

---

## Rate Limits & Production Considerations

- Implement rate limiting for production use
- Add authentication/authorization
- Configure CORS appropriately for your frontend domain
- Monitor OpenAI API usage and costs
- Set up proper logging and monitoring
- Consider implementing caching for frequently accessed data
- Use environment-specific configurations

---

## Support

For issues and questions:
- Check the interactive documentation at `/docs`
- Review server logs for debugging
- Ensure OpenAI API key is valid and has sufficient credits 
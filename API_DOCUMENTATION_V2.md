# Multi-Brand Customer Service Chatbot API v2.0 Documentation

## Overview

A FastAPI-based backend service for multi-brand intelligent customer service chatbots with real-time WebSocket streaming, vector-based product recommendations, and comprehensive brand management. The system uses OpenAI's GPT models for conversation and ChromaDB for vector-based product search with complete data isolation per brand.

**Base URL:** `http://localhost:8000`  
**WebSocket URL:** `ws://localhost:8000`  
**API Version:** 2.0.0  
**Interactive Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

## 🆕 What's New in V2.0

### WebSocket Streaming Chat
- **Real-time streaming responses** from OpenAI with chunk-based delivery
- **Voice-optimized responses** for voice interfaces (1 sentence max)
- **Connection management** with automatic cleanup per brand
- **Live typing indicators** and progressive response building

### Multi-Brand System
- **Complete data isolation** with separate ChromaDB collections per brand
- **Custom system prompts** and welcome messages per brand
- **Brand-specific product catalogs** and conversation histories
- **Configurable appearance settings** and company information
- **Independent conversation management** and statistics

### Enhanced Features
- **Brand configuration management** with persistent storage
- **Brand-scoped API endpoints** for all operations
- **Bulk operations** and file uploads per brand
- **Comprehensive brand statistics** and monitoring
- **Backward compatibility** with v1.0 API (defaults to TechPro brand)

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

## 📡 WebSocket API

### Connection Endpoint
```
ws://localhost:8000/ws/chat/{brand_id}
```

### Connection Flow

1. **Connect** to the WebSocket endpoint with a specific brand ID
2. **Receive** a welcome message from the brand
3. **Send** chat messages and receive streaming responses
4. **Handle** chunks, final responses, and suggested products
5. **Disconnect** when conversation is complete

### Message Types

#### Client → Server Messages

**Chat Message:**
```json
{
  "type": "chat",
  "data": {
    "message": "I need a laptop for business work",
    "conversation_id": "optional-conversation-id",
    "user_id": "optional-user-id",
    "voice": false
  }
}
```

**Ping Message:**
```json
{
  "type": "ping",
  "data": {}
}
```

#### Server → Client Messages

**Welcome Message:**
```json
{
  "type": "welcome",
  "data": {
    "message": "Welcome to TechPro Solutions! How can I help you today?",
    "brand_id": "techpro",
    "brand_name": "TechPro Solutions"
  }
}
```

**Response Chunk:**
```json
{
  "type": "chunk",
  "data": {
    "content": "I'd be happy to help you find",
    "is_final": false,
    "conversation_id": "conv-123456789",
    "suggested_products": null,
    "confidence_score": null
  }
}
```

**Complete Response:**
```json
{
  "type": "complete",
  "data": {
    "content": "",
    "is_final": true,
    "conversation_id": "conv-123456789",
    "suggested_products": [
      {
        "id": "laptop-002",
        "name": "Dell XPS 13 Plus",
        "description": "Ultra-portable business laptop...",
        "category": "Laptop",
        "price": 19999000.00,
        "features": ["Intel Core i7", "16GB RAM"],
        "specifications": {...},
        "availability": true
      }
    ],
    "confidence_score": 0.85
  }
}
```

**Error Message:**
```json
{
  "type": "error",
  "data": {
    "message": "Brand 'invalid-brand' not found or inactive"
  }
}
```

**Pong Response:**
```json
{
  "type": "pong",
  "data": {
    "timestamp": "2024-01-20T10:30:00"
  }
}
```

### Voice-Optimized Responses

When `voice: true` is set in the chat request:
- Responses are limited to **1 sentence maximum**
- **Concise and direct** wording optimized for voice output
- **Natural speech patterns** for text-to-speech systems
- **Same language detection** (English/Indonesian support)

### WebSocket Client Example

```javascript
// JavaScript WebSocket Client
const ws = new WebSocket('ws://localhost:8000/ws/chat/techpro');

ws.onopen = function(event) {
    console.log('Connected to TechPro chatbot');
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    
    switch(message.type) {
        case 'welcome':
            console.log('Welcome:', message.data.message);
            break;
            
        case 'chunk':
            // Append streaming content to UI
            appendToChat(message.data.content);
            break;
            
        case 'complete':
            // Handle suggested products and final response
            if (message.data.suggested_products) {
                displaySuggestedProducts(message.data.suggested_products);
            }
            console.log('Confidence:', message.data.confidence_score);
            break;
            
        case 'error':
            console.error('Error:', message.data.message);
            break;
    }
};

// Send a message
function sendMessage(text, isVoice = false) {
    const message = {
        type: 'chat',
        data: {
            message: text,
            voice: isVoice
        }
    };
    ws.send(JSON.stringify(message));
}

// Example usage
sendMessage("I need a powerful laptop for video editing");
sendMessage("What's the price?", true); // Voice-optimized response
```

---

## 🏢 Brand Management API

### Create Brand

#### `POST /brands`
**Description:** Create a new brand with automatic configuration setup.

**Query Parameters:**
- `name` (required): Brand name
- `description` (required): Brand description  
- `brand_id` (optional): Custom brand ID (auto-generated if not provided)

**Request:**
```bash
curl -X POST "http://localhost:8000/brands?name=TechCorp%20Solutions&description=Enterprise%20technology%20solutions&brand_id=techcorp"
```

**Response:**
```json
{
  "id": "techcorp",
  "name": "TechCorp Solutions",
  "description": "Enterprise technology solutions",
  "created_at": "2024-01-20T10:30:00",
  "updated_at": null,
  "is_active": true
}
```

### List Brands

#### `GET /brands`
**Description:** Get all brands (active and inactive).

**Response:**
```json
[
  {
    "id": "techpro",
    "name": "TechPro Solutions",
    "description": "Premium technology retailer",
    "created_at": "2024-01-20T10:00:00",
    "updated_at": null,
    "is_active": true
  },
  {
    "id": "techcorp",
    "name": "TechCorp Solutions", 
    "description": "Enterprise technology solutions",
    "created_at": "2024-01-20T10:30:00",
    "updated_at": null,
    "is_active": true
  }
]
```

#### `GET /brands/active`
**Description:** Get only active brands.

### Get Brand Details

#### `GET /brands/{brand_id}`
**Description:** Get details for a specific brand.

**Parameters:**
- `brand_id` (path): The brand identifier

### Update Brand

#### `PUT /brands/{brand_id}`
**Description:** Update brand information.

**Query Parameters:**
- `name` (optional): New brand name
- `description` (optional): New description
- `is_active` (optional): Active status

**Request:**
```bash
curl -X PUT "http://localhost:8000/brands/techcorp?name=TechCorp%20Enterprise&is_active=true"
```

### Delete Brand

#### `DELETE /brands/{brand_id}`
**Description:** Delete a brand and ALL its data (products, conversations, configurations).

**⚠️ Warning:** This operation is irreversible and will delete:
- All brand products from vector store
- All conversation histories
- Brand configuration
- All associated data

**Response:**
```json
{
  "message": "Brand deleted successfully"
}
```

---

## ⚙️ Brand Configuration API

### Get Brand Configuration

#### `GET /brands/{brand_id}/config`
**Description:** Get brand configuration including system prompt and appearance.

**Response:**
```json
{
  "brand_id": "techpro",
  "system_prompt": "You are a helpful customer service chatbot for TechPro Solutions...",
  "welcome_message": "Welcome to TechPro Solutions! How can I help you today?",
  "company_info": {
    "name": "TechPro Solutions",
    "founded": "2018",
    "specialty": "Business and professional technology equipment",
    "location": "North America",
    "mission": "Provide cutting-edge technology solutions..."
  },
  "appearance_settings": {
    "primary_color": "#007bff",
    "secondary_color": "#6c757d",
    "logo_url": "/static/techpro-logo.png"
  },
  "updated_at": "2024-01-20T10:30:00"
}
```

### Update Brand Configuration

#### `PUT /brands/{brand_id}/config`
**Description:** Update brand configuration (system prompt, welcome message, etc.).

**Request Body:**
```json
{
  "system_prompt": "You are a fashion consultant for StyleHub, a premium clothing retailer...",
  "welcome_message": "Welcome to StyleHub! How can I style your wardrobe today?",
  "company_info": {
    "name": "StyleHub",
    "founded": "2020",
    "specialty": "Sustainable fashion and styling",
    "mission": "Provide stylish, eco-friendly clothing solutions"
  },
  "appearance_settings": {
    "primary_color": "#ff6b6b",
    "secondary_color": "#4ecdc4",
    "logo_url": "/static/stylehub-logo.png"
  }
}
```

### Get Brand Statistics

#### `GET /brands/{brand_id}/stats`
**Description:** Get comprehensive statistics for a brand.

**Response:**
```json
{
  "brand_id": "techpro",
  "brand_name": "TechPro Solutions",
  "total_products": 12,
  "available_products": 11,
  "categories": 4,
  "active_conversations": 3,
  "category_list": ["Laptop", "Smartphone", "Monitor", "Accessories"]
}
```

---

## 💬 Chat API (Enhanced)

### WebSocket Streaming Chat

#### `WS /ws/chat/{brand_id}`
**Description:** Real-time streaming chat with a specific brand's chatbot.

**Connection Process:**
1. Connect to WebSocket endpoint
2. Receive welcome message
3. Send chat messages
4. Receive streaming response chunks
5. Handle final response with products

### Traditional Chat API

#### `POST /chat/{brand_id}`
**Description:** Traditional request-response chat with a specific brand.

**Request:**
```json
{
  "message": "I need a laptop for business work under $1500",
  "conversation_id": "optional-conversation-id",
  "user_id": "optional-user-id",
  "voice": false
}
```

**Response:**
```json
{
  "response": "I'd recommend the Dell XPS 13 Plus for Rp 19,999,000 (~$1,300). It's perfect for business professionals...",
  "conversation_id": "conv-123456789",
  "suggested_products": [...],
  "confidence_score": 0.95
}
```

### Get Conversation History

#### `GET /chat/{brand_id}/history/{conversation_id}`
**Description:** Retrieve conversation history for a specific brand and conversation.

**Response:**
```json
{
  "conversation_id": "conv-123456789",
  "brand_id": "techpro",
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

#### `DELETE /chat/{brand_id}/{conversation_id}`
**Description:** Clear conversation history for a specific brand and conversation.

---

## 📦 Product Management API (Brand-Scoped)

### Add Product to Brand

#### `POST /brands/{brand_id}/products`
**Description:** Add a new product to a specific brand's catalog.

**Request:**
```json
{
  "id": "laptop-007",
  "name": "Surface Laptop 5",
  "description": "Sleek and powerful laptop perfect for business professionals",
  "category": "Laptop",
  "price": 21499000.00,
  "features": [
    "12th Gen Intel Core i7 processor",
    "13.5-inch PixelSense touchscreen",
    "16GB LPDDR5x RAM",
    "512GB SSD storage"
  ],
  "specifications": {
    "processor": "Intel Core i7-1255U",
    "memory": "16GB LPDDR5x",
    "storage": "512GB SSD",
    "display": "13.5-inch PixelSense (2256x1504)",
    "weight": "1.29 kg",
    "battery": "Up to 17 hours",
    "os": "Windows 11 Home"
  },
  "availability": true
}
```

### Get Brand Products

#### `GET /brands/{brand_id}/products`
**Description:** Get all products from a specific brand's catalog.

### Update Brand Product

#### `PUT /brands/{brand_id}/products/{product_id}`
**Description:** Update an existing product in a specific brand's catalog.

### Delete Brand Product

#### `DELETE /brands/{brand_id}/products/{product_id}`
**Description:** Delete a product from a specific brand's catalog.

### Search Brand Products

#### `POST /brands/{brand_id}/products/search`
**Description:** Search for products within a specific brand's catalog.

**Request:**
```json
{
  "query": "lightweight laptop for travel",
  "category": "Laptop",
  "price_range": [15000000, 30000000],
  "limit": 5
}
```

**Response:**
```json
{
  "query": "lightweight laptop for travel",
  "brand_id": "techpro",
  "results": [
    {
      "product": {...},
      "similarity_score": 0.89
    }
  ]
}
```

### Get Brand Recommendations

#### `POST /brands/{brand_id}/recommendations`
**Description:** Get AI-powered product recommendations from a specific brand.

**Parameters:**
- `query` (query): Search query
- `limit` (query): Number of recommendations (default: 5)

**Response:**
```json
{
  "products": [...],
  "reasoning": "Based on your need for business work, I recommend these laptops because they offer excellent performance for productivity tasks...",
  "match_score": 0.92
}
```

### Get Brand Categories

#### `GET /brands/{brand_id}/categories`
**Description:** Get all available product categories for a specific brand.

**Response:**
```json
{
  "categories": ["Laptop", "Smartphone", "Monitor", "Accessories"],
  "brand_id": "techpro"
}
```

### Bulk Add Products

#### `POST /brands/{brand_id}/products/bulk`
**Description:** Add multiple products to a specific brand in a single request.

**Request:**
```json
[
  {product1},
  {product2},
  ...
]
```

**Response:**
```json
{
  "message": "Successfully added 8/10 products to techpro",
  "success_count": 8,
  "total_count": 10,
  "brand_id": "techpro"
}
```

---

## 📁 File Upload API (Brand-Scoped)

### Upload Product File to Brand

#### `POST /brands/{brand_id}/upload/products`
**Description:** Upload a file containing product data to a specific brand.

**Supported Formats:**
- JSON (.json)
- CSV (.csv)
- PDF (.pdf)
- Text (.txt, .md)
- Word (.docx)
- XML (.xml)

**Request:**
```bash
curl -X POST "http://localhost:8000/brands/techpro/upload/products" \
  -F "file=@products.json"
```

**Response:**
```json
{
  "message": "Successfully uploaded products.json and added 5 products to techpro",
  "filename": "products.json",
  "products_added": 5,
  "upload_id": "upload-123456789"
}
```

---

## 📊 Global Statistics API

### Get Global Statistics

#### `GET /stats`
**Description:** Get global API statistics across all brands.

**Response:**
```json
{
  "total_brands": 3,
  "active_brands": 2,
  "total_products": 25,
  "total_conversations": 8,
  "brands_stats": [
    {
      "brand_id": "techpro",
      "brand_name": "TechPro Solutions",
      "total_products": 12,
      "available_products": 11,
      "categories": 4,
      "active_conversations": 3
    },
    {
      "brand_id": "techcorp",
      "brand_name": "TechCorp Solutions",
      "total_products": 13,
      "available_products": 13,
      "categories": 3,
      "active_conversations": 5
    }
  ]
}
```

---

## 🔄 Legacy API Compatibility

All v1.0 endpoints continue to work and default to the "techpro" brand:

### Legacy Endpoints
- `POST /chat` → `POST /chat/techpro`
- `GET /products` → `GET /brands/techpro/products`
- `POST /products/search` → `POST /brands/techpro/products/search`
- `POST /recommendations` → `POST /brands/techpro/recommendations`
- `GET /categories` → `GET /brands/techpro/categories`

### Migration Path

1. **Immediate compatibility** - existing clients continue working
2. **Gradual migration** - update clients to use brand-specific endpoints
3. **Enhanced features** - adopt WebSocket streaming for real-time chat
4. **Multi-brand support** - create additional brands as needed

---

## 🔧 Data Models

### Brand Model
```json
{
  "id": "string",
  "name": "string",
  "description": "string", 
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_active": "boolean"
}
```

### BrandConfig Model
```json
{
  "brand_id": "string",
  "system_prompt": "string",
  "welcome_message": "string",
  "company_info": {
    "name": "string",
    "founded": "string",
    "specialty": "string",
    "location": "string",
    "mission": "string"
  },
  "appearance_settings": {
    "primary_color": "string",
    "secondary_color": "string", 
    "logo_url": "string"
  },
  "updated_at": "datetime"
}
```

### WebSocketChatRequest Model
```json
{
  "message": "string",
  "brand_id": "string",
  "conversation_id": "string (optional)",
  "user_id": "string (optional)",
  "voice": "boolean (default: false)"
}
```

### WebSocketChatChunk Model
```json
{
  "content": "string",
  "is_final": "boolean",
  "conversation_id": "string",
  "suggested_products": "Product[] (optional)",
  "confidence_score": "number (optional)"
}
```

### Enhanced ChatRequest Model
```json
{
  "message": "string",
  "conversation_id": "string (optional)",
  "user_id": "string (optional)",
  "voice": "boolean (optional)"
}
```

---

## 🚨 Error Responses

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request  
- `404`: Not Found (Brand/Product/Conversation)
- `500`: Internal Server Error

### WebSocket Error Messages
```json
{
  "type": "error",
  "data": {
    "message": "Specific error description"
  }
}
```

### Common Error Scenarios

**Brand Not Found:**
```json
{
  "detail": "Brand 'invalid-brand' not found or inactive"
}
```

**WebSocket Connection Error:**
```json
{
  "type": "error", 
  "data": {
    "message": "Brand 'invalid-brand' not found or inactive"
  }
}
```

**File Upload Error:**
```json
{
  "detail": "Unsupported file type. Supported formats: .json, .csv, .pdf, .txt, .md, .docx, .xml"
}
```

---

## 🧪 Testing Examples

### Test WebSocket Streaming

```python
import asyncio
import websockets
import json

async def test_streaming():
    uri = "ws://localhost:8000/ws/chat/techpro"
    
    async with websockets.connect(uri) as websocket:
        # Send test message
        message = {
            "type": "chat",
            "data": {
                "message": "I need a laptop for video editing",
                "voice": False
            }
        }
        await websocket.send(json.dumps(message))
        
        # Receive streaming response
        full_response = ""
        while True:
            data = await websocket.recv()
            msg = json.loads(data)
            
            if msg["type"] == "chunk":
                content = msg["data"]["content"]
                full_response += content
                print(content, end="", flush=True)
            elif msg["type"] == "complete":
                products = msg["data"]["suggested_products"]
                if products:
                    print(f"\nSuggested {len(products)} products")
                break

asyncio.run(test_streaming())
```

### Test Brand Management

```bash
# Create a new brand
curl -X POST "http://localhost:8000/brands" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fashion Forward",
    "description": "Trendy clothing and accessories",
    "brand_id": "fashion"
  }'

# Update brand configuration
curl -X PUT "http://localhost:8000/brands/fashion/config" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a fashion consultant...",
    "welcome_message": "Welcome to Fashion Forward!",
    "company_info": {
      "name": "Fashion Forward",
      "specialty": "Trendy clothing"
    }
  }'

# Add products to brand
curl -X POST "http://localhost:8000/brands/fashion/products" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "dress-001",
    "name": "Summer Floral Dress",
    "description": "Beautiful floral pattern dress",
    "category": "Dresses",
    "price": 899000.00,
    "features": ["Cotton blend", "Machine washable"],
    "specifications": {"size": "S-XL", "material": "Cotton"},
    "availability": true
  }'
```

### Test Voice-Optimized Responses

```bash
# WebSocket message with voice enabled
{
  "type": "chat",
  "data": {
    "message": "What's your cheapest laptop?",
    "voice": true
  }
}

# Expected response: Single sentence
"Our most affordable laptop is the Dell Inspiron 15 at Rp 8,999,000."
```

---

## 🚀 Production Deployment

### Environment Configuration

```env
# Required
OPENAI_API_KEY=your_production_api_key

# Recommended for production
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db

# Optional performance tuning
UVICORN_WORKERS=4
MAX_CONNECTIONS_PER_BRAND=100
WEBSOCKET_TIMEOUT=300
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

# Create data directory for persistence
RUN mkdir -p /app/data/chroma_db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Load Balancing Considerations

- **Sticky sessions** for WebSocket connections
- **Brand-based routing** for optimal performance  
- **Connection pooling** for database operations
- **Redis** for shared session state (future enhancement)

---

## 📚 Advanced Usage

### Custom Brand Implementation

```python
# Example: Create a clothing brand with custom prompts
import httpx

async def setup_clothing_brand():
    base_url = "http://localhost:8000"
    
    # Create brand
    brand_data = {
        "name": "StyleHub",
        "description": "Sustainable fashion and styling solutions",
        "brand_id": "stylehub"
    }
    
    async with httpx.AsyncClient() as client:
        # Create brand
        response = await client.post(f"{base_url}/brands", json=brand_data)
        print(f"Brand created: {response.json()}")
        
        # Configure brand
        config_data = {
            "system_prompt": """
            You are a fashion consultant for StyleHub, a sustainable fashion retailer.
            
            **About StyleHub:**
            - Founded in 2020, specializing in sustainable fashion
            - Eco-friendly materials and ethical production
            - Clothing for professionals and casual wear
            
            **Your Role:**
            - Help customers find perfect outfits
            - Provide styling advice and recommendations
            - Promote sustainability in fashion choices
            - Answer questions about sizing and materials
            
            Always be fashionable, helpful, and environmentally conscious.
            """,
            "welcome_message": "Welcome to StyleHub! How can I help you style your sustainable wardrobe today?",
            "company_info": {
                "name": "StyleHub",
                "founded": "2020",
                "specialty": "Sustainable fashion",
                "mission": "Making fashion sustainable and accessible"
            },
            "appearance_settings": {
                "primary_color": "#2ecc71",
                "secondary_color": "#27ae60"
            }
        }
        
        response = await client.put(f"{base_url}/brands/stylehub/config", json=config_data)
        print(f"Brand configured: {response.json()}")
```

### Multilingual Support

The system automatically detects and responds in the customer's language:

```python
# Indonesian conversation example
{
  "type": "chat",
  "data": {
    "message": "Saya butuh laptop untuk kerja bisnis dengan budget 20 juta",
    "voice": false
  }
}

# Response will be in Indonesian:
# "Saya merekomendasikan Dell XPS 13 Plus seharga Rp 19.999.000..."
```

---

## 🔍 Monitoring and Analytics

### Key Metrics to Track

- **WebSocket connections** per brand
- **Message throughput** and response times
- **Product recommendation accuracy** (confidence scores)
- **Brand-specific conversation volume**
- **Error rates** and connection failures

### Health Check Endpoint

```bash
curl "http://localhost:8000/"
```

Response includes active brand count and system status.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/websocket-enhancement`
3. Test WebSocket functionality: `python websocket_client_example.py`
4. Test brand management: Run brand creation/configuration tests
5. Submit pull request with documentation updates

---

## 📞 Support

For technical support:

- **Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **WebSocket Testing**: Use `websocket_client_example.py`
- **Debug Mode**: Set `LOG_LEVEL=DEBUG` for detailed logging
- **Server Logs**: Check uvicorn output for error details

---

## 📋 Changelog

### v2.0.0
- ✅ WebSocket streaming chat with real-time responses
- ✅ Multi-brand system with complete data isolation
- ✅ Brand management and configuration API
- ✅ Voice-optimized responses for voice interfaces
- ✅ Brand-scoped endpoints for all operations
- ✅ Enhanced models and data structures
- ✅ Backward compatibility with v1.0 API
- ✅ Comprehensive documentation and examples

### v1.0.0
- ✅ Basic chat functionality
- ✅ Product recommendations
- ✅ Vector-based product search
- ✅ Single-brand system 
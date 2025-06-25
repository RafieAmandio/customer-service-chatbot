# Multi-Brand Customer Service Chatbot API v2.0

A powerful backend API for multi-brand customer service chatbots with real-time WebSocket streaming, vector-based product recommendations, and comprehensive brand management.

## 🆕 What's New in V2.0

### WebSocket Streaming Chat
- **Real-time streaming responses** from OpenAI
- **Live typing indicators** and chunk-based delivery
- **Voice-optimized responses** for voice interfaces
- **Connection management** per brand

### Multi-Brand System
- **Separate brands** with isolated data stores
- **Custom system prompts** per brand
- **Brand-specific knowledge bases**
- **Configurable appearance settings**
- **Independent conversation management**

### Enhanced Features
- **Brand configuration management**
- **Isolated vector stores** per brand
- **Brand-specific file uploads**
- **Comprehensive brand statistics**
- **Legacy API compatibility**

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd be-chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 2. Environment Setup

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 3. Start the Server

```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or using the run script (if available)
./run.sh
```

### 4. Test WebSocket Connection

```bash
# Run the example WebSocket client
python websocket_client_example.py
```

## 📡 WebSocket API

### Connection Endpoint
```
ws://localhost:8000/ws/chat/{brand_id}
```

### Message Format

**Send Message:**
```json
{
  "type": "chat",
  "data": {
    "message": "Hello! I need a laptop for business",
    "conversation_id": "optional-conversation-id",
    "user_id": "optional-user-id",
    "voice": false
  }
}
```

**Receive Chunks:**
```json
{
  "type": "chunk",
  "data": {
    "content": "I'd be happy to help you find",
    "is_final": false,
    "conversation_id": "conv-123",
    "suggested_products": null,
    "confidence_score": null
  }
}
```

**Final Response:**
```json
{
  "type": "complete",
  "data": {
    "content": "",
    "is_final": true,
    "conversation_id": "conv-123",
    "suggested_products": [...],
    "confidence_score": 0.85
  }
}
```

### WebSocket Client Example

```python
import asyncio
import websockets
import json

async def chat_example():
    uri = "ws://localhost:8000/ws/chat/techpro"
    
    async with websockets.connect(uri) as websocket:
        # Send a message
        message = {
            "type": "chat",
            "data": {
                "message": "I need a powerful laptop for video editing",
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
                # Handle suggested products
                products = msg["data"]["suggested_products"]
                print(f"\nSuggested {len(products)} products")
                break

asyncio.run(chat_example())
```

## 🏢 Brand Management API

### Create a New Brand

```bash
curl -X POST "http://localhost:8000/brands" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechCorp Solutions",
    "description": "Enterprise technology solutions",
    "brand_id": "techcorp"
  }'
```

### Update Brand Configuration

```bash
curl -X PUT "http://localhost:8000/brands/techcorp/config" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a helpful assistant for TechCorp...",
    "welcome_message": "Welcome to TechCorp! How can I help?",
    "company_info": {
      "name": "TechCorp Solutions",
      "specialty": "Enterprise IT solutions"
    },
    "appearance_settings": {
      "primary_color": "#0066cc",
      "secondary_color": "#6c757d"
    }
  }'
```

### Brand-Specific Operations

All product and chat operations can be scoped to specific brands:

```bash
# Add product to specific brand
POST /brands/{brand_id}/products

# Chat with specific brand
POST /chat/{brand_id}
WS /ws/chat/{brand_id}

# Search products in specific brand
POST /brands/{brand_id}/products/search

# Upload files to specific brand
POST /brands/{brand_id}/upload/products
```

## 📊 API Endpoints

### Brand Management
- `GET /brands` - List all brands
- `GET /brands/active` - List active brands
- `POST /brands` - Create new brand
- `GET /brands/{brand_id}` - Get brand details
- `PUT /brands/{brand_id}` - Update brand
- `DELETE /brands/{brand_id}` - Delete brand
- `GET /brands/{brand_id}/config` - Get brand configuration
- `PUT /brands/{brand_id}/config` - Update brand configuration
- `GET /brands/{brand_id}/stats` - Get brand statistics

### Chat API (New)
- `WS /ws/chat/{brand_id}` - WebSocket streaming chat
- `POST /chat/{brand_id}` - Traditional chat API
- `GET /chat/{brand_id}/history/{conversation_id}` - Get conversation history
- `DELETE /chat/{brand_id}/{conversation_id}` - Clear conversation

### Product Management (Brand-Scoped)
- `POST /brands/{brand_id}/products` - Add product to brand
- `GET /brands/{brand_id}/products` - Get brand products
- `PUT /brands/{brand_id}/products/{product_id}` - Update product
- `DELETE /brands/{brand_id}/products/{product_id}` - Delete product
- `POST /brands/{brand_id}/products/search` - Search brand products
- `POST /brands/{brand_id}/products/bulk` - Bulk add products
- `POST /brands/{brand_id}/upload/products` - Upload product files

### Legacy Endpoints (Default to TechPro)
- `POST /chat` - Chat with TechPro
- `GET /products` - Get TechPro products
- `POST /products/search` - Search TechPro products

## 🔧 Configuration

### Brand Configuration Schema

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
    "primary_color": "#hex",
    "secondary_color": "#hex",
    "logo_url": "string"
  }
}
```

### System Prompt Customization

Each brand can have a completely custom system prompt:

```python
# Example system prompt for a clothing brand
system_prompt = """
You are a fashion consultant for StyleHub, a premium clothing retailer.

**About StyleHub:**
- Founded in 2020, we specialize in sustainable fashion
- We offer clothing for professionals and casual wear
- Our mission is to provide stylish, eco-friendly clothing

**Your Role:**
- Help customers find the perfect outfits
- Provide styling advice and recommendations
- Answer questions about sizing, materials, and care
- Promote our sustainability initiatives

Always be fashionable, helpful, and environmentally conscious.
"""
```

## 📦 Data Isolation

Each brand has completely isolated data:

- **Vector Store:** Separate ChromaDB collection per brand
- **Conversations:** Independent conversation history
- **Products:** Brand-specific product catalogs
- **Configuration:** Custom prompts and settings

## 🔄 Migration from V1.0

The API maintains backward compatibility:

1. **Existing endpoints** continue to work (default to TechPro brand)
2. **Data preservation** - existing data is automatically assigned to "techpro" brand
3. **Gradual migration** - add new brands while keeping existing functionality

### Migration Steps

1. **Start the V''2.0 server** - exi

sting data is automatically migrated
2. **Create new brands** using the brand management API
3. **Upload brand-specific data** using brand-scoped endpoints
4. **Update clients** to use WebSocket streaming (optional)

## 🛠️ Development

### File Structure

```
├── main.py                 # FastAPI app with WebSocket support
├── brand_service.py        # Multi-brand management
├── chatbot_service.py      # Enhanced chatbot with streaming
├── vector_store.py         # Brand-aware vector storage
├── models.py              # Pydantic models (enhanced)
├── config.py              # Configuration management
├── sample_data.py         # Sample data for testing
├── websocket_client_example.py  # WebSocket client example
├── requirements.txt       # Updated dependencies
└── brands_config.json     # Brand configuration storage
```

### Adding WebSocket Support to Frontend

```javascript
// JavaScript WebSocket client example
const ws = new WebSocket('ws://localhost:8000/ws/chat/techpro');

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    
    if (message.type === 'chunk') {
        // Append streaming content
        appendToChat(message.data.content);
    } else if (message.type === 'complete') {
        // Handle final response with products
        displaySuggestedProducts(message.data.suggested_products);
    }
};

// Send message
ws.send(JSON.stringify({
    type: 'chat',
    data: {
        message: 'Hello!',
        voice: false
    }
}));
```

## 🧪 Testing

### Test WebSocket Streaming

```bash
# Run the interactive WebSocket client
python websocket_client_example.py

# Test multiple brands
python -c "
import asyncio
from websocket_client_example import test_multiple_brands
asyncio.run(test_multiple_brands())
"
```

### Test Brand Management

```bash
# Create a test brand
curl -X POST "http://localhost:8000/brands" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Brand", "description": "Test description"}'

# List all brands
curl "http://localhost:8000/brands"

# Get brand stats
curl "http://localhost:8000/brands/test_brand/stats"
```

## 📈 Performance Considerations

### WebSocket Optimization
- **Connection pooling** per brand
- **Message batching** for high-frequency updates
- **Automatic reconnection** handling
- **Memory management** for long conversations

### Scaling
- **Horizontal scaling** with Redis for session management
- **Load balancing** with sticky sessions
- **Database optimization** with connection pooling
- **Caching** for frequently accessed brand configurations

## 🔒 Security

### WebSocket Security
- **Origin validation** for WebSocket connections
- **Rate limiting** per connection
- **Message size limits**
- **Connection timeout management**

### Brand Isolation
- **Data segregation** at the database level
- **Access control** per brand
- **Audit logging** for brand operations

## 🚀 Deployment

### Docker Support (Future)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_key_here

# Optional
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 📚 Documentation

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **WebSocket Testing:** Use the provided client examples
- **Brand Management:** See API endpoints section

## 🆘 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if server is running on correct port
   - Verify brand_id exists and is active

2. **Brand Not Found**
   - Ensure brand is created and active
   - Check brand_id spelling

3. **Streaming Issues**
   - Verify OpenAI API key is valid
   - Check network connectivity
   - Review server logs for errors

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Next Steps

- **Redis integration** for session management
- **Authentication & authorization** system
- **Analytics dashboard** for brand performance
- **A/B testing** framework for different prompts
- **Mobile SDK** for native app integration
- **Voice interface** optimization 
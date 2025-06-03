# Customer Service Chatbot Backend

A comprehensive backend API for a customer service chatbot that uses OpenAI for natural language processing and ChromaDB for vector-based product search and recommendations.

## Features

- 🤖 **AI-Powered Chat**: OpenAI GPT-4 integration for intelligent customer service
- 🔍 **Vector Search**: ChromaDB for semantic product search and recommendations
- 📊 **Product Management**: Full CRUD operations for product catalog
- 💬 **Conversation History**: Persistent chat sessions
- 🎯 **Smart Recommendations**: Context-aware product suggestions
- 🚀 **Fast API**: High-performance REST API with automatic documentation

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI**: GPT-4 for chat and text-embedding-ada-002 for embeddings
- **ChromaDB**: Vector database for semantic search
- **Pydantic**: Data validation and serialization
- **Python 3.8+**: Modern Python with async/await support

## Quick Start

### 1. Installation

```bash
# Clone the repository
cd be-chatbot

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 3. Run the Server

```bash
# Start the development server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Populate Sample Data

```bash
# Add sample products to the database
python sample_data.py
```

### 5. API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## API Endpoints

### Chat Endpoints

#### POST `/chat`
Start or continue a conversation with the chatbot.

```json
{
  "message": "I need a good laptop for video editing",
  "conversation_id": "optional-existing-id",
  "user_id": "optional-user-id"
}
```

Response:
```json
{
  "response": "For video editing, I'd recommend the MacBook Pro 14-inch...",
  "conversation_id": "unique-conversation-id",
  "suggested_products": [...],
  "confidence_score": 0.85
}
```

#### GET `/chat/history/{conversation_id}`
Get conversation history for a specific chat session.

#### DELETE `/chat/{conversation_id}`
Clear a conversation history.

### Product Management

#### POST `/products`
Add a new product to the catalog.

```json
{
  "id": "unique-product-id",
  "name": "Product Name",
  "description": "Detailed product description",
  "category": "Electronics",
  "price": 999.99,
  "features": ["Feature 1", "Feature 2"],
  "specifications": {
    "processor": "M2 Pro",
    "memory": "16GB"
  },
  "availability": true
}
```

#### GET `/products`
Get all products from the catalog.

#### PUT `/products/{product_id}`
Update an existing product.

#### DELETE `/products/{product_id}`
Delete a product from the catalog.

#### POST `/products/bulk`
Add multiple products at once.

### Search & Recommendations

#### POST `/products/search`
Search for products based on a query.

```json
{
  "query": "gaming laptop under $1500",
  "category": "Laptops",
  "price_range": [500, 1500],
  "limit": 5
}
```

#### POST `/recommendations`
Get AI-powered product recommendations with reasoning.

```bash
POST /recommendations?query=best%20headphones%20for%20music&limit=3
```

#### GET `/categories`
Get all available product categories.

#### GET `/stats`
Get API and database statistics.

## Usage Examples

### Basic Chat Interaction

```python
import httpx
import asyncio

async def chat_example():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/chat", json={
            "message": "I need wireless headphones for working out"
        })
        print(response.json())

asyncio.run(chat_example())
```

### Product Search

```python
async def search_example():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/products/search", json={
            "query": "smartphone with good camera",
            "limit": 3
        })
        print(response.json())

asyncio.run(search_example())
```

### Add Product

```python
async def add_product_example():
    product_data = {
        "id": "new-product-001",
        "name": "Amazing Product",
        "description": "This is an amazing product",
        "category": "Electronics",
        "price": 299.99,
        "features": ["Feature 1", "Feature 2"],
        "specifications": {"color": "black", "weight": "1kg"},
        "availability": True
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/products", json=product_data)
        print(response.json())

asyncio.run(add_product_example())
```

## Project Structure

```
be-chatbot/
├── main.py                 # FastAPI application and routes
├── config.py              # Configuration and environment variables
├── models.py              # Pydantic data models
├── vector_store.py        # ChromaDB integration
├── chatbot_service.py     # OpenAI integration and chat logic
├── sample_data.py         # Sample product data for testing
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── chroma_db/            # ChromaDB data directory (created automatically)
```

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4)
- `EMBEDDING_MODEL`: Embedding model (default: text-embedding-ada-002)
- `CHROMA_PERSIST_DIRECTORY`: ChromaDB storage path (default: ./chroma_db)

## Error Handling

The API includes comprehensive error handling:
- Invalid requests return 400 Bad Request
- Missing resources return 404 Not Found
- Server errors return 500 Internal Server Error
- All errors include descriptive messages

## Performance Considerations

- **Background Tasks**: Product embedding generation runs in background
- **Async Operations**: All I/O operations are asynchronous
- **Vector Search**: Efficient similarity search with ChromaDB
- **Conversation Management**: In-memory conversation storage (consider Redis for production)

## Production Deployment

For production deployment:

1. **Environment Variables**: Use proper secret management
2. **Database**: Consider persistent storage for conversations
3. **CORS**: Configure appropriate CORS origins
4. **Rate Limiting**: Add rate limiting middleware
5. **Monitoring**: Add logging and monitoring
6. **Scaling**: Consider horizontal scaling with load balancers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on the repository or contact the development team. 
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
from datetime import datetime
import json
import uuid
import os

from models import (
    Product, ChatRequest, ChatResponse, ProductQuery, 
    ProductRecommendation, ChatMessage, FileUpload, FileUploadResponse
)
from chatbot_service import ChatbotService
from vector_store import VectorStore
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Customer Service Chatbot API",
    description="A backend API for customer service chatbot with product recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chatbot_service = ChatbotService()
vector_store = VectorStore()

# File upload tracking
uploaded_files: List[FileUpload] = []
UPLOAD_DIR = "uploads"

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    print("🚀 Starting Customer Service Chatbot API...")
    print(f"OpenAI Model: {settings.OPENAI_MODEL}")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"Chroma DB Path: {settings.CHROMA_PERSIST_DIRECTORY}")
    
    # Auto-populate sample data if database is empty
    try:
        existing_products = vector_store.get_all_products()
        if len(existing_products) == 0:
            print("📚 Database is empty. Loading sample data...")
            await populate_sample_data()
            print("✅ Sample data loaded successfully!")
        else:
            print(f"📊 Found {len(existing_products)} existing products in database")
    except Exception as e:
        print(f"⚠️ Error checking/loading sample data: {e}")

async def populate_sample_data():
    """Populate the database with sample products"""
    from sample_data import SAMPLE_PRODUCTS
    
    success_count = 0
    for product in SAMPLE_PRODUCTS:
        try:
            if vector_store.add_product(product):
                success_count += 1
        except Exception as e:
            print(f"❌ Failed to add {product.name}: {e}")
    
    print(f"📦 Successfully loaded {success_count}/{len(SAMPLE_PRODUCTS)} sample products")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Customer Service Chatbot API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

# Chat Endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """Chat with the customer service chatbot"""
    try:
        response = await chatbot_service.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """Get conversation history"""
    try:
        history = chatbot_service.get_conversation_history(conversation_id)
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.delete("/chat/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation"""
    success = chatbot_service.clear_conversation(conversation_id)
    if success:
        return {"message": "Conversation cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

# Product Management Endpoints
@app.post("/products")
async def add_product(product: Product, background_tasks: BackgroundTasks):
    """Add a new product to the catalog"""
    try:
        # Add product to vector store in background
        success = vector_store.add_product(product)
        if success:
            return {"message": "Product added successfully", "product_id": product.id}
        else:
            raise HTTPException(status_code=500, detail="Failed to add product to vector store")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding product: {str(e)}")

@app.get("/products", response_model=List[Product])
async def get_all_products():
    """Get all products from the catalog"""
    try:
        products = vector_store.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")

@app.put("/products/{product_id}")
async def update_product(product_id: str, product: Product, background_tasks: BackgroundTasks):
    """Update an existing product"""
    try:
        if product.id != product_id:
            raise HTTPException(status_code=400, detail="Product ID mismatch")
        
        # Update product in vector store
        success = vector_store.update_product(product)
        if success:
            return {"message": "Product updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Delete a product from the catalog"""
    try:
        success = vector_store.delete_product(product_id)
        if success:
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

# Product Search and Recommendation Endpoints
@app.post("/products/search")
async def search_products(query: ProductQuery):
    """Search for products based on a query"""
    try:
        if query.category:
            results = vector_store.search_by_category(query.category, query.limit)
        else:
            results = vector_store.search_products(query.query, query.limit)
        
        # Filter by price range if specified
        if query.price_range:
            min_price, max_price = query.price_range
            results = [
                r for r in results 
                if min_price <= r["product"].price <= max_price
            ]
        
        return {
            "query": query.query,
            "results": [
                {
                    "product": result["product"],
                    "similarity_score": result["similarity_score"]
                }
                for result in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")

@app.post("/recommendations", response_model=ProductRecommendation)
async def get_recommendations(query: str, limit: int = 5):
    """Get product recommendations with reasoning"""
    try:
        recommendations = await chatbot_service.get_product_recommendations(query, limit)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get all available product categories"""
    try:
        products = vector_store.get_all_products()
        categories = list(set(product.category for product in products))
        return {"categories": sorted(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

# Utility Endpoints
@app.post("/products/bulk")
async def add_products_bulk(products: List[Product]):
    """Add multiple products in bulk"""
    try:
        success_count = 0
        for product in products:
            if vector_store.add_product(product):
                success_count += 1
        
        return {
            "message": f"Successfully added {success_count}/{len(products)} products",
            "success_count": success_count,
            "total_count": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding products in bulk: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    try:
        all_products = vector_store.get_all_products()
        categories = list(set(product.category for product in all_products))
        available_products = [p for p in all_products if p.availability]
        
        return {
            "total_products": len(all_products),
            "available_products": len(available_products),
            "categories": len(categories),
            "conversations_active": chatbot_service.get_active_conversations_count(),
            "category_list": sorted(categories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

# File Upload Endpoints
@app.post("/upload/products", response_model=FileUploadResponse)
async def upload_product_file(file: UploadFile = File(...)):
    """Upload a JSON or CSV file containing product data"""
    try:
        # Validate file type
        if not file.filename.endswith(('.json', '.csv')):
            raise HTTPException(status_code=400, detail="Only JSON and CSV files are supported")
        
        # Save uploaded file
        upload_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{upload_id}_{file.filename}")
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Parse and add products
        products_added = 0
        if file.filename.endswith('.json'):
            products_added = await _process_json_file(file_path)
        elif file.filename.endswith('.csv'):
            products_added = await _process_csv_file(file_path)
        
        # Track uploaded file
        file_upload = FileUpload(
            filename=file.filename,
            upload_time=datetime.now(),
            file_size=len(content),
            products_added=products_added,
            status="success" if products_added > 0 else "failed"
        )
        uploaded_files.append(file_upload)
        
        return FileUploadResponse(
            message=f"Successfully uploaded {file.filename} and added {products_added} products",
            filename=file.filename,
            products_added=products_added,
            upload_id=upload_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/uploads", response_model=List[FileUpload])
async def get_uploaded_files():
    """Get list of all uploaded files"""
    return uploaded_files

@app.get("/uploads/{filename}")
async def get_upload_details(filename: str):
    """Get details of a specific uploaded file"""
    for upload in uploaded_files:
        if upload.filename == filename:
            return upload
    raise HTTPException(status_code=404, detail="File not found")

async def _process_json_file(file_path: str) -> int:
    """Process a JSON file containing product data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products_added = 0
        
        # Handle both single product and array of products
        if isinstance(data, list):
            for product_data in data:
                try:
                    product = Product(**product_data)
                    if vector_store.add_product(product):
                        products_added += 1
                except Exception as e:
                    print(f"Error adding product: {e}")
        elif isinstance(data, dict):
            try:
                product = Product(**data)
                if vector_store.add_product(product):
                    products_added += 1
            except Exception as e:
                print(f"Error adding product: {e}")
        
        return products_added
        
    except Exception as e:
        print(f"Error processing JSON file: {e}")
        return 0

async def _process_csv_file(file_path: str) -> int:
    """Process a CSV file containing product data"""
    try:
        import pandas as pd
        
        df = pd.read_csv(file_path)
        products_added = 0
        
        for _, row in df.iterrows():
            try:
                # Parse features and specifications from string format
                features = row.get('features', '').split(',') if row.get('features') else []
                features = [f.strip() for f in features if f.strip()]
                
                specs = {}
                if 'specifications' in row and pd.notna(row['specifications']):
                    # Assume specifications are in JSON format in the CSV
                    specs = json.loads(row['specifications'])
                
                product = Product(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    category=row['category'],
                    price=float(row['price']),
                    features=features,
                    specifications=specs,
                    availability=bool(row.get('availability', True))
                )
                
                if vector_store.add_product(product):
                    products_added += 1
                    
            except Exception as e:
                print(f"Error adding product from CSV row: {e}")
        
        return products_added
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return 0

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
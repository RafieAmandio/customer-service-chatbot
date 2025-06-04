from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: float
    features: List[str]
    specifications: Dict[str, Any]
    availability: bool = True

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    voice: Optional[bool] = False  # New parameter for voice responses

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    suggested_products: Optional[List[Product]] = None
    confidence_score: Optional[float] = None

class ProductQuery(BaseModel):
    query: str
    category: Optional[str] = None
    price_range: Optional[tuple[float, float]] = None
    limit: int = 5

class ProductRecommendation(BaseModel):
    products: List[Product]
    reasoning: str
    match_score: float

# New models for file upload functionality
class FileUpload(BaseModel):
    filename: str
    upload_time: datetime
    file_size: int
    products_added: int
    status: str

class FileUploadResponse(BaseModel):
    message: str
    filename: str
    products_added: int
    upload_id: str 
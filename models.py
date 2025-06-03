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
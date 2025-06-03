import chromadb
from chromadb.config import Settings as ChromaSettings
from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
import uuid
from config import settings
from models import Product

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="products",
            metadata={"hnsw:space": "cosine"}
        )
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        try:
            response = self.openai_client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    def prepare_product_text(self, product: Product) -> str:
        """Prepare product data for embedding"""
        features_text = ", ".join(product.features)
        specs_text = ", ".join([f"{k}: {v}" for k, v in product.specifications.items()])
        
        return f"""
        Product: {product.name}
        Category: {product.category}
        Description: {product.description}
        Price: ${product.price}
        Features: {features_text}
        Specifications: {specs_text}
        Available: {product.availability}
        """.strip()

    def add_product(self, product: Product) -> bool:
        """Add a product to the vector store"""
        try:
            product_text = self.prepare_product_text(product)
            embedding = self.generate_embedding(product_text)
            
            self.collection.add(
                embeddings=[embedding],
                documents=[product_text],
                metadatas=[{
                    "product_id": product.id,
                    "name": product.name,
                    "category": product.category,
                    "price": product.price,
                    "availability": product.availability,
                    "product_data": product.model_dump_json()
                }],
                ids=[product.id]
            )
            return True
        except Exception as e:
            print(f"Error adding product to vector store: {e}")
            return False

    def search_products(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for products based on query"""
        try:
            query_embedding = self.generate_embedding(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                include=["metadatas", "documents", "distances"]
            )
            
            products = []
            if results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    product_data = json.loads(metadata['product_data'])
                    products.append({
                        "product": Product(**product_data),
                        "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                        "context": results['documents'][0][i]
                    })
            
            return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return []

    def search_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search products by category"""
        try:
            results = self.collection.get(
                where={"category": category},
                limit=limit,
                include=["metadatas", "documents"]
            )
            
            products = []
            for metadata in results['metadatas']:
                product_data = json.loads(metadata['product_data'])
                products.append({
                    "product": Product(**product_data),
                    "similarity_score": 1.0,  # Perfect match for category
                    "context": metadata
                })
            
            return products
        except Exception as e:
            print(f"Error searching by category: {e}")
            return []

    def get_all_products(self) -> List[Product]:
        """Get all products from the vector store"""
        try:
            results = self.collection.get(include=["metadatas"])
            products = []
            for metadata in results['metadatas']:
                product_data = json.loads(metadata['product_data'])
                products.append(Product(**product_data))
            return products
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    def update_product(self, product: Product) -> bool:
        """Update a product in the vector store"""
        try:
            # Delete existing product
            self.collection.delete(ids=[product.id])
            # Add updated product
            return self.add_product(product)
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_product(self, product_id: str) -> bool:
        """Delete a product from the vector store"""
        try:
            self.collection.delete(ids=[product_id])
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False 
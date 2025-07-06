from typing import Dict, List, Optional
import json
import uuid
from datetime import datetime
from models import Brand, BrandConfig
from chatbot_service import ChatbotService
from vector_store import VectorStore
import os

class BrandService:
    def __init__(self):
        self.brands: Dict[str, Brand] = {}
        self.brand_configs: Dict[str, BrandConfig] = {}
        self.chatbot_instances: Dict[str, ChatbotService] = {}
        self.config_file = "brands_config.json"
        
        # Load existing brands from config file
        self._load_brands_from_file()
        
        # Initialize default brand if no brands exist
        if not self.brands:
            self._create_default_brand()
    
    def _load_brands_from_file(self):
        """Load brands and configurations from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Load brands
                    for brand_data in data.get('brands', []):
                        brand = Brand(**brand_data)
                        self.brands[brand.id] = brand
                    
                    # Load brand configs
                    for config_data in data.get('configs', []):
                        config = BrandConfig(**config_data)
                        self.brand_configs[config.brand_id] = config
                        
                    print(f"Loaded {len(self.brands)} brands from config file")
        except Exception as e:
            print(f"Error loading brands from file: {e}")
    
    def _save_brands_to_file(self):
        """Save brands and configurations to JSON file"""
        try:
            data = {
                'brands': [brand.model_dump() for brand in self.brands.values()],
                'configs': [config.model_dump() for config in self.brand_configs.values()]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Error saving brands to file: {e}")
    
    def _create_default_brand(self):
        """Create default TechPro Solutions brand"""
        default_brand = Brand(
            id="techpro",
            name="TechPro Solutions",
            description="Premium technology retailer specializing in business and professional equipment",
            created_at=datetime.now(),
            is_active=True
        )
        
        default_config = BrandConfig(
            brand_id="techpro",
            system_prompt="""
            You are a helpful customer service chatbot for TechPro Solutions, a premium technology retailer specializing in business and professional equipment.

            **MULTILINGUAL SUPPORT:**
            You can communicate in both English and Indonesian (Bahasa Indonesia). Always respond in the same language the customer uses.

            **About TechPro Solutions:**
            - Founded in 2018, we serve businesses, professionals, and tech enthusiasts across North America
            - We specialize in business laptops, workstations, creative systems, and professional accessories
            - We partner with top brands like Apple, Dell, HP, Lenovo, ASUS, and more
            - Our mission is to provide cutting-edge technology solutions that empower productivity and innovation

            **Current Promotions & Services:**
            - 10% off business laptop bundles (laptop + monitor + accessories)
            - Free setup and data migration with laptop purchases over $1,500
            - Extended warranty at 50% off for first-time business customers
            - Volume discounts: 5 units (5% off) up to 50+ units (15% off)
            - 24/7 technical support and same-day delivery in major metropolitan areas

            Always be professional, knowledgeable, and helpful.
            """,
            welcome_message="Welcome to TechPro Solutions! How can I help you find the perfect technology solution today?",
            company_info={
                "name": "TechPro Solutions",
                "founded": "2018",
                "specialty": "Business and professional technology equipment",
                "location": "North America",
                "mission": "Provide cutting-edge technology solutions that empower productivity and innovation"
            },
            appearance_settings={
                "primary_color": "#007bff",
                "secondary_color": "#6c757d",
                "logo_url": "/static/techpro-logo.png"
            },
            updated_at=datetime.now()
        )
        
        self.brands["techpro"] = default_brand
        self.brand_configs["techpro"] = default_config
        self._save_brands_to_file()
        
        print("Created default TechPro Solutions brand")
    
    def create_brand(self, name: str, description: str, brand_id: Optional[str] = None) -> Brand:
        """Create a new brand"""
        
        # Sanitize brand ID to be compliant with ChromaDB's naming scheme
        id_source = brand_id if brand_id else name
        sanitized_id = id_source.lower().replace(" ", "-")

        # Ensure unique ID
        final_id = sanitized_id
        counter = 1
        while final_id in self.brands:
            final_id = f"{sanitized_id}-{counter}"
            counter += 1
        
        if final_id in self.brands:
            raise ValueError(f"Brand with ID '{final_id}' already exists")
        
        brand = Brand(
            id=final_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            is_active=True
        )
        
        # Create default config for the brand
        default_config = BrandConfig(
            brand_id=final_id,
            system_prompt=f"""
            You are a helpful customer service chatbot for {name}.
            
            **About {name}:**
            {description}
            
            **Your Role:**
            - Help customers with their inquiries
            - Provide information about products and services
            - Be professional, knowledgeable, and helpful
            - Respond in the same language as the customer
            
            Always maintain a helpful and professional tone.
            """,
            welcome_message=f"Welcome to {name}! How can I assist you today?",
            company_info={
                "name": name,
                "description": description
            },
            appearance_settings={
                "primary_color": "#007bff",
                "secondary_color": "#6c757d"
            },
            updated_at=datetime.now()
        )
        
        self.brands[final_id] = brand
        self.brand_configs[final_id] = default_config
        self._save_brands_to_file()
        
        print(f"Created new brand: {name} (ID: {final_id})")
        return brand
    
    def get_brand(self, brand_id: str) -> Optional[Brand]:
        """Get a brand by ID"""
        return self.brands.get(brand_id)
    
    def get_all_brands(self) -> List[Brand]:
        """Get all brands"""
        return list(self.brands.values())
    
    def get_active_brands(self) -> List[Brand]:
        """Get all active brands"""
        return [brand for brand in self.brands.values() if brand.is_active]
    
    def update_brand(self, brand_id: str, name: Optional[str] = None, description: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Brand]:
        """Update a brand"""
        if brand_id not in self.brands:
            return None
        
        brand = self.brands[brand_id]
        
        if name is not None:
            brand.name = name
        if description is not None:
            brand.description = description
        if is_active is not None:
            brand.is_active = is_active
        
        brand.updated_at = datetime.now()
        self._save_brands_to_file()
        
        # Remove chatbot instance if brand is deactivated
        if is_active is False and brand_id in self.chatbot_instances:
            del self.chatbot_instances[brand_id]
        
        return brand
    
    def delete_brand(self, brand_id: str) -> bool:
        """Delete a brand and its data"""
        if brand_id not in self.brands:
            return False
        
        try:
            # Delete vector store data
            vector_store = VectorStore(brand_id=brand_id)
            vector_store.delete_brand_collection()
            
            # Remove from memory
            del self.brands[brand_id]
            if brand_id in self.brand_configs:
                del self.brand_configs[brand_id]
            if brand_id in self.chatbot_instances:
                del self.chatbot_instances[brand_id]
            
            self._save_brands_to_file()
            
            print(f"Deleted brand: {brand_id}")
            return True
            
        except Exception as e:
            print(f"Error deleting brand {brand_id}: {e}")
            return False
    
    def get_brand_config(self, brand_id: str) -> Optional[BrandConfig]:
        """Get brand configuration"""
        return self.brand_configs.get(brand_id)
    
    def update_brand_config(
        self, 
        brand_id: str, 
        system_prompt: Optional[str] = None,
        persona_prompt: Optional[str] = None,
        welcome_message: Optional[str] = None,
        company_info: Optional[Dict] = None,
        appearance_settings: Optional[Dict] = None
    ) -> Optional[BrandConfig]:
        """Update brand configuration"""
        if brand_id not in self.brand_configs:
            return None
        
        config = self.brand_configs[brand_id]
        
        if system_prompt is not None:
            config.system_prompt = system_prompt
        if persona_prompt is not None:
            config.persona_prompt = persona_prompt
        if welcome_message is not None:
            config.welcome_message = welcome_message
        if company_info is not None:
            config.company_info = company_info
        if appearance_settings is not None:
            config.appearance_settings = appearance_settings
        
        config.updated_at = datetime.now()
        self._save_brands_to_file()
        
        # Remove existing chatbot instance to force reload with new config
        if brand_id in self.chatbot_instances:
            del self.chatbot_instances[brand_id]
        
        return config
    
    def get_chatbot_instance(self, brand_id: str) -> Optional[ChatbotService]:
        """Get or create chatbot instance for a brand"""
        if brand_id not in self.brands or not self.brands[brand_id].is_active:
            return None
        
        if brand_id not in self.chatbot_instances:
            brand_config = self.brand_configs.get(brand_id)
            self.chatbot_instances[brand_id] = ChatbotService(
                brand_id=brand_id,
                brand_config=brand_config
            )
        
        return self.chatbot_instances[brand_id]
    
    def refresh_chatbot_instance(self, brand_id: str) -> bool:
        """Force refresh chatbot instance with updated configuration"""
        try:
            if brand_id not in self.brands or not self.brands[brand_id].is_active:
                return False
            
            # Remove existing instance to force recreation with new config
            if brand_id in self.chatbot_instances:
                del self.chatbot_instances[brand_id]
            
            # Create new instance with updated config
            brand_config = self.brand_configs.get(brand_id)
            self.chatbot_instances[brand_id] = ChatbotService(
                brand_id=brand_id,
                brand_config=brand_config
            )
            
            print(f"Refreshed chatbot instance for brand: {brand_id}")
            return True
            
        except Exception as e:
            print(f"Error refreshing chatbot instance for {brand_id}: {e}")
            return False
    
    def get_brand_stats(self, brand_id: str) -> Optional[Dict]:
        """Get statistics for a brand"""
        if brand_id not in self.brands:
            return None
        
        try:
            vector_store = VectorStore(brand_id=brand_id)
            products = vector_store.get_all_products()
            
            chatbot = self.get_chatbot_instance(brand_id)
            active_conversations = chatbot.get_active_conversations_count() if chatbot else 0
            
            categories = list(set(product.category for product in products))
            available_products = [p for p in products if p.availability]
            
            return {
                "brand_id": brand_id,
                "brand_name": self.brands[brand_id].name,
                "total_products": len(products),
                "available_products": len(available_products),
                "categories": len(categories),
                "active_conversations": active_conversations,
                "category_list": sorted(categories)
            }
            
        except Exception as e:
            print(f"Error getting brand stats for {brand_id}: {e}")
            return None
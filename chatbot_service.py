from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime
from config import settings
from models import ChatMessage, ChatRequest, ChatResponse, Product, ProductRecommendation
from vector_store import VectorStore

class ChatbotService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_store = VectorStore()
        self.conversations: Dict[str, List[ChatMessage]] = {}
        
        # Enhanced system prompt with multilingual support
        self.system_prompt = """
        You are a helpful customer service chatbot for TechPro Solutions, a premium technology retailer specializing in business and professional equipment.

        **MULTILINGUAL SUPPORT:**
        You can communicate in both English and Indonesian (Bahasa Indonesia). Always respond in the same language the customer uses. If they switch languages, follow their language preference.

        **About TechPro Solutions:**
        - Founded in 2018, we serve businesses, professionals, and tech enthusiasts across North America
        - We specialize in business laptops, workstations, creative systems, and professional accessories
        - We partner with top brands like Apple, Dell, HP, Lenovo, ASUS, and more
        - Our mission is to provide cutting-edge technology solutions that empower productivity and innovation

        **Your Role & Guidelines:**
        1. Help customers find the perfect technology solutions for their needs
        2. Provide detailed product information, comparisons, and recommendations
        3. Answer questions about our company, services, and current promotions
        4. Maintain context throughout the conversation - remember what customers have told you
        5. Be professional, knowledgeable, and helpful
        6. Respond in the same language as the customer (English or Indonesian)

        **Current Promotions & Services:**
        - 10% off business laptop bundles (laptop + monitor + accessories)
        - Free setup and data migration with laptop purchases over $1,500
        - Extended warranty at 50% off for first-time business customers
        - Volume discounts: 5 units (5% off) up to 50+ units (15% off)
        - 24/7 technical support and same-day delivery in major metropolitan areas

        **When recommending products:**
        - Ask clarifying questions about intended use, budget, and preferences
        - Explain why certain products are good fits for their requirements
        - Mention key features, specifications, and benefits
        - Consider their business needs and productivity requirements
        - Suggest relevant accessories or bundles when appropriate

        **Conversation Guidelines:**
        - Remember previous messages in the conversation
        - Reference earlier parts of the conversation when relevant
        - Build on what the customer has already told you
        - If they mention specific requirements, keep those in mind for future recommendations
        - Detect the language used and respond appropriately

        Always be honest about product availability and limitations.
        Keep responses informative but conversational.
        """

    async def _is_asking_for_product_recommendations(self, message: str, conversation_history: List[ChatMessage]) -> bool:
        """
        Use OpenAI to determine if the user is asking for product recommendations
        Supports both English and Indonesian
        """
        try:
            # Build context from recent conversation
            recent_context = ""
            if len(conversation_history) > 1:
                recent_messages = conversation_history[-4:]  # Last 4 messages for context
                context_parts = []
                for msg in recent_messages:
                    if msg.role != "system":
                        context_parts.append(f"{msg.role}: {msg.content}")
                recent_context = "\n".join(context_parts)

            prompt = f"""
            Analyze the following customer message and conversation context to determine if the customer is asking for product recommendations, product information, product comparisons, or wants to know about specific products.

            Current message: "{message}"

            Recent conversation context:
            {recent_context}

            Instructions:
            - Return ONLY "true" or "false"
            - Return "true" if the customer is:
              * Asking for product recommendations (in any language)
              * Looking for specific products
              * Asking about product features, specifications, or comparisons
              * Asking "what do you have", "show me products", "I need...", "I'm looking for..."
              * Using Indonesian phrases like "saya butuh", "rekomendasikan", "produk apa", "laptop apa", etc.
              * Asking about prices, availability, or technical specs of products
            - Return "false" if the customer is:
              * Asking about company information
              * Asking about promotions/services in general
              * Asking for support/help
              * Just greeting or having general conversation
              * Asking about policies, warranty, shipping, etc. without mentioning specific products

            Examples of TRUE:
            - "I need a laptop for business"
            - "What laptops do you recommend?"
            - "Saya butuh laptop untuk kerja"
            - "Show me your MacBooks"
            - "Compare Dell vs HP laptops"
            - "What's the price of iPhone 15?"

            Examples of FALSE:
            - "Tell me about your company"
            - "What promotions do you have?"
            - "Hello, how are you?"
            - "Ceritakan tentang perusahaan kalian"
            - "What's your warranty policy?"

            Response (true/false):
            """

            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip().lower()
            return result == "true"
            
        except Exception as e:
            print(f"Error determining recommendation intent: {e}")
            # Fallback: simple keyword detection for both languages
            product_keywords = [
                # English keywords
                'laptop', 'computer', 'macbook', 'iphone', 'monitor', 'mouse', 'keyboard',
                'recommend', 'suggest', 'need', 'looking for', 'want', 'buy', 'purchase',
                'price', 'cost', 'budget', 'specs', 'specifications', 'features',
                'compare', 'difference', 'vs', 'versus', 'which', 'what', 'show me',
                # Indonesian keywords
                'laptop', 'komputer', 'handphone', 'hp', 'monitor', 'mouse', 'keyboard',
                'rekomendasikan', 'sarankan', 'butuh', 'perlu', 'cari', 'mau', 'ingin', 'beli',
                'harga', 'biaya', 'budget', 'spesifikasi', 'spek', 'fitur',
                'bandingkan', 'banding', 'perbedaan', 'mana yang', 'apa', 'tunjukkan'
            ]
            
            message_lower = message.lower()
            return any(keyword in message_lower for keyword in product_keywords)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Main chat function that handles customer queries with conversation history"""
        try:
            # Get or create conversation
            conversation_id = request.conversation_id or str(uuid.uuid4())
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = [
                    ChatMessage(role="system", content=self.system_prompt, timestamp=datetime.now())
                ]
            
            # Add user message to conversation
            user_message = ChatMessage(
                role="user", 
                content=request.message, 
                timestamp=datetime.now()
            )
            self.conversations[conversation_id].append(user_message)
            
            # Check if user is asking for product recommendations
            is_asking_for_products = await self._is_asking_for_product_recommendations(
                request.message, 
                self.conversations[conversation_id]
            )
            
            relevant_products = []
            product_context = ""
            suggested_products = None
            confidence_score = None
            
            # Only search for products if the user is asking for them
            if is_asking_for_products:
                relevant_products = self.vector_store.search_products(request.message, limit=5)
                product_context = self._prepare_product_context(relevant_products)
                suggested_products = [item["product"] for item in relevant_products[:3]] if relevant_products else []
                confidence_score = self._calculate_confidence(relevant_products)
            
            # Generate response using OpenAI with full conversation context
            response_content = await self._generate_response(
                conversation_id, 
                product_context,
                request.message,
                is_asking_for_products,
                is_voice=request.voice  # Pass voice parameter
            )
            
            # Add assistant response to conversation
            assistant_message = ChatMessage(
                role="assistant", 
                content=response_content, 
                timestamp=datetime.now()
            )
            self.conversations[conversation_id].append(assistant_message)
            
            return ChatResponse(
                response=response_content,
                conversation_id=conversation_id,
                suggested_products=suggested_products,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            print(f"Error in chat service: {e}")
            return ChatResponse(
                response="I'm sorry, I'm having trouble processing your request right now. Please try again. / Maaf, saya mengalami kesulitan memproses permintaan Anda. Silakan coba lagi.",
                conversation_id=conversation_id or str(uuid.uuid4())
            )

    def _prepare_product_context(self, relevant_products: List[Dict[str, Any]]) -> str:
        """Prepare product information for the AI model"""
        if not relevant_products:
            return "No specific products found for this query."
        
        context = "Here are some relevant products from our TechPro Solutions catalog:\n\n"
        for i, item in enumerate(relevant_products[:5], 1):
            product = item["product"]
            score = item["similarity_score"]
            
            context += f"{i}. **{product.name}** (Category: {product.category})\n"
            context += f"   Price: ${product.price:,.2f}\n"
            context += f"   Description: {product.description}\n"
            context += f"   Key Features: {', '.join(product.features[:3])}{'...' if len(product.features) > 3 else ''}\n"
            context += f"   Available: {'Yes' if product.availability else 'No'}\n"
            context += f"   Relevance Score: {score:.2f}\n\n"
        
        return context

    async def _generate_response(self, conversation_id: str, product_context: str, current_message: str, is_product_request: bool, is_voice: bool = False) -> str:
        """Generate response using OpenAI with full conversation context"""
        try:
            # Prepare messages for OpenAI - include full conversation history
            messages = []
            conversation_history = self.conversations[conversation_id]
            
            # Add all conversation messages
            for msg in conversation_history:
                messages.append({"role": msg.role, "content": msg.content})
            
            # Add voice-specific instruction if needed
            if is_voice:
                voice_instruction = """
                IMPORTANT: This is a voice response request. Your response must be:
                - Maximum 1 sentence
                - Concise and direct
                - Natural for voice output
                - Still helpful and informative
                
                Respond in the same language as the customer (English or Indonesian).
                """
                messages.append({
                    "role": "system",
                    "content": voice_instruction
                })
            
            # Add product context only if this is a product-related request
            if is_product_request and product_context and product_context != "No specific products found for this query.":
                context_message = f"""
                Product Information for current query "{current_message}":
                {product_context}
                
                Use this product information to help answer the customer's question. Remember to:
                - Respond in the same language as the customer (English or Indonesian)
                - Reference their conversation history when relevant
                - Suggest products that match their stated needs and preferences
                - Mention current promotions when appropriate
                {"- Keep response to 1 sentence maximum for voice output" if is_voice else "- Ask follow-up questions to better understand their requirements"}
                """
                messages.append({
                    "role": "system", 
                    "content": context_message
                })
            elif is_product_request and not product_context:
                # If asking for products but none found
                no_products_message = f"""
                The customer is asking for product recommendations, but no matching products were found in the database. 
                Please acknowledge their request and suggest they:
                1. Try different search terms
                2. Contact our support team for personalized assistance
                3. Browse our website categories
                
                Respond in the same language as the customer.
                {"Keep response to 1 sentence maximum for voice output." if is_voice else ""}
                """
                messages.append({
                    "role": "system",
                    "content": no_products_message
                })
            
            # Adjust max_tokens for voice responses
            max_tokens = 50 if is_voice else 600
            
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            
            # Additional safety check for voice responses - ensure it's truly 1 sentence
            if is_voice:
                # Split by sentence-ending punctuation and take first sentence
                import re
                sentences = re.split(r'[.!?]+', response_content)
                if sentences and sentences[0].strip():
                    response_content = sentences[0].strip() + "."
            
            return response_content
            
        except Exception as e:
            print(f"Error generating OpenAI response: {e}")
            if is_voice:
                return "Sorry, I'm having trouble right now. / Maaf, saya mengalami masalah."
            return "I apologize, but I'm having trouble generating a response right now. Please try rephrasing your question. / Maaf, saya mengalami kesulitan memberikan respons saat ini. Silakan coba ulangi pertanyaan Anda."

    def _calculate_confidence(self, relevant_products: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on product relevance"""
        if not relevant_products:
            return 0.0
        
        # Average similarity score of all relevant products
        scores = [item["similarity_score"] for item in relevant_products]
        return sum(scores) / len(scores)

    async def get_product_recommendations(self, query: str, limit: int = 5) -> ProductRecommendation:
        """Get specific product recommendations based on a query"""
        try:
            relevant_products = self.vector_store.search_products(query, limit)
            
            if not relevant_products:
                return ProductRecommendation(
                    products=[],
                    reasoning="No products found matching your criteria. Please try a different search term or contact our support team for personalized assistance.",
                    match_score=0.0
                )
            
            products = [item["product"] for item in relevant_products]
            avg_score = sum(item["similarity_score"] for item in relevant_products) / len(relevant_products)
            
            # Generate reasoning using OpenAI
            reasoning = await self._generate_recommendation_reasoning(query, relevant_products)
            
            return ProductRecommendation(
                products=products,
                reasoning=reasoning,
                match_score=avg_score
            )
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return ProductRecommendation(
                products=[],
                reasoning="Error retrieving recommendations. Please try again or contact support.",
                match_score=0.0
            )

    async def _generate_recommendation_reasoning(self, query: str, relevant_products: List[Dict[str, Any]]) -> str:
        """Generate reasoning for product recommendations with multilingual support"""
        try:
            product_info = self._prepare_product_context(relevant_products)
            
            # Detect if query is in Indonesian
            indonesian_keywords = ['saya', 'butuh', 'perlu', 'cari', 'mau', 'ingin', 'untuk', 'yang', 'apa', 'bagaimana']
            is_indonesian = any(keyword in query.lower() for keyword in indonesian_keywords)
            
            if is_indonesian:
                prompt = f"""
                Pertanyaan Pelanggan: "{query}"
                
                {product_info}
                
                Sebagai customer service TechPro Solutions, berikan penjelasan singkat (2-3 kalimat) dalam Bahasa Indonesia
                mengapa produk-produk ini merupakan rekomendasi yang baik untuk pertanyaan pelanggan. Fokuskan pada:
                - Bagaimana produk-produk ini sesuai dengan kebutuhan spesifik mereka
                - Manfaat dan fitur utama yang relevan
                - Promosi terkini yang mungkin berlaku
                - Proposisi nilai untuk penggunaan bisnis/profesional
                """
            else:
                prompt = f"""
                Customer Query: "{query}"
                
                {product_info}
                
                As a TechPro Solutions customer service representative, provide a brief explanation (2-3 sentences) 
                of why these products are good recommendations for this customer's query. Focus on:
                - How the products match their specific needs
                - Key benefits and features that are relevant
                - Any current promotions that might apply
                - Value proposition for business/professional use
                """
            
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating reasoning: {e}")
            # Fallback response in both languages
            return "These products were selected based on their relevance to your query and our expertise in matching technology solutions to professional needs. / Produk-produk ini dipilih berdasarkan relevansinya dengan pertanyaan Anda dan keahlian kami dalam mencocokkan solusi teknologi dengan kebutuhan profesional."

    def get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """Get conversation history"""
        history = self.conversations.get(conversation_id, [])
        # Filter out system messages for cleaner display
        return [msg for msg in history if msg.role != "system"]

    def get_conversation_summary(self, conversation_id: str) -> str:
        """Get a summary of the conversation for context"""
        history = self.get_conversation_history(conversation_id)
        if not history:
            return "No conversation history."
        
        summary_parts = []
        for msg in history[-6:]:  # Last 6 messages for context
            role_emoji = "👤" if msg.role == "user" else "🤖"
            content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_parts.append(f"{role_emoji} {content_preview}")
        
        return "\n".join(summary_parts)

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def get_active_conversations_count(self) -> int:
        """Get count of active conversations"""
        return len(self.conversations) 
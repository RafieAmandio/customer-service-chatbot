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
        
        # Enhanced system prompt with business context
        self.system_prompt = """
        You are a helpful customer service chatbot for TechPro Solutions, a premium technology retailer specializing in business and professional equipment.

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

        Always be honest about product availability and limitations.
        Keep responses informative but conversational.
        """

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
            
            # Search for relevant products based on the current message
            relevant_products = self.vector_store.search_products(request.message, limit=5)
            
            # Prepare context with product information
            product_context = self._prepare_product_context(relevant_products)
            
            # Generate response using OpenAI with full conversation context
            response_content = await self._generate_response(
                conversation_id, 
                product_context,
                request.message
            )
            
            # Add assistant response to conversation
            assistant_message = ChatMessage(
                role="assistant", 
                content=response_content, 
                timestamp=datetime.now()
            )
            self.conversations[conversation_id].append(assistant_message)
            
            # Extract suggested products (top 3 most relevant)
            suggested_products = [item["product"] for item in relevant_products[:3]] if relevant_products else []
            
            # Calculate confidence score based on product relevance
            confidence_score = self._calculate_confidence(relevant_products)
            
            return ChatResponse(
                response=response_content,
                conversation_id=conversation_id,
                suggested_products=suggested_products if suggested_products else None,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            print(f"Error in chat service: {e}")
            return ChatResponse(
                response="I'm sorry, I'm having trouble processing your request right now. Please try again.",
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

    async def _generate_response(self, conversation_id: str, product_context: str, current_message: str) -> str:
        """Generate response using OpenAI with full conversation context"""
        try:
            # Prepare messages for OpenAI - include full conversation history
            messages = []
            conversation_history = self.conversations[conversation_id]
            
            # Add all conversation messages
            for msg in conversation_history:
                messages.append({"role": msg.role, "content": msg.content})
            
            # Add product context if available and relevant
            if product_context and product_context != "No specific products found for this query.":
                context_message = f"""
                Product Information for current query "{current_message}":
                {product_context}
                
                Use this product information to help answer the customer's question. Remember to:
                - Reference their conversation history when relevant
                - Suggest products that match their stated needs and preferences
                - Mention current promotions when appropriate
                - Ask follow-up questions to better understand their requirements
                """
                messages.append({
                    "role": "system", 
                    "content": context_message
                })
            
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating OpenAI response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try rephrasing your question."

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
        """Generate reasoning for product recommendations"""
        try:
            product_info = self._prepare_product_context(relevant_products)
            
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
            return "These products were selected based on their relevance to your query and our expertise in matching technology solutions to professional needs."

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
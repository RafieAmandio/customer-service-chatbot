#!/usr/bin/env python3
"""
WebSocket Client Example for Multi-Brand Chatbot API

This example demonstrates how to connect to the WebSocket endpoint
and have a streaming conversation with a specific brand's chatbot.
"""

import asyncio
import websockets
import json
from datetime import datetime

async def chat_with_brand(brand_id: str = "techpro", server_url: str = "ws://localhost:8000"):
    """
    Connect to the WebSocket chat endpoint and have a conversation
    """
    uri = f"{server_url}/ws/chat/{brand_id}"
    
    print(f"🔗 Connecting to {brand_id} chatbot at {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Listen for welcome message
            welcome_data = await websocket.recv()
            welcome_msg = json.loads(welcome_data)
            
            if welcome_msg.get("type") == "welcome":
                print(f"🤖 {welcome_msg['data']['message']}")
                print(f"   Brand: {welcome_msg['data']['brand_name']} (ID: {welcome_msg['data']['brand_id']})")
            
            print("\n💬 You can start chatting! Type 'quit' to exit.\n")
            
            conversation_id = None
            
            # Start the conversation loop
            while True:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Send chat message
                chat_message = {
                    "type": "chat",
                    "data": {
                        "message": user_input,
                        "conversation_id": conversation_id,
                        "voice": False  # Set to True for voice-optimized responses
                    }
                }
                
                await websocket.send(json.dumps(chat_message))
                
                # Receive streaming response
                print("🤖 ", end="", flush=True)
                full_response = ""
                
                while True:
                    try:
                        response_data = await websocket.recv()
                        response_msg = json.loads(response_data)
                        
                        if response_msg.get("type") == "chunk":
                            chunk_data = response_msg.get("data", {})
                            content = chunk_data.get("content", "")
                            full_response += content
                            print(content, end="", flush=True)
                            
                            # Save conversation ID from first chunk
                            if not conversation_id:
                                conversation_id = chunk_data.get("conversation_id")
                        
                        elif response_msg.get("type") == "complete":
                            chunk_data = response_msg.get("data", {})
                            
                            # Show suggested products if any
                            suggested_products = chunk_data.get("suggested_products")
                            if suggested_products:
                                print(f"\n\n📦 Suggested Products:")
                                for i, product in enumerate(suggested_products[:3], 1):
                                    print(f"   {i}. {product['name']} - ${product['price']:,.2f}")
                                    print(f"      {product['description'][:100]}...")
                            
                            # Show confidence score
                            confidence = chunk_data.get("confidence_score")
                            if confidence:
                                print(f"\n🎯 Match Confidence: {confidence:.1%}")
                            
                            print("\n")  # New line after complete response
                            break
                        
                        elif response_msg.get("type") == "error":
                            error_msg = response_msg.get("data", {}).get("message", "Unknown error")
                            print(f"\n❌ Error: {error_msg}\n")
                            break
                            
                    except websockets.exceptions.ConnectionClosed:
                        print("\n🔌 Connection closed by server")
                        return
                    except json.JSONDecodeError:
                        print("\n⚠️ Received invalid JSON response")
                        continue
    
    except websockets.exceptions.ConnectionRefused:
        print(f"❌ Connection refused. Make sure the server is running at {server_url}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def list_available_brands(server_url: str = "http://localhost:8000"):
    """
    List all available brands (requires httpx for HTTP requests)
    """
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{server_url}/brands/active")
            if response.status_code == 200:
                brands = response.json()
                print("🏢 Available Brands:")
                for brand in brands:
                    print(f"   - {brand['name']} (ID: {brand['id']})")
                    print(f"     {brand['description']}")
                return brands
            else:
                print(f"❌ Failed to fetch brands: {response.status_code}")
                return []
    except ImportError:
        print("⚠️ httpx not available. Install with: pip install httpx")
        return []
    except Exception as e:
        print(f"❌ Error fetching brands: {e}")
        return []

async def test_multiple_brands():
    """
    Test chatting with multiple brands
    """
    print("🧪 Testing Multiple Brand Chat")
    print("=" * 50)
    
    # List available brands
    brands = await list_available_brands()
    
    if not brands:
        print("Using default TechPro brand...")
        brands = [{"id": "techpro", "name": "TechPro Solutions"}]
    
    for brand in brands[:2]:  # Test first 2 brands
        print(f"\n🔄 Testing {brand['name']} (ID: {brand['id']})")
        print("-" * 30)
        
        try:
            uri = f"ws://localhost:8000/ws/chat/{brand['id']}"
            
            async with websockets.connect(uri) as websocket:
                # Send a test message
                test_message = {
                    "type": "chat",
                    "data": {
                        "message": "Hello! Can you tell me about your company?",
                        "voice": False
                    }
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Collect response
                full_response = ""
                while True:
                    response_data = await websocket.recv()
                    response_msg = json.loads(response_data)
                    
                    if response_msg.get("type") == "chunk":
                        content = response_msg.get("data", {}).get("content", "")
                        full_response += content
                    elif response_msg.get("type") == "complete":
                        break
                
                print(f"🤖 Response: {full_response[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing {brand['name']}: {e}")

async def main():
    """
    Main function - choose what to run
    """
    print("🚀 WebSocket Client for Multi-Brand Chatbot API")
    print("=" * 50)
    
    # Uncomment the function you want to run:
    
    # 1. Interactive chat with default brand
    await chat_with_brand("techpro")
    
    # 2. Interactive chat with specific brand
    # await chat_with_brand("your_brand_id")
    
    # 3. Test multiple brands automatically
    # await test_multiple_brands()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}") 
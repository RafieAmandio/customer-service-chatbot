#!/usr/bin/env python3
"""
WebSocket Streaming Test Script
This script demonstrates how to connect to the WebSocket endpoint and receive streaming responses.
"""

import asyncio
import websockets
import json
from datetime import datetime

class WebSocketTester:
    def __init__(self, brand_id="techpro"):
        self.brand_id = brand_id
        self.url = f"ws://localhost:8000/ws/chat/{brand_id}"
        self.conversation_id = None
        
    async def connect_and_test(self):
        print(f"🔌 Connecting to WebSocket: {self.url}")
        
        try:
            async with websockets.connect(self.url) as websocket:
                print("✅ Connected successfully!")
                
                # Listen for welcome message
                await self.listen_for_welcome(websocket)
                
                # Test streaming with different types of messages
                test_messages = [
                    "Tell me about your company",
                    "I need a laptop for business work under $25 million rupiah",
                    "What's the cheapest MacBook you have?",
                    "Compare Dell vs HP laptops"
                ]
                
                for i, message in enumerate(test_messages, 1):
                    print(f"\n{'='*60}")
                    print(f"🧪 Test {i}: {message}")
                    print(f"{'='*60}")
                    await self.send_message_and_stream(websocket, message)
                    
                    # Wait between tests
                    await asyncio.sleep(2)
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")
            
    async def listen_for_welcome(self, websocket):
        print("👂 Listening for welcome message...")
        try:
            welcome_msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            welcome_data = json.loads(welcome_msg)
            
            if welcome_data.get("type") == "welcome":
                print(f"👋 Welcome: {welcome_data['data']['message']}")
                print(f"🏢 Brand: {welcome_data['data']['brand_name']} (ID: {welcome_data['data']['brand_id']})")
            else:
                print(f"⚠️ Unexpected message type: {welcome_data.get('type')}")
                
        except asyncio.TimeoutError:
            print("⏰ Timeout waiting for welcome message")
        except Exception as e:
            print(f"❌ Error receiving welcome: {e}")
    
    async def send_message_and_stream(self, websocket, message):
        # Send chat message
        chat_message = {
            "type": "chat",
            "data": {
                "message": message,
                "conversation_id": self.conversation_id,
                "voice": False
            }
        }
        
        print(f"📤 Sending: {json.dumps(chat_message, indent=2)}")
        await websocket.send(json.dumps(chat_message))
        
        # Collect streaming response
        full_response = ""
        chunk_count = 0
        start_time = datetime.now()
        
        print("📥 Receiving streaming response:")
        print("-" * 40)
        
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                data = json.loads(response)
                
                if data.get("type") == "chunk":
                    chunk_data = data.get("data", {})
                    chunk_content = chunk_data.get("content", "")
                    full_response += chunk_content
                    chunk_count += 1
                    
                    # Update conversation ID
                    if chunk_data.get("conversation_id"):
                        self.conversation_id = chunk_data["conversation_id"]
                    
                    # Print chunk with visual indicator
                    print(f"📄 Chunk {chunk_count}: '{chunk_content}'")
                    print(f"   Current message: '{full_response}'")
                    
                elif data.get("type") == "complete":
                    complete_data = data.get("data", {})
                    
                    # Update conversation ID
                    if complete_data.get("conversation_id"):
                        self.conversation_id = complete_data["conversation_id"]
                    
                    # Get final data
                    suggested_products = complete_data.get("suggested_products", [])
                    confidence_score = complete_data.get("confidence_score")
                    
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    print("-" * 40)
                    print(f"✅ Complete response received!")
                    print(f"📊 Statistics:")
                    print(f"   - Chunks received: {chunk_count}")
                    print(f"   - Total characters: {len(full_response)}")
                    print(f"   - Duration: {duration:.2f} seconds")
                    print(f"   - Conversation ID: {self.conversation_id}")
                    
                    print(f"\n💬 Full Response:")
                    print(f"'{full_response}'")
                    
                    if suggested_products:
                        print(f"\n🛍️ Suggested Products ({len(suggested_products)}):")
                        for i, product in enumerate(suggested_products, 1):
                            print(f"   {i}. {product['name']} - ${product['price']:,.2f}")
                            print(f"      Category: {product['category']}")
                            print(f"      Description: {product['description'][:100]}...")
                    
                    if confidence_score is not None:
                        print(f"\n🎯 Confidence Score: {confidence_score:.2f} ({confidence_score*100:.1f}%)")
                    
                    break
                    
                elif data.get("type") == "error":
                    error_msg = data.get("data", {}).get("message", "Unknown error")
                    print(f"❌ Error: {error_msg}")
                    break
                    
                else:
                    print(f"⚠️ Unknown message type: {data.get('type')}")
                    print(f"   Data: {json.dumps(data, indent=2)}")
                    
            except asyncio.TimeoutError:
                print("⏰ Timeout waiting for response")
                break
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                break
            except Exception as e:
                print(f"❌ Error receiving message: {e}")
                break

async def test_voice_optimization():
    """Test voice-optimized responses"""
    print(f"\n{'='*60}")
    print("🗣️ Testing Voice-Optimized Responses")
    print(f"{'='*60}")
    
    tester = WebSocketTester()
    
    try:
        async with websockets.connect(tester.url) as websocket:
            # Wait for welcome
            await tester.listen_for_welcome(websocket)
            
            # Test voice message
            voice_message = {
                "type": "chat",
                "data": {
                    "message": "What's your cheapest laptop?",
                    "voice": True  # Voice optimization enabled
                }
            }
            
            print(f"📤 Sending voice message: {json.dumps(voice_message, indent=2)}")
            await websocket.send(json.dumps(voice_message))
            
            # Listen for response
            response_text = ""
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                data = json.loads(response)
                
                if data.get("type") == "chunk":
                    response_text += data.get("data", {}).get("content", "")
                elif data.get("type") == "complete":
                    print(f"🗣️ Voice Response: '{response_text}'")
                    print(f"📏 Length: {len(response_text)} characters")
                    
                    # Count sentences
                    import re
                    sentences = re.split(r'[.!?]+', response_text.strip())
                    sentence_count = len([s for s in sentences if s.strip()])
                    print(f"📝 Sentences: {sentence_count}")
                    break
                elif data.get("type") == "error":
                    print(f"❌ Error: {data.get('data', {}).get('message')}")
                    break
                    
    except Exception as e:
        print(f"❌ Voice test error: {e}")

async def test_connection_scenarios():
    """Test different connection scenarios"""
    print(f"\n{'='*60}")
    print("🔍 Testing Connection Scenarios")
    print(f"{'='*60}")
    
    # Test invalid brand
    print("🧪 Testing invalid brand...")
    try:
        async with websockets.connect("ws://localhost:8000/ws/chat/invalid-brand") as websocket:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            if data.get("type") == "error":
                print(f"✅ Correctly received error: {data['data']['message']}")
            else:
                print(f"⚠️ Unexpected response: {data}")
    except Exception as e:
        print(f"❌ Connection to invalid brand failed as expected: {e}")
    
    # Test ping/pong
    print("\n🏓 Testing ping/pong...")
    try:
        async with websockets.connect("ws://localhost:8000/ws/chat/techpro") as websocket:
            # Send ping
            ping_msg = {"type": "ping", "data": {}}
            await websocket.send(json.dumps(ping_msg))
            
            # Wait for pong
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            if data.get("type") == "pong":
                print(f"✅ Received pong: {data['data']['timestamp']}")
            else:
                print(f"⚠️ Expected pong, got: {data}")
                
    except Exception as e:
        print(f"❌ Ping/pong test failed: {e}")

async def main():
    print("🚀 WebSocket Streaming Test Suite")
    print("=" * 60)
    
    # Main streaming tests
    tester = WebSocketTester()
    await tester.connect_and_test()
    
    # Voice optimization test
    await test_voice_optimization()
    
    # Connection scenario tests
    await test_connection_scenarios()
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print("💡 Use this as a reference for your frontend implementation.")
    print("📖 Check WEBSOCKET_DOCUMENTATION.md for detailed examples.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}") 
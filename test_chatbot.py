#!/usr/bin/env python3
"""
Test script to demonstrate the Customer Service Chatbot capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def send_message(message, conversation_id=None, voice=False):
    """Send a message to the chatbot and return the response"""
    data = {"message": message, "voice": voice}
    if conversation_id:
        data["conversation_id"] = conversation_id
    
    response = requests.post(f"{BASE_URL}/chat", json=data)
    return response.json()

def print_chat_response(response, query_num, is_voice=False):
    """Pretty print the chat response"""
    print(f"\n{'='*60}")
    voice_indicator = " (VOICE)" if is_voice else ""
    print(f"Query {query_num}{voice_indicator}: {response.get('response', 'No response')}")
    
    if response.get('suggested_products'):
        print(f"\n📦 Produk yang Disarankan ({len(response['suggested_products'])}):")
        for i, product in enumerate(response['suggested_products'], 1):
            # Format price in Rupiah
            price_formatted = f"Rp {product['price']:,.0f}".replace(',', '.')
            print(f"  {i}. {product['name']} - {price_formatted}")
    
    if response.get('confidence_score'):
        print(f"\n🎯 Confidence Score: {response['confidence_score']:.2f}")
    
    return response.get('conversation_id')

def main():
    print("🤖 Customer Service Chatbot Demo - Indonesian Edition")
    print("📋 Testing various capabilities including voice responses...")
    print("\n" + "="*60)
    
    # Test queries in both Indonesian and English
    test_queries = [
        # Business information - Indonesian
        {
            "message": "Ceritakan tentang perusahaan kalian",
            "description": "Testing business knowledge in Indonesian",
            "voice": False
        },
        
        # Product search - Indonesian
        {
            "message": "Saya butuh laptop untuk kerja bisnis di bawah 25 juta",
            "description": "Testing product search with budget in Indonesian",
            "voice": False
        },
        
        # Voice response test - Indonesian
        {
            "message": "Rekomendasikan laptop gaming yang bagus",
            "description": "Testing voice response in Indonesian",
            "voice": True
        },
        
        # Specific brand preference with conversation context
        {
            "message": "Sebenarnya saya lebih suka MacBook. Apa yang kalian punya?",
            "description": "Testing conversation memory and brand filtering in Indonesian",
            "voice": False
        },
        
        # Voice response for specs - should be short
        {
            "message": "Berapa harga MacBook Pro?",
            "description": "Testing voice response for price inquiry",
            "voice": True
        },
        
        # Technical specifications - Indonesian
        {
            "message": "Apa spesifikasi lengkap MacBook Pro?",
            "description": "Testing detailed product information in Indonesian",
            "voice": False
        },
        
        # Comparison request - Indonesian
        {
            "message": "Tolong bandingkan laptop Dell XPS dengan ThinkPad",
            "description": "Testing product comparison in Indonesian",
            "voice": False
        },
        
        # Promotions and services - Indonesian
        {
            "message": "Apa promosi yang tersedia untuk pelanggan bisnis?",
            "description": "Testing promotion knowledge in Indonesian",
            "voice": False
        },
        
        # English voice test
        {
            "message": "What's the best laptop for video editing?",
            "description": "Testing voice response in English",
            "voice": True
        },
        
        # Accessories - Indonesian
        {
            "message": "Aksesoris apa yang cocok dengan MacBook?",
            "description": "Testing accessory recommendations in Indonesian",
            "voice": False
        }
    ]
    
    conversation_id = None
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query['description']}")
        print(f"💬 User: {query['message']}")
        if query.get('voice'):
            print("🎤 Voice Response Mode: ON")
        print("-" * 60)
        
        try:
            response = send_message(query['message'], conversation_id, query.get('voice', False))
            conversation_id = print_chat_response(response, i, query.get('voice', False))
            
            # Small delay to be nice to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test file upload functionality
    print(f"\n{'='*60}")
    print("📁 Testing File Upload Feature")
    print("-" * 60)
    
    try:
        # Check uploads endpoint
        uploads_response = requests.get(f"{BASE_URL}/uploads")
        if uploads_response.status_code == 200:
            uploads = uploads_response.json()
            print(f"✅ Uploads endpoint working - Found {len(uploads)} uploaded files")
        else:
            print(f"❌ Uploads endpoint error: {uploads_response.status_code}")
    except Exception as e:
        print(f"❌ Upload test error: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Demo completed!")
    print(f"💬 Conversation ID: {conversation_id}")
    print(f"🌐 API Documentation: {BASE_URL}/docs")
    print(f"📊 API Stats: {BASE_URL}/stats")
    print(f"📁 File Uploads: {BASE_URL}/uploads")

if __name__ == "__main__":
    main() 
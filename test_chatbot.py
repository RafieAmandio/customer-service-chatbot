#!/usr/bin/env python3
"""
Test script to demonstrate the Customer Service Chatbot capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def send_message(message, conversation_id=None):
    """Send a message to the chatbot and return the response"""
    data = {"message": message}
    if conversation_id:
        data["conversation_id"] = conversation_id
    
    response = requests.post(f"{BASE_URL}/chat", json=data)
    return response.json()

def print_chat_response(response, query_num):
    """Pretty print the chat response"""
    print(f"\n{'='*60}")
    print(f"Query {query_num}: {response.get('response', 'No response')}")
    
    if response.get('suggested_products'):
        print(f"\n📦 Suggested Products ({len(response['suggested_products'])}):")
        for i, product in enumerate(response['suggested_products'], 1):
            print(f"  {i}. {product['name']} - ${product['price']:,.2f}")
    
    if response.get('confidence_score'):
        print(f"\n🎯 Confidence Score: {response['confidence_score']:.2f}")
    
    return response.get('conversation_id')

def main():
    print("🤖 Customer Service Chatbot Demo")
    print("📋 Testing various capabilities...")
    print("\n" + "="*60)
    
    # Test queries that demonstrate different capabilities
    test_queries = [
        # Business information
        {
            "message": "Tell me about your company",
            "description": "Testing business knowledge"
        },
        
        # Product search - laptops
        {
            "message": "I need a laptop for business work under $1500",
            "description": "Testing product search and budget filtering"
        },
        
        # Specific brand preference with conversation context
        {
            "message": "Actually, I prefer MacBooks. What do you have?",
            "description": "Testing conversation memory and brand filtering"
        },
        
        # Technical specifications
        {
            "message": "What are the specs of the MacBook Pro?",
            "description": "Testing detailed product information"
        },
        
        # Comparison request
        {
            "message": "Can you compare the Dell XPS and ThinkPad laptops?",
            "description": "Testing product comparison capabilities"
        },
        
        # Promotions and services
        {
            "message": "What promotions do you have for business customers?",
            "description": "Testing promotion knowledge"
        },
        
        # Gaming/Performance laptops
        {
            "message": "I need a powerful laptop for gaming and video editing",
            "description": "Testing performance-focused recommendations"
        },
        
        # Accessories
        {
            "message": "What accessories would go well with a MacBook?",
            "description": "Testing accessory recommendations"
        }
    ]
    
    conversation_id = None
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query['description']}")
        print(f"💬 User: {query['message']}")
        print("-" * 60)
        
        try:
            response = send_message(query['message'], conversation_id)
            conversation_id = print_chat_response(response, i)
            
            # Small delay to be nice to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Demo completed!")
    print(f"💬 Conversation ID: {conversation_id}")
    print(f"🌐 API Documentation: {BASE_URL}/docs")
    print(f"📊 API Stats: {BASE_URL}/stats")

if __name__ == "__main__":
    main() 
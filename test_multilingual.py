#!/usr/bin/env python3
"""
Test script for multilingual and smart recommendation functionality
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

def print_chat_response(response, query_num, query_description):
    """Pretty print the chat response"""
    print(f"\n{'='*80}")
    print(f"Test {query_num}: {query_description}")
    print(f"Response: {response.get('response', 'No response')}")
    
    has_products = response.get('suggested_products')
    if has_products:
        print(f"\n📦 Product Recommendations ({len(has_products)}):")
        for i, product in enumerate(has_products, 1):
            print(f"  {i}. {product['name']} - ${product['price']:,.2f}")
        print(f"\n🎯 Confidence Score: {response.get('confidence_score', 0):.2f}")
    else:
        print("\n✅ No product recommendations (as expected for general queries)")
    
    return response.get('conversation_id')

def main():
    print("🧪 Testing Multilingual Smart Recommendation System")
    print("="*80)
    print("Testing both English and Indonesian queries")
    print("Only product-related queries should return recommendations")
    
    # Test scenarios - mix of product and non-product queries in both languages
    test_queries = [
        # English - General queries (should NOT return products)
        {
            "message": "Hello, tell me about your company",
            "description": "[EN] Company info query - NO products expected",
            "expect_products": False
        },
        
        # English - Product queries (should return products)
        {
            "message": "I need a laptop for business work under $1500",
            "description": "[EN] Product search - products expected",
            "expect_products": True
        },
        
        # Indonesian - General queries (should NOT return products)
        {
            "message": "Halo, ceritakan tentang perusahaan kalian",
            "description": "[ID] Company info query - NO products expected",
            "expect_products": False
        },
        
        # Indonesian - Product queries (should return products)
        {
            "message": "Saya butuh laptop untuk kerja bisnis dengan budget 20 juta",
            "description": "[ID] Product search - products expected",
            "expect_products": True
        },
        
        # English - Promotion query (should NOT return products)
        {
            "message": "What promotions do you have for business customers?",
            "description": "[EN] Promotion inquiry - NO products expected",
            "expect_products": False
        },
        
        # Indonesian - Specific product question (should return products)
        {
            "message": "Apa perbedaan antara MacBook Pro dan MacBook Air?",
            "description": "[ID] Product comparison - products expected",
            "expect_products": True
        },
        
        # English - Support question (should NOT return products)
        {
            "message": "What's your warranty policy?",
            "description": "[EN] Policy question - NO products expected",
            "expect_products": False
        },
        
        # Indonesian - Product specification (should return products)
        {
            "message": "Spesifikasi laptop gaming apa yang tersedia?",
            "description": "[ID] Gaming laptop specs - products expected",
            "expect_products": True
        },
        
        # Mixed conversation - following up on previous product question
        {
            "message": "Can you tell me more about the ASUS ROG?",
            "description": "[EN] Follow-up product question - products expected",
            "expect_products": True
        },
        
        # Indonesian - General thank you (should NOT return products)
        {
            "message": "Terima kasih atas informasinya",
            "description": "[ID] Thank you message - NO products expected",
            "expect_products": False
        }
    ]
    
    conversation_id = None
    correct_predictions = 0
    total_tests = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}/10: {query['description']}")
        print(f"💬 User: {query['message']}")
        print("-" * 80)
        
        try:
            response = send_message(query['message'], conversation_id)
            conversation_id = print_chat_response(response, i, query['description'])
            
            # Check if prediction is correct
            has_products = bool(response.get('suggested_products'))
            expected_products = query['expect_products']
            
            if has_products == expected_products:
                print(f"✅ CORRECT: Expected products={expected_products}, Got products={has_products}")
                correct_predictions += 1
            else:
                print(f"❌ INCORRECT: Expected products={expected_products}, Got products={has_products}")
            
            # Small delay to be nice to the API
            time.sleep(1.5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*80}")
    print("📊 TEST RESULTS")
    print(f"✅ Correct predictions: {correct_predictions}/{total_tests}")
    print(f"📈 Accuracy: {(correct_predictions/total_tests)*100:.1f}%")
    print(f"💬 Conversation ID: {conversation_id}")
    
    if correct_predictions == total_tests:
        print("🎉 Perfect! All tests passed!")
    elif correct_predictions >= total_tests * 0.8:
        print("🎯 Good! Most tests passed!")
    else:
        print("⚠️  Some tests failed. Check the logic.")
    
    print(f"\n🌐 API Documentation: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 
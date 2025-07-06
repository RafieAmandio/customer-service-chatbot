#!/usr/bin/env python3
"""
Test script to verify persona_prompt functionality
"""

import json
from models import BrandConfig, BrandConfigUpdateRequest
from brand_service import BrandService
from chatbot_service import ChatbotService
from datetime import datetime

def test_persona_prompt():
    """Test the persona_prompt functionality"""
    print("Testing persona_prompt functionality...")
    
    # Test 1: Create a brand config with persona_prompt
    test_config = BrandConfig(
        brand_id="test",
        system_prompt="You are a helpful customer service chatbot.",
        persona_prompt="You should be enthusiastic, friendly, and use emojis occasionally. Always end responses with a positive note.",
        welcome_message="Hello! Welcome to our store!",
        company_info={"name": "Test Company"},
        appearance_settings={"primary_color": "#007bff"},
        updated_at=datetime.now()
    )
    
    print("✅ BrandConfig with persona_prompt created successfully")
    
    # Test 2: Test ChatbotService with persona_prompt
    chatbot = ChatbotService(brand_id="test", brand_config=test_config)
    
    print("System prompt with persona:")
    print(chatbot.system_prompt)
    print()
    
    # Test 3: Test BrandConfigUpdateRequest
    update_request = BrandConfigUpdateRequest(
        system_prompt="Updated system prompt",
        persona_prompt="Updated persona: Be more professional and concise.",
        welcome_message="Updated welcome message"
    )
    
    print("✅ BrandConfigUpdateRequest with persona_prompt created successfully")
    print(f"Update request persona_prompt: {update_request.persona_prompt}")
    
    # Test 4: Test without persona_prompt (should work with None)
    config_without_persona = BrandConfig(
        brand_id="test2",
        system_prompt="You are a helpful customer service chatbot.",
        welcome_message="Hello!",
        company_info={"name": "Test Company 2"},
        appearance_settings={"primary_color": "#007bff"},
        updated_at=datetime.now()
    )
    
    chatbot_without_persona = ChatbotService(brand_id="test2", brand_config=config_without_persona)
    
    print("System prompt without persona:")
    print(chatbot_without_persona.system_prompt)
    print()
    
    print("✅ All persona_prompt tests passed!")

if __name__ == "__main__":
    test_persona_prompt()
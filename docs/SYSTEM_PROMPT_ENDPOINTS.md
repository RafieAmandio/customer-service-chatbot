# System Prompt Management Endpoints

## Overview

These endpoints allow you to manage the system prompt for specific brand chatbots. The system prompt defines the AI's personality, role, and behavior instructions.

## Endpoints

### Get System Prompt

#### `GET /brands/{brand_id}/system-prompt`

**Description:** Retrieve the current system prompt for a specific brand's chatbot.

**Parameters:**
- `brand_id` (path): The brand identifier

**Response:**
```json
{
  "brand_id": "techpro",
  "brand_name": "TechPro Solutions",
  "system_prompt": "You are a friendly AI assistant for TechPro Solutions...",
  "updated_at": "2025-06-12T21:38:53.857510"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands/techpro/system-prompt"
```

### Update System Prompt

#### `PUT /brands/{brand_id}/system-prompt`

**Description:** Update the system prompt for a specific brand's chatbot. This will force refresh the chatbot instance to use the new prompt immediately.

**Parameters:**
- `brand_id` (path): The brand identifier

**Request Body:**
```json
{
  "system_prompt": "Your new system prompt here..."
}
```

**Response:**
```json
{
  "message": "System prompt updated successfully",
  "brand_id": "techpro",
  "brand_name": "TechPro Solutions",
  "system_prompt": "Your new system prompt here...",
  "updated_at": "2025-06-12T21:38:53.857510"
}
```

**Example:**
```bash
curl -X PUT "http://localhost:8000/brands/techpro/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a helpful AI assistant for TechPro Solutions. Always be professional and provide detailed product recommendations."
  }'
```

## Error Responses

### Brand Not Found (404)
```json
{
  "detail": "Brand not found"
}
```

### Invalid Request (422)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "system_prompt"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

## Features

✅ **Immediate Effect**: Changes take effect immediately by refreshing the chatbot instance  
✅ **Brand Isolation**: Each brand has its own independent system prompt  
✅ **Validation**: Ensures brand exists before updating  
✅ **Error Handling**: Proper HTTP status codes and error messages  
✅ **Timestamps**: Tracks when the system prompt was last updated  

## Use Cases

### 1. Changing Chatbot Personality
```bash
# Make the chatbot more formal
curl -X PUT "http://localhost:8000/brands/techpro/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a professional customer service representative for TechPro Solutions. Maintain a formal tone and provide accurate technical information."
  }'
```

### 2. Adding New Instructions
```bash
# Add voice optimization instructions
curl -X PUT "http://localhost:8000/brands/techpro/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a friendly AI assistant for TechPro Solutions. When voice=true, respond with maximum 1 sentence. Always be helpful and provide detailed product recommendations."
  }'
```

### 3. Brand-Specific Customization
```bash
# Customize for a luxury brand
curl -X PUT "http://localhost:8000/brands/luxury-tech/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are an exclusive concierge for Luxury Tech Solutions. Provide premium service with sophistication and attention to detail. Our clients expect the finest technology products and white-glove service."
  }'
```

## Integration Notes

- **WebSocket Connections**: Existing WebSocket connections will continue using the old prompt until they reconnect
- **REST API**: New chat requests will immediately use the updated prompt
- **Persistence**: System prompts are automatically saved and persist across server restarts
- **No Downtime**: Updates happen without interrupting the service

## Best Practices

1. **Clear Instructions**: Be specific about the chatbot's role and behavior
2. **Language Support**: Include multilingual instructions if needed
3. **Brand Voice**: Ensure the prompt reflects your brand's personality
4. **Product Context**: Include relevant information about your products/services
5. **Testing**: Test the updated prompt with sample conversations

This provides full control over your chatbot's behavior while maintaining the existing API structure! 
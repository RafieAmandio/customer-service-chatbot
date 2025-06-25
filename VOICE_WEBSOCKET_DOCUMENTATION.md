# Voice-Optimized WebSocket Chat Documentation

## Overview

The `/ws/voice/{brand_id}` WebSocket endpoint provides real-time streaming chat functionality with **voice-optimized responses**. Every message sent through this endpoint will receive a response that is concise, direct, and limited to a single sentence—ideal for text-to-speech (TTS) or voice assistant integrations.

---

## Endpoint

```
ws://localhost:8000/ws/voice/{brand_id}
```

- `brand_id` (required): The ID of the brand you want to chat with (e.g., `techpro`)

---

## Connection Flow

1. **Connect** to the WebSocket endpoint with a specific brand ID
2. **Receive** a welcome message from the brand
3. **Send** chat messages (no need to set `voice: true`)
4. **Receive** streaming, voice-optimized responses
5. **Handle** chunks, final responses, and suggested products
6. **Disconnect** when conversation is complete

---

## Message Format

### Client → Server Messages

#### 1. Chat Message
```json
{
  "type": "chat",
  "data": {
    "message": "What is your cheapest laptop?",
    "conversation_id": "optional-conversation-id",
    "user_id": "optional-user-id"
  }
}
```
- `type`: Always `"chat"` for chat messages
- `data.message` (required): The user's message
- `data.conversation_id` (optional): Continue existing conversation
- `data.user_id` (optional): User identifier for tracking

> **Note:** You do **not** need to set `voice: true`—it is always enabled on this endpoint.

#### 2. Ping Message
```json
{
  "type": "ping",
  "data": {}
}
```

---

### Server → Client Messages

#### 1. Welcome Message
```json
{
  "type": "welcome",
  "data": {
    "message": "Welcome to TechPro Solutions! How can I help you today?",
    "brand_id": "techpro",
    "brand_name": "TechPro Solutions"
  }
}
```

#### 2. Response Chunk
```json
{
  "type": "chunk",
  "data": {
    "content": "Our cheapest laptop is the Dell Inspiron 14.",
    "is_final": false,
    "conversation_id": "conv-123456789",
    "suggested_products": null,
    "confidence_score": null
  }
}
```

#### 3. Complete Response
```json
{
  "type": "complete",
  "data": {
    "content": "",
    "is_final": true,
    "conversation_id": "conv-123456789",
    "suggested_products": [
      {
        "id": "laptop-002",
        "name": "Dell Inspiron 14",
        "description": "Affordable business laptop...",
        "category": "Laptop",
        "price": 499.99,
        "features": ["Intel Core i3", "8GB RAM"],
        "specifications": {"RAM": "8GB", "Storage": "256GB SSD"},
        "availability": true,
        "brand_id": "techpro"
      }
    ],
    "confidence_score": 0.92
  }
}
```

#### 4. Error Message
```json
{
  "type": "error",
  "data": {
    "message": "Brand 'invalid-brand' not found or inactive"
  }
}
```

#### 5. Pong Response
```json
{
  "type": "pong",
  "data": {
    "timestamp": "2024-01-20T10:30:00"
  }
}
```

---

## Voice-Optimized Response Characteristics
- **Maximum 1 sentence**
- **Concise and direct**
- **Natural for text-to-speech**
- **Same language detection** (English/Indonesian supported)

---

## Example Python Client

```python
import asyncio
import websockets
import json

async def voice_chat_example():
    uri = "ws://localhost:8000/ws/voice/techpro"
    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(json.loads(welcome))

        # Send a chat message
        message = {
            "type": "chat",
            "data": {
                "message": "What is your cheapest laptop?"
            }
        }
        await websocket.send(json.dumps(message))

        # Receive streaming response
        full_response = ""
        while True:
            data = await websocket.recv()
            msg = json.loads(data)
            if msg["type"] == "chunk":
                content = msg["data"]["content"]
                full_response += content
                print(content, end="", flush=True)
            elif msg["type"] == "complete":
                print("\nSuggested products:", msg["data"]["suggested_products"])
                break

asyncio.run(voice_chat_example())
```

---

## Notes
- Use this endpoint for any voice assistant or TTS integration.
- For regular chat (not voice-optimized), use `/ws/chat/{brand_id}` instead. 
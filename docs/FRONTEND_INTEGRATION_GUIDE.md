# Frontend Integration Guide - WebSocket Streaming Chat

## Overview

This guide shows how to integrate the real-time streaming chat functionality into your frontend application. The WebSocket endpoint provides **live typing effects** where responses stream word-by-word as the AI generates them.

## Quick Start

### Connection URL
```
ws://localhost:8000/ws/chat/{brand_id}
```

### Basic Implementation

```javascript
const chatSocket = new WebSocket('ws://localhost:8000/ws/chat/techpro');
let currentResponse = '';

chatSocket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    
    if (message.type === 'chunk') {
        currentResponse += message.data.content;
        updateChatUI(currentResponse); // Update UI with streaming text
    } else if (message.type === 'complete') {
        displayProducts(message.data.suggested_products);
    }
};

// Send a message
function sendMessage(text) {
    chatSocket.send(JSON.stringify({
        type: 'chat',
        data: { message: text }
    }));
    currentResponse = ''; // Reset for new response
}
```

## React Implementation

### Custom Hook

```jsx
import { useState, useEffect, useRef } from 'react';

const useChatbot = (brandId = 'techpro') => {
    const [socket, setSocket] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [currentMessage, setCurrentMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [products, setProducts] = useState([]);
    const [conversationId, setConversationId] = useState(null);

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${brandId}`);
        
        ws.onopen = () => setIsConnected(true);
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            
            switch (message.type) {
                case 'welcome':
                    console.log('Connected to:', message.data.brand_name);
                    break;
                    
                case 'chunk':
                    setCurrentMessage(prev => prev + message.data.content);
                    setConversationId(message.data.conversation_id);
                    setIsTyping(true);
                    break;
                    
                case 'complete':
                    setIsTyping(false);
                    if (message.data.suggested_products) {
                        setProducts(message.data.suggested_products);
                    }
                    break;
                    
                case 'error':
                    console.error('Chat error:', message.data.message);
                    setIsTyping(false);
                    break;
            }
        };
        
        ws.onclose = () => setIsConnected(false);
        
        setSocket(ws);
        
        return () => ws.close();
    }, [brandId]);

    const sendMessage = (text, isVoice = false) => {
        if (!socket || !isConnected) return;
        
        setCurrentMessage('');
        setProducts([]);
        
        socket.send(JSON.stringify({
            type: 'chat',
            data: {
                message: text,
                conversation_id: conversationId,
                voice: isVoice
            }
        }));
    };

    return {
        isConnected,
        currentMessage,
        isTyping,
        products,
        sendMessage
    };
};
```

### Chat Component

```jsx
import React, { useState } from 'react';

const StreamingChat = () => {
    const [input, setInput] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const { 
        isConnected, 
        currentMessage, 
        isTyping, 
        products, 
        sendMessage 
    } = useChatbot('techpro');

    const handleSend = () => {
        if (!input.trim()) return;
        
        // Add user message to history
        setChatHistory(prev => [...prev, {
            role: 'user',
            content: input,
            timestamp: new Date()
        }]);
        
        sendMessage(input);
        setInput('');
    };

    // Add completed responses to history
    React.useEffect(() => {
        if (!isTyping && currentMessage) {
            setChatHistory(prev => [...prev, {
                role: 'assistant',
                content: currentMessage,
                products: products,
                timestamp: new Date()
            }]);
        }
    }, [isTyping, currentMessage, products]);

    return (
        <div className="chat-container">
            <div className="status">
                {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
            </div>
            
            <div className="messages">
                {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="content">{msg.content}</div>
                        {msg.products && (
                            <ProductList products={msg.products} />
                        )}
                    </div>
                ))}
                
                {/* Live streaming message */}
                {isTyping && (
                    <div className="message assistant streaming">
                        <div className="content">
                            {currentMessage}
                            <span className="cursor">▌</span>
                        </div>
                    </div>
                )}
            </div>
            
            <div className="input-area">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Type your message..."
                    disabled={!isConnected}
                />
                <button onClick={handleSend} disabled={!isConnected}>
                    Send
                </button>
            </div>
        </div>
    );
};

const ProductList = ({ products }) => (
    <div className="products">
        <h4>Recommended Products:</h4>
        {products.map(product => (
            <div key={product.id} className="product">
                <h5>{product.name}</h5>
                <p>Price: ${product.price.toLocaleString()}</p>
                <p>{product.description}</p>
            </div>
        ))}
    </div>
);
```

## Vue.js Implementation

```vue
<template>
  <div class="chat-app">
    <div class="status" :class="{ connected: isConnected }">
      {{ isConnected ? 'Connected' : 'Disconnected' }}
    </div>
    
    <div class="messages" ref="messagesContainer">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        :class="['message', message.role]"
      >
        {{ message.content }}
        <ProductGrid 
          v-if="message.products" 
          :products="message.products" 
        />
      </div>
      
      <!-- Live streaming -->
      <div v-if="isTyping" class="message assistant streaming">
        {{ currentMessage }}<span class="cursor">▌</span>
      </div>
    </div>
    
    <div class="input-container">
      <input
        v-model="inputText"
        @keyup.enter="sendMessage"
        :disabled="!isConnected"
        placeholder="Type your message..."
      />
      <button @click="sendMessage" :disabled="!isConnected">
        Send
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      isConnected: false,
      currentMessage: '',
      isTyping: false,
      messages: [],
      inputText: '',
      conversationId: null
    }
  },
  
  mounted() {
    this.connect();
  },
  
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
  
  methods: {
    connect() {
      this.socket = new WebSocket('ws://localhost:8000/ws/chat/techpro');
      
      this.socket.onopen = () => {
        this.isConnected = true;
      };
      
      this.socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      };
      
      this.socket.onclose = () => {
        this.isConnected = false;
        this.isTyping = false;
      };
    },
    
    handleMessage(message) {
      switch (message.type) {
        case 'chunk':
          this.currentMessage += message.data.content;
          this.conversationId = message.data.conversation_id;
          this.isTyping = true;
          break;
          
        case 'complete':
          this.isTyping = false;
          this.messages.push({
            role: 'assistant',
            content: this.currentMessage,
            products: message.data.suggested_products || []
          });
          this.currentMessage = '';
          this.scrollToBottom();
          break;
          
        case 'error':
          this.isTyping = false;
          console.error('Chat error:', message.data.message);
          break;
      }
    },
    
    sendMessage() {
      if (!this.inputText.trim() || !this.isConnected) return;
      
      // Add user message
      this.messages.push({
        role: 'user',
        content: this.inputText
      });
      
      // Send to server
      this.socket.send(JSON.stringify({
        type: 'chat',
        data: {
          message: this.inputText,
          conversation_id: this.conversationId
        }
      }));
      
      this.inputText = '';
      this.currentMessage = '';
      this.scrollToBottom();
    },
    
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        container.scrollTop = container.scrollHeight;
      });
    }
  }
}
</script>

<style scoped>
.chat-app {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.status {
  padding: 10px;
  background: #f8d7da;
  color: #721c24;
  text-align: center;
  font-weight: bold;
}

.status.connected {
  background: #d4edda;
  color: #155724;
}

.messages {
  height: 400px;
  overflow-y: auto;
  padding: 15px;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background: #007bff;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background: #e9ecef;
  color: #333;
}

.message.streaming {
  background: #e3f2fd;
}

.cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.input-container {
  display: flex;
  padding: 15px;
  background: white;
  border-top: 1px solid #ddd;
}

.input-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-container button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-container button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}
</style>
```

## Vanilla JavaScript Implementation

```html
<!DOCTYPE html>
<html>
<head>
    <title>Streaming Chat</title>
    <style>
        .chat-container {
            max-width: 600px;
            margin: 50px auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .status {
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }
        
        .connected { background: #d4edda; color: #155724; }
        .disconnected { background: #f8d7da; color: #721c24; }
        
        .messages {
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            background: #f9f9f9;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .user { background: #007bff; color: white; margin-left: auto; }
        .assistant { background: #e9ecef; color: #333; }
        .streaming { background: #e3f2fd; }
        
        .cursor {
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .input-area {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #ddd;
        }
        
        .input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-right: 10px;
        }
        
        .input-area button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .products {
            margin-top: 10px;
            padding: 10px;
            background: #fff3cd;
            border-radius: 4px;
        }
        
        .product {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #ffc107;
            background: white;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div id="status" class="status disconnected">Disconnected</div>
        <div id="messages" class="messages"></div>
        <div class="input-area">
            <input id="messageInput" type="text" placeholder="Type your message..." disabled>
            <button id="sendButton" disabled>Send</button>
        </div>
    </div>

    <script>
        class StreamingChat {
            constructor() {
                this.socket = null;
                this.currentMessage = '';
                this.conversationId = null;
                
                this.statusEl = document.getElementById('status');
                this.messagesEl = document.getElementById('messages');
                this.inputEl = document.getElementById('messageInput');
                this.sendButtonEl = document.getElementById('sendButton');
                
                this.setupEventListeners();
                this.connect();
            }
            
            setupEventListeners() {
                this.sendButtonEl.addEventListener('click', () => this.sendMessage());
                this.inputEl.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.sendMessage();
                });
            }
            
            connect() {
                this.socket = new WebSocket('ws://localhost:8000/ws/chat/techpro');
                
                this.socket.onopen = () => {
                    this.statusEl.textContent = 'Connected';
                    this.statusEl.className = 'status connected';
                    this.inputEl.disabled = false;
                    this.sendButtonEl.disabled = false;
                };
                
                this.socket.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    this.handleMessage(message);
                };
                
                this.socket.onclose = () => {
                    this.statusEl.textContent = 'Disconnected';
                    this.statusEl.className = 'status disconnected';
                    this.inputEl.disabled = true;
                    this.sendButtonEl.disabled = true;
                };
            }
            
            handleMessage(message) {
                switch (message.type) {
                    case 'welcome':
                        this.addSystemMessage(message.data.message);
                        break;
                        
                    case 'chunk':
                        this.updateStreamingMessage(message.data.content);
                        this.conversationId = message.data.conversation_id;
                        break;
                        
                    case 'complete':
                        this.finalizeMessage(message.data.suggested_products);
                        break;
                        
                    case 'error':
                        this.addErrorMessage(message.data.message);
                        break;
                }
            }
            
            sendMessage() {
                const text = this.inputEl.value.trim();
                if (!text || !this.socket) return;
                
                this.addUserMessage(text);
                
                this.socket.send(JSON.stringify({
                    type: 'chat',
                    data: {
                        message: text,
                        conversation_id: this.conversationId
                    }
                }));
                
                this.inputEl.value = '';
                this.currentMessage = '';
                this.startStreaming();
            }
            
            addUserMessage(content) {
                const messageEl = document.createElement('div');
                messageEl.className = 'message user';
                messageEl.textContent = content;
                this.messagesEl.appendChild(messageEl);
                this.scrollToBottom();
            }
            
            addSystemMessage(content) {
                const messageEl = document.createElement('div');
                messageEl.className = 'message assistant';
                messageEl.textContent = content;
                this.messagesEl.appendChild(messageEl);
                this.scrollToBottom();
            }
            
            startStreaming() {
                this.streamingEl = document.createElement('div');
                this.streamingEl.className = 'message assistant streaming';
                this.streamingEl.innerHTML = '<span class="cursor">▌</span>';
                this.messagesEl.appendChild(this.streamingEl);
            }
            
            updateStreamingMessage(chunk) {
                if (!this.streamingEl) this.startStreaming();
                
                this.currentMessage += chunk;
                this.streamingEl.innerHTML = this.currentMessage + '<span class="cursor">▌</span>';
                this.scrollToBottom();
            }
            
            finalizeMessage(products) {
                if (this.streamingEl) {
                    this.streamingEl.className = 'message assistant';
                    this.streamingEl.innerHTML = this.currentMessage;
                    
                    if (products && products.length > 0) {
                        const productsEl = this.createProductsElement(products);
                        this.streamingEl.appendChild(productsEl);
                    }
                    
                    this.streamingEl = null;
                }
                this.scrollToBottom();
            }
            
            createProductsElement(products) {
                const productsEl = document.createElement('div');
                productsEl.className = 'products';
                
                const title = document.createElement('h4');
                title.textContent = 'Recommended Products:';
                productsEl.appendChild(title);
                
                products.forEach(product => {
                    const productEl = document.createElement('div');
                    productEl.className = 'product';
                    productEl.innerHTML = `
                        <strong>${product.name}</strong><br>
                        Price: $${product.price.toLocaleString()}<br>
                        ${product.description.substring(0, 100)}...
                    `;
                    productsEl.appendChild(productEl);
                });
                
                return productsEl;
            }
            
            addErrorMessage(content) {
                const messageEl = document.createElement('div');
                messageEl.className = 'message assistant';
                messageEl.textContent = `Error: ${content}`;
                messageEl.style.background = '#f8d7da';
                messageEl.style.color = '#721c24';
                this.messagesEl.appendChild(messageEl);
                this.scrollToBottom();
            }
            
            scrollToBottom() {
                this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
            }
        }
        
        // Initialize the chat when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new StreamingChat();
        });
    </script>
</body>
</html>
```

## Key Features

### ✅ Real-time Streaming
- Words appear as AI types them
- Smooth live typing effect
- 20ms delay between chunks for visibility

### ✅ Product Recommendations
- Suggested products appear after response
- Rich product information display
- Confidence scoring

### ✅ Voice Optimization
- Set `voice: true` for concise responses
- Perfect for text-to-speech integration

### ✅ Multi-brand Support
- Different brands have isolated data
- Brand-specific configurations
- Custom welcome messages

### ✅ Conversation Memory
- Maintains conversation context
- Conversation IDs for tracking
- Full chat history

## Error Handling

```javascript
// Connection error handling
socket.onerror = (error) => {
    console.error('WebSocket error:', error);
    showErrorMessage('Connection failed. Please check server.');
};

// Reconnection logic
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

function reconnect() {
    if (reconnectAttempts < maxReconnectAttempts) {
        setTimeout(() => {
            reconnectAttempts++;
            connect();
        }, 1000 * reconnectAttempts);
    }
}
```

## Production Considerations

1. **Environment Configuration**
   ```javascript
   const WS_URL = process.env.NODE_ENV === 'production' 
     ? 'wss://your-api-domain.com/ws/chat'
     : 'ws://localhost:8000/ws/chat';
   ```

2. **Rate Limiting**
   ```javascript
   const rateLimiter = {
     lastMessage: 0,
     minInterval: 1000, // 1 second between messages
     
     canSend() {
       const now = Date.now();
       if (now - this.lastMessage < this.minInterval) {
         return false;
       }
       this.lastMessage = now;
       return true;
     }
   };
   ```

3. **Message Validation**
   ```javascript
   function validateMessage(text) {
     if (!text || text.length === 0) return false;
     if (text.length > 1000) return false;
     return true;
   }
   ```

This guide provides everything needed to implement real-time streaming chat in any frontend framework! 
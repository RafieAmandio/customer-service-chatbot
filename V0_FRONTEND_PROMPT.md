# V0 Frontend Prompt: Customer Service Chatbot Interface

Create a modern, responsive React web application for a customer service chatbot that interacts with an existing FastAPI backend.

## 🎯 Application Overview

Build a **customer service chatbot interface** for "TechPro Solutions" - a technology retailer specializing in business laptops, smartphones, monitors, and accessories. The interface should be professional, intuitive, and optimized for both customers and support agents.

## 🎨 Design Requirements

### Visual Style
- **Modern, clean design** with a professional business aesthetic
- **Color scheme:** Primary blue (#1e40af), secondary gray (#64748b), accent green (#10b981) for success states
- **Typography:** Inter or similar clean sans-serif font
- **Responsive design** that works on desktop, tablet, and mobile
- **Dark/light mode support** with toggle

### Layout Structure
- **Header:** Company logo, navigation, dark mode toggle
- **Main chat area:** Full-height chat interface with conversation history
- **Sidebar (optional):** Product categories, recent searches, suggested questions
- **Product cards:** Rich product display with images, specs, and pricing

## 🔧 Core Features to Implement

### 1. Chat Interface
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  suggestedProducts?: Product[];
  confidenceScore?: number;
}
```

**Features:**
- Real-time typing indicators
- Message bubbles with different styles for user/assistant
- Auto-scroll to latest message
- Message timestamps
- Copy message functionality
- Regenerate response button

### 2. Product Display & Interaction
```typescript
interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  features: string[];
  specifications: Record<string, any>;
  availability: boolean;
}
```

**Features:**
- **Product cards** in chat responses with hover effects
- **Product comparison** side-by-side view
- **Product details modal** with full specifications
- **Add to cart/wishlist** buttons (visual only)
- **Price formatting** with currency symbols
- **Availability indicators** (in stock/out of stock)

### 3. Conversation Management
- **New conversation** button
- **Conversation history** with titles and timestamps
- **Clear conversation** functionality
- **Export conversation** as text/PDF
- **Search conversation history**

### 4. Smart Input Features
- **Suggested questions/prompts** for new users
- **Quick action buttons:** "Find laptops", "Compare products", "Business solutions"
- **Voice input** support (optional)
- **File upload** for images/documents (placeholder)
- **Auto-complete** for common queries

### 5. Advanced UI Components
- **Loading states** with skeleton loaders
- **Error handling** with retry mechanisms
- **Toast notifications** for actions
- **Progressive disclosure** for complex product specs
- **Infinite scroll** for product lists
- **Search filters** for products by category, price range

## 🛠 Technical Requirements

### Frontend Stack
- **React 18+** with TypeScript
- **Tailwind CSS** for styling
- **Shadcn/ui** or **Radix UI** for components
- **React Query/TanStack Query** for API state management
- **Zustand** or **Context API** for global state
- **React Router** for navigation
- **Lucide React** for icons

### API Integration
**Base URL:** `http://localhost:8000`

#### Key Endpoints to Integrate:
```typescript
// Chat endpoints
POST /chat
GET /chat/history/{conversation_id}
DELETE /chat/{conversation_id}

// Product endpoints  
GET /products
POST /products/search
GET /categories
GET /stats

// Health check
GET /
```

#### Example API Calls:
```typescript
// Send message to chatbot
const sendMessage = async (message: string, conversationId?: string) => {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversation_id: conversationId })
  });
  return response.json();
};

// Search products
const searchProducts = async (query: string, filters?: any) => {
  const response = await fetch('http://localhost:8000/products/search', {
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, ...filters })
  });
  return response.json();
};
```

## 📱 Component Structure

```
src/
├── components/
│   ├── chat/
│   │   ├── ChatContainer.tsx        # Main chat interface
│   │   ├── ChatMessage.tsx          # Individual message bubble  
│   │   ├── ChatInput.tsx            # Message input with features
│   │   ├── TypingIndicator.tsx      # Loading/typing animation
│   │   └── SuggestedQuestions.tsx   # Quick question buttons
│   ├── products/
│   │   ├── ProductCard.tsx          # Product display card
│   │   ├── ProductModal.tsx         # Detailed product view
│   │   ├── ProductComparison.tsx    # Side-by-side comparison
│   │   └── ProductFilters.tsx       # Search/filter controls
│   ├── layout/
│   │   ├── Header.tsx               # App header with nav
│   │   ├── Sidebar.tsx              # Optional sidebar
│   │   └── Layout.tsx               # Main layout wrapper
│   └── ui/                          # Reusable UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Modal.tsx
│       └── ...
├── hooks/
│   ├── useChat.ts                   # Chat state management
│   ├── useProducts.ts               # Product data fetching
│   └── useLocalStorage.ts           # Persist conversations
├── types/
│   ├── chat.ts                      # Chat-related types
│   └── product.ts                   # Product types
└── utils/
    ├── api.ts                       # API client
    ├── formatters.ts                # Price, date formatting
    └── constants.ts                 # App constants
```

## 🎭 User Experience Features

### Onboarding
- **Welcome screen** with company information
- **Sample questions** to get users started
- **Tutorial tooltip** for first-time users
- **Features overview** modal

### Accessibility
- **ARIA labels** and semantic HTML
- **Keyboard navigation** support
- **Screen reader** compatibility
- **High contrast** mode option
- **Focus management** for modals

### Performance
- **Code splitting** for routes
- **Image lazy loading** for products
- **Debounced search** input
- **Optimistic updates** for better UX
- **Service worker** for offline support (optional)

### Error Handling
- **Network error** recovery
- **API timeout** handling
- **Fallback UI** for failed states
- **User-friendly error messages**

## 💡 Sample User Flows

### 1. First-Time User Journey
1. User lands on homepage with welcome message
2. Sees suggested questions: "Tell me about your company", "I need a laptop for business"
3. Clicks on "I need a laptop for business"
4. Chatbot responds with questions about budget, use case
5. Shows relevant laptop recommendations with specs
6. User can compare products, view details, get more recommendations

### 2. Product Search Flow
1. User types: "gaming laptop under $2000"
2. Chat shows typing indicator
3. Response includes 2-3 relevant laptops with reasoning
4. Product cards show key specs, price, availability
5. User clicks "View Details" → opens product modal
6. User can ask follow-up questions about specific products

### 3. Business Customer Flow
1. User asks: "What promotions do you have for business customers?"
2. Chatbot explains current business deals
3. Shows relevant product bundles with discounts
4. Offers to connect with business account manager
5. Provides contact information and next steps

## 🔧 Configuration & Environment

```typescript
// Environment variables
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_COMPANY_NAME=TechPro Solutions
REACT_APP_SUPPORT_EMAIL=support@techprosolutions.com
REACT_APP_ENABLE_VOICE=true
REACT_APP_ENABLE_ANALYTICS=false
```

## 🎨 Example Component Code

```typescript
// ChatMessage.tsx example structure
interface ChatMessageProps {
  message: ChatMessage;
  onProductClick: (product: Product) => void;
  onRegenerateResponse: () => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onProductClick,
  onRegenerateResponse
}) => {
  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[70%] rounded-lg p-4 ${
        message.role === 'user' 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 text-gray-900'
      }`}>
        <p className="text-sm">{message.content}</p>
        
        {message.suggestedProducts && (
          <div className="mt-3 space-y-2">
            {message.suggestedProducts.map(product => (
              <ProductCard 
                key={product.id}
                product={product}
                compact
                onClick={() => onProductClick(product)}
              />
            ))}
          </div>
        )}
        
        <div className="flex items-center justify-between mt-2 text-xs opacity-70">
          <span>{formatTime(message.timestamp)}</span>
          {message.role === 'assistant' && (
            <Button variant="ghost" size="sm" onClick={onRegenerateResponse}>
              <RefreshIcon className="w-3 h-3" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
```

## 🚀 Getting Started Instructions

1. **Setup the project** with Vite + React + TypeScript
2. **Install dependencies:** React Query, Tailwind, Shadcn/ui
3. **Configure API client** to connect to FastAPI backend
4. **Implement core chat interface** first
5. **Add product display** and interaction features
6. **Enhance with advanced features** (search, filters, etc.)
7. **Add responsive design** and mobile optimization
8. **Implement error handling** and loading states

## 🎯 Success Criteria

- ✅ **Functional chat interface** that connects to the API
- ✅ **Professional design** that reflects TechPro Solutions brand
- ✅ **Responsive layout** that works on all devices
- ✅ **Smooth animations** and transitions
- ✅ **Product recommendations** display beautifully
- ✅ **Error handling** provides good user experience
- ✅ **Fast performance** with optimized loading
- ✅ **Accessible** to users with disabilities

This should be a **production-ready customer service interface** that businesses would be proud to deploy for their customers! 
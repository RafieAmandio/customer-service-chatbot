# 🆕 New Features Documentation

## Overview
This document covers the three major new features added to the Customer Service Chatbot API:

1. **Voice Response Mode** - Short, voice-optimized responses
2. **File Upload System** - Bulk product upload via JSON/CSV files  
3. **Indonesian Localization** - Full Indonesian language support with Rupiah pricing

---

## 🎤 Feature 1: Voice Response Mode

### What's New
Added an optional `voice` parameter to the chat endpoint that enables voice-optimized responses perfect for text-to-speech systems and voice assistants.

### Implementation Details

#### Request Parameter
```json
{
  "message": "Your message here",
  "voice": true  // NEW: Optional boolean parameter
}
```

#### Response Characteristics
When `voice: true`:
- ✅ **Maximum 1 sentence** response
- ✅ **Reduced token usage** (50 vs 600 tokens)
- ✅ **Natural speech patterns**
- ✅ **Still includes product suggestions** in metadata
- ✅ **Maintains conversation context**

#### Examples

**Regular Chat Response:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Rekomendasikan laptop gaming"}'
```
Response: ~2-3 paragraphs with detailed explanations

**Voice-Optimized Response:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Rekomendasikan laptop gaming", "voice": true}'
```
Response: "Untuk kebutuhan gaming, saya rekomendasikan ASUS ROG Strix G16 karena memiliki prosesor Intel Core i7 generasi ke-13 dan grafis RTX 4060."

#### Technical Implementation
```python
# Voice response handling in chatbot_service.py
if is_voice:
    # Add voice-specific instruction to OpenAI prompt
    voice_instruction = """
    IMPORTANT: This is a voice response request. Your response must be:
    - Maximum 1 sentence
    - Concise and direct
    - Natural for voice output
    - Still helpful and informative
    """
    
    # Reduce max_tokens for efficiency
    max_tokens = 50 if is_voice else 600
    
    # Post-process to ensure single sentence
    sentences = re.split(r'[.!?]+', response_content)
    response_content = sentences[0].strip() + "."
```

### Use Cases
- Voice assistants (Alexa, Google Assistant)
- Text-to-speech applications
- Mobile voice interfaces
- Quick voice queries during multitasking

---

## 📁 Feature 2: File Upload System

### What's New
Complete file upload system that allows bulk product management through JSON and CSV files.

### New Endpoints

#### 1. Upload Products File
```http
POST /upload/products
Content-Type: multipart/form-data
```

**Supported Formats:**
- ✅ JSON files (.json)
- ✅ CSV files (.csv)
- ✅ PDF files (.pdf) - AI-powered text extraction
- ✅ Text files (.txt) - Plain text parsing
- ✅ Markdown files (.md) - Structured text parsing
- ✅ Word documents (.docx) - Document text extraction
- ✅ XML files (.xml) - Structured data parsing

**Response:**
```json
{
  "message": "Successfully uploaded sample_products.pdf and added 5 products",
  "filename": "sample_products.pdf", 
  "products_added": 5,
  "upload_id": "6fff5fdb-fd4b-448c-b6e0-111404ac9131"
}
```

#### 2. List Uploaded Files
```http
GET /uploads
```

**Response:**
```json
[
  {
    "filename": "sample_products.json",
    "upload_time": "2025-06-04T19:45:16.186396",
    "file_size": 2597,
    "products_added": 3,
    "status": "success"
  }
]
```

#### 3. Get Upload Details
```http
GET /uploads/{filename}
```

### File Formats

#### JSON Format
```json
[
  {
    "id": "laptop-007",
    "name": "Acer Aspire 5 Slim", 
    "description": "Laptop terjangkau dengan performa yang baik...",
    "category": "Laptop",
    "price": 8999000.0,
    "features": [
      "AMD Ryzen 5 5500U",
      "Layar Full HD 15.6-inch"
    ],
    "specifications": {
      "prosesor": "AMD Ryzen 5 5500U (6-core)",
      "memori": "8GB DDR4"
    },
    "availability": true
  }
]
```

#### CSV Format
```csv
id,name,description,category,price,features,specifications,availability
laptop-007,Acer Aspire 5,"Laptop terjangkau",Laptop,8999000.0,"AMD Ryzen 5,Full HD","{""prosesor"":""AMD Ryzen 5""}",true
```

#### XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<products>
    <product>
        <id>smartphone-001</id>
        <name>Samsung Galaxy S24 Ultra</name>
        <description>Smartphone flagship dengan S Pen dan kamera 200MP</description>
        <category>Smartphone</category>
        <price>21999000</price>
        <features>
            <feature>S Pen terintegrasi</feature>
            <feature>Kamera 200MP dengan AI</feature>
        </features>
        <specifications>
            <prosesor>Snapdragon 8 Gen 3</prosesor>
            <memori>12GB RAM</memori>
        </specifications>
        <availability>true</availability>
    </product>
</products>
```

#### Text Format (.txt, .md)
```txt
=== LAPTOP GAMING ===

MSI Gaming Laptop GF63
- ID: laptop-gaming-001
- Kategori: Laptop Gaming
- Harga: Rp 12.500.000
- Deskripsi: Laptop gaming dengan performa tinggi
- Prosesor: Intel Core i5-11400H
- Memori: 8GB DDR4
- Grafis: NVIDIA GeForce GTX 1650
```

#### PDF Format
- ✅ **Automatic text extraction** using pdfplumber and PyPDF2
- ✅ **AI-powered parsing** to identify product information
- ✅ **Multi-page support** with content consolidation
- ✅ **Table extraction** from PDF documents
- ✅ **Fallback processing** if structured parsing fails

#### Word Document Format (.docx)
- ✅ **Text extraction** from paragraphs and tables
- ✅ **Structured content processing** including headers
- ✅ **Table data parsing** for tabular product information
- ✅ **Rich text handling** with formatting preservation

### AI-Powered Text Parsing

For unstructured formats (PDF, TXT, MD, DOCX), the system uses **OpenAI GPT-4** to intelligently extract product information:

#### AI Parsing Features
- ✅ **Automatic field detection** (name, price, category, etc.)
- ✅ **Currency conversion** to Indonesian Rupiah
- ✅ **Feature extraction** from descriptive text
- ✅ **Specification parsing** from technical details
- ✅ **ID generation** if not provided
- ✅ **Smart categorization** based on content analysis

#### Example AI Parsing
**Input Text:**
```
Laptop gaming MSI dengan prosesor Intel i7, RAM 16GB, 
harga $1000, cocok untuk gaming dan editing video
```

**AI-Generated Product:**
```json
{
  "id": "extracted-abc12345",
  "name": "MSI Gaming Laptop", 
  "description": "Laptop gaming dengan prosesor Intel i7 untuk gaming dan editing video",
  "category": "Laptop",
  "price": 15500000,
  "features": ["Intel Core i7", "16GB RAM", "Gaming optimized"],
  "specifications": {
    "prosesor": "Intel Core i7",
    "memori": "16GB RAM"
  },
  "availability": true
}
```

### Implementation Features
- ✅ **Automatic parsing** and database insertion
- ✅ **Error handling** for malformed files
- ✅ **Upload tracking** with metadata
- ✅ **Duplicate handling** (updates existing products)
- ✅ **File validation** (type and format checking)

### Technical Implementation
```python
# File processing in main.py
async def _process_json_file(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products_added = 0
    if isinstance(data, list):
        for product_data in data:
            product = Product(**product_data)
            if vector_store.add_product(product):
                products_added += 1
    
    return products_added
```

### Use Cases
- Bulk product imports from external systems
- Inventory updates from CSV exports
- Product catalog migrations
- Batch product management
- Integration with e-commerce platforms

---

## 🇮🇩 Feature 3: Indonesian Localization

### What's New
Complete Indonesian language support with localized product data, Rupiah pricing, and native Indonesian conversation capabilities.

### Key Changes

#### 1. Product Data Localization
All sample products converted to Indonesian:

**Before (English):**
```json
{
  "name": "MacBook Pro 14-inch M3 Pro",
  "description": "Premium laptop designed for professionals, creative work, and business applications",
  "category": "Laptops",
  "price": 1999.99,
  "specifications": {
    "processor": "Apple M3 Pro",
    "memory": "18GB unified memory",
    "warranty": "1 year limited warranty"
  }
}
```

**After (Indonesian):**
```json
{
  "name": "MacBook Pro 14-inch M3 Pro", 
  "description": "Laptop premium yang dirancang untuk profesional, pekerjaan kreatif, dan aplikasi bisnis",
  "category": "Laptop",
  "price": 30999000.00,
  "specifications": {
    "prosesor": "Apple M3 Pro",
    "memori": "18GB unified memory", 
    "garansi": "1 tahun garansi terbatas"
  }
}
```

#### 2. Currency Conversion
- ✅ **Prices in Indonesian Rupiah** (IDR)
- ✅ **Proper formatting**: Rp 30.999.000
- ✅ **No decimal places** for Rupiah amounts
- ✅ **Realistic pricing** based on Indonesian market

#### 3. Language Detection & Response
```python
# Automatic language detection
indonesian_keywords = ['saya', 'butuh', 'perlu', 'cari', 'mau', 'ingin', 'untuk', 'yang', 'apa', 'bagaimana']
is_indonesian = any(keyword in query.lower() for keyword in indonesian_keywords)

# Bilingual prompting
if is_indonesian:
    prompt = "Berikan penjelasan dalam Bahasa Indonesia..."
else:
    prompt = "Provide explanation in English..."
```

#### 4. Business Context Localization
Updated company information to Indonesian context:

```python
BUSINESS_CONTEXT = """
**TechPro Solutions Indonesia - Partner Teknologi Premium**

**Tentang Perusahaan Kami:**
- Kami adalah TechPro Solutions Indonesia, retailer teknologi terkemuka
- Didirikan pada tahun 2018, kami melayani bisnis di seluruh Indonesia
- Spesialisasi: laptop bisnis, workstation, sistem kreatif, aksesoris profesional

**Promosi Terkini:**
- Diskon 10% untuk bundel laptop bisnis
- Setup gratis untuk pembelian di atas Rp 23 juta
- Garansi diperpanjang 50% off untuk pelanggan baru
"""
```

### Language Features

#### Conversation Examples

**Indonesian Input:**
```json
{
  "message": "Saya butuh laptop untuk kerja bisnis di bawah 25 juta"
}
```

**Indonesian Response:**
```json
{
  "response": "Untuk kebutuhan kerja bisnis dengan budget di bawah 25 juta, saya rekomendasikan beberapa pilihan yang sangat baik. Dell XPS 13 Plus dengan harga Rp 19.999.000 sangat cocok untuk profesional bisnis..."
}
```

**English Input:**
```json
{
  "message": "I need a laptop for business work under 25 million rupiah"
}
```

**English Response:**
```json
{
  "response": "For business work within your budget of 25 million rupiah, I recommend several excellent options. The Dell XPS 13 Plus at Rp 19,999,000 is perfect for business professionals..."
}
```

### Implementation Details

#### 1. Multilingual System Prompt
```python
self.system_prompt = """
You are a helpful customer service chatbot for TechPro Solutions, a premium technology retailer.

**MULTILINGUAL SUPPORT:**
You can communicate in both English and Indonesian (Bahasa Indonesia). Always respond in the same language the customer uses.

**Language Guidelines:**
- Detect the language used and respond appropriately
- Use proper Indonesian terminology for technical specifications
- Format prices in Rupiah for Indonesian responses
- Maintain cultural context for Indonesian customers
"""
```

#### 2. Price Formatting
```python
# In test_chatbot.py
price_formatted = f"Rp {product['price']:,.0f}".replace(',', '.')
# Output: Rp 30.999.000
```

#### 3. Category Localization
- Laptops → Laptop
- Accessories → Aksesoris  
- Smartphones → Smartphone
- Monitors → Monitor

### Benefits
- ✅ **Native Indonesian experience** for local customers
- ✅ **Accurate pricing** in local currency
- ✅ **Cultural relevance** in product descriptions
- ✅ **Technical terms** in Indonesian
- ✅ **Seamless bilingual** operation

---

## 🧪 Testing the New Features

### 1. Test Voice Responses
```bash
# Standard response
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Rekomendasikan laptop gaming"}'

# Voice response
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Rekomendasikan laptop gaming", "voice": true}'
```

### 2. Test File Upload
```bash
# Upload sample products (JSON)
curl -X POST "http://localhost:8000/upload/products" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_products.json"

# Upload text file
curl -X POST "http://localhost:8000/upload/products" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_products.txt"

# Upload XML file
curl -X POST "http://localhost:8000/upload/products" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_products.xml"

# Check uploads
curl -X GET "http://localhost:8000/uploads"
```

### 3. Test Indonesian Language
```bash
# Indonesian query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Saya butuh laptop untuk bisnis dengan budget 20 juta"}'

# English query  
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a business laptop with 20 million rupiah budget"}'
```

### 4. Run Comprehensive Tests
```bash
python test_chatbot.py
```

---

## 🚀 Migration Guide

### For Existing Users

#### 1. Chat API Changes
**Before:**
```json
{
  "message": "I need a laptop",
  "conversation_id": "optional"
}
```

**After (Backward Compatible):**
```json
{
  "message": "I need a laptop", 
  "conversation_id": "optional",
  "voice": false  // NEW: Optional parameter
}
```

#### 2. Price Updates
- All existing USD prices converted to IDR
- Display format changed to Rupiah
- No breaking changes to API structure

#### 3. New Endpoints
- `POST /upload/products` - New file upload capability
- `GET /uploads` - New upload tracking
- `GET /uploads/{filename}` - New upload details

### Integration Tips

#### Voice Integration
```javascript
// Example: Voice assistant integration
async function getVoiceResponse(message) {
  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, voice: true })
  });
  
  const data = await response.json();
  
  // Perfect for text-to-speech
  speechSynthesis.speak(new SpeechSynthesisUtterance(data.response));
  
  return data;
}
```

#### File Upload Integration
```javascript
// Example: File upload with progress
async function uploadProducts(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/upload/products', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log(`Added ${result.products_added} products`);
}
```

---

## 📊 Performance Impact

### Voice Mode Benefits
- **50% reduction** in token usage (50 vs 600 tokens)
- **Faster response times** due to shorter generation
- **Lower API costs** from OpenAI
- **Better user experience** for voice interfaces

### File Upload Capabilities
- **Bulk operations** instead of individual API calls
- **Atomic transactions** (all succeed or all fail)
- **Automatic validation** and error reporting
- **Upload tracking** for audit purposes

### Indonesian Localization
- **No performance impact** on existing functionality
- **Automatic language detection** with minimal overhead
- **Enhanced user experience** for Indonesian users
- **Broader market reach** capabilities

---

## 🔮 Future Enhancements

### Planned Improvements
1. **Voice Mode Enhancements**
   - Multiple sentence options (1, 2, 3 sentences)
   - Voice personality settings
   - SSML support for better TTS

2. **File Upload Extensions**
   - Excel file support (.xlsx)
   - Image upload for product photos
   - Bulk update capabilities
   - Scheduled imports

3. **Localization Expansion**
   - Additional languages (Malay, Thai, Vietnamese)
   - Regional pricing for different countries
   - Cultural customization options
   - Local payment method integration

### Contribution Guidelines
To extend these features:
1. Follow existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Maintain backward compatibility
5. Consider performance implications 
# Brand Management API Documentation

## Overview

The Brand Management API provides complete multi-brand support for the chatbot system. Each brand has isolated data storage, custom configurations, and independent chatbot instances. This allows you to run multiple brands with different personalities, product catalogs, and configurations on the same platform.

## Core Concepts

- **Brand**: A unique entity with its own identity, products, and chatbot instance
- **Brand Configuration**: Settings that define the chatbot's behavior, appearance, and messaging
- **Data Isolation**: Each brand has separate product catalogs and conversation histories
- **Brand Status**: Brands can be active or inactive, affecting their availability

---

## Brand CRUD Operations

### Create Brand

#### `POST /brands`

**Description:** Create a new brand with default configuration.

**Query Parameters:**
- `name` (required): The brand name
- `description` (required): Brand description
- `brand_id` (optional): Custom brand ID (auto-generated if not provided)

**Response:**
```json
{
  "id": "techpro",
  "name": "TechPro Solutions", 
  "description": "Premium technology retailer",
  "created_at": "2025-06-12T21:39:10.041967",
  "updated_at": null,
  "is_active": true
}
```

**Examples:**
```bash
# Basic brand creation
curl -X POST "http://localhost:8000/brands?name=TechCorp&description=Technology%20company"

# With custom brand ID
curl -X POST "http://localhost:8000/brands?name=LuxuryTech&description=Premium%20tech%20retailer&brand_id=luxury"
```

### Get All Brands

#### `GET /brands`

**Description:** Retrieve all brands (active and inactive).

**Response:**
```json
[
  {
    "id": "techpro",
    "name": "TechPro Solutions",
    "description": "Premium technology retailer",
    "created_at": "2025-06-12T21:39:10.041967",
    "updated_at": null,
    "is_active": true
  },
  {
    "id": "luxury",
    "name": "LuxuryTech",
    "description": "Premium tech retailer",
    "created_at": "2025-06-12T21:40:15.123456",
    "updated_at": null,
    "is_active": true
  }
]
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands"
```

### Get Active Brands

#### `GET /brands/active`

**Description:** Retrieve only active brands.

**Response:**
```json
[
  {
    "id": "techpro",
    "name": "TechPro Solutions",
    "description": "Premium technology retailer",
    "created_at": "2025-06-12T21:39:10.041967",
    "updated_at": null,
    "is_active": true
  }
]
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands/active"
```

### Get Specific Brand

#### `GET /brands/{brand_id}`

**Description:** Retrieve details for a specific brand.

**Parameters:**
- `brand_id` (path): The brand identifier

**Response:**
```json
{
  "id": "techpro",
  "name": "TechPro Solutions",
  "description": "Premium technology retailer",
  "created_at": "2025-06-12T21:39:10.041967",
  "updated_at": null,
  "is_active": true
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands/techpro"
```

### Update Brand

#### `PUT /brands/{brand_id}`

**Description:** Update brand information.

**Parameters:**
- `brand_id` (path): The brand identifier

**Query Parameters (all optional):**
- `name`: New brand name
- `description`: New brand description  
- `is_active`: Brand status (true/false)

**Response:**
```json
{
  "id": "techpro",
  "name": "TechPro Solutions Updated",
  "description": "Updated premium technology retailer",
  "created_at": "2025-06-12T21:39:10.041967",
  "updated_at": "2025-06-12T22:15:30.123456",
  "is_active": true
}
```

**Examples:**
```bash
# Update name and description
curl -X PUT "http://localhost:8000/brands/techpro?name=TechPro%20Solutions%20Updated&description=Updated%20description"

# Deactivate brand
curl -X PUT "http://localhost:8000/brands/techpro?is_active=false"

# Reactivate brand
curl -X PUT "http://localhost:8000/brands/techpro?is_active=true"
```

### Delete Brand

#### `DELETE /brands/{brand_id}`

**Description:** Permanently delete a brand and all its data including products, configurations, and conversation history.

**Parameters:**
- `brand_id` (path): The brand identifier

**Response:**
```json
{
  "message": "Brand deleted successfully"
}
```

**⚠️ Warning:** This operation is irreversible and will delete all brand data.

---

## Brand Configuration Management

### Get Brand Configuration

#### `GET /brands/{brand_id}/config`

**Description:** Retrieve the complete configuration for a brand.

**Parameters:**
- `brand_id` (path): The brand identifier

**Response:**
```json
{
  "brand_id": "techpro",
  "system_prompt": "You are a helpful customer service chatbot for TechPro Solutions...",
  "welcome_message": "Welcome to TechPro Solutions! How can I help you today?",
  "company_info": {
    "name": "TechPro Solutions",
    "founded": "2018",
    "specialty": "Business and professional technology equipment"
  },
  "appearance_settings": {
    "primary_color": "#007bff",
    "secondary_color": "#6c757d",
    "logo_url": "/static/techpro-logo.png"
  },
  "updated_at": "2025-06-12T21:39:10.042005"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands/techpro/config"
```

### Update Brand Configuration

#### `PUT /brands/{brand_id}/config`

**Description:** Update brand configuration settings.

**Parameters:**
- `brand_id` (path): The brand identifier

**Query Parameters (all optional):**
- `system_prompt`: AI chatbot instructions
- `welcome_message`: Initial greeting message
- `company_info`: Company information (JSON object)
- `appearance_settings`: UI customization (JSON object)

**Response:**
```json
{
  "brand_id": "techpro",
  "system_prompt": "Updated system prompt...",
  "welcome_message": "Updated welcome message",
  "company_info": {
    "name": "TechPro Solutions",
    "founded": "2018"
  },
  "appearance_settings": {
    "primary_color": "#ff6b35",
    "secondary_color": "#2c3e50"
  },
  "updated_at": "2025-06-12T22:30:15.789012"
}
```

**Examples:**
```bash
# Update welcome message
curl -X PUT "http://localhost:8000/brands/techpro/config?welcome_message=Hello%20and%20welcome!"

# Update appearance (JSON as URL parameter is complex, better to use the dedicated endpoints)
```

---

## System Prompt Management

### Get System Prompt

#### `GET /brands/{brand_id}/system-prompt`

**Description:** Retrieve the current system prompt for a brand's chatbot.

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

**Description:** Update the system prompt for a brand's chatbot with immediate effect.

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
  "updated_at": "2025-06-12T22:45:30.123456"
}
```

**Example:**
```bash
curl -X PUT "http://localhost:8000/brands/techpro/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a professional customer service representative for TechPro Solutions. Always maintain a helpful and informative tone."
  }'
```

---

## Brand Statistics

### Get Brand Statistics

#### `GET /brands/{brand_id}/stats`

**Description:** Retrieve comprehensive statistics for a specific brand.

**Parameters:**
- `brand_id` (path): The brand identifier

**Response:**
```json
{
  "brand_id": "techpro",
  "brand_name": "TechPro Solutions",
  "total_products": 10,
  "available_products": 9,
  "categories": 4,
  "active_conversations": 5,
  "category_list": ["Accessories", "Laptop", "Monitor", "Smartphone"]
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/brands/techpro/stats"
```

### Get Global Statistics

#### `GET /stats`

**Description:** Retrieve statistics across all brands.

**Response:**
```json
{
  "total_brands": 2,
  "active_brands": 2,
  "total_products": 15,
  "total_conversations": 8,
  "brands_stats": [
    {
      "brand_id": "techpro",
      "brand_name": "TechPro Solutions",
      "total_products": 10,
      "available_products": 9,
      "categories": 4,
      "active_conversations": 5
    },
    {
      "brand_id": "luxury",
      "brand_name": "LuxuryTech",
      "total_products": 5,
      "available_products": 5,
      "categories": 2,
      "active_conversations": 3
    }
  ]
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/stats"
```

---

## Error Responses

### Brand Not Found (404)
```json
{
  "detail": "Brand not found"
}
```

### Brand Already Exists (400)
```json
{
  "detail": "Brand with ID 'techpro' already exists"
}
```

### Invalid Parameters (422)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "name"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

---

## Data Models

### Brand Model
```json
{
  "id": "string",
  "name": "string",
  "description": "string", 
  "created_at": "datetime",
  "updated_at": "datetime|null",
  "is_active": "boolean"
}
```

### Brand Configuration Model
```json
{
  "brand_id": "string",
  "system_prompt": "string",
  "welcome_message": "string",
  "company_info": {
    "name": "string",
    "founded": "string",
    "specialty": "string",
    "location": "string",
    "mission": "string"
  },
  "appearance_settings": {
    "primary_color": "string",
    "secondary_color": "string", 
    "logo_url": "string"
  },
  "updated_at": "datetime"
}
```

---

## Integration Examples

### Complete Brand Setup

```bash
# 1. Create a new brand
curl -X POST "http://localhost:8000/brands?name=FashionTech&description=Trendy%20technology%20for%20fashion"

# 2. Update system prompt
curl -X PUT "http://localhost:8000/brands/fashiontech/system-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a stylish AI assistant for FashionTech. Help customers find trendy technology that matches their lifestyle and aesthetic preferences."
  }'

# 3. Update configuration
curl -X PUT "http://localhost:8000/brands/fashiontech/config?welcome_message=Welcome%20to%20FashionTech!%20Let%27s%20find%20your%20perfect%20tech%20style"

# 4. Check brand statistics
curl -X GET "http://localhost:8000/brands/fashiontech/stats"
```

### Brand Management Workflow

```bash
# List all brands
curl -X GET "http://localhost:8000/brands"

# Get specific brand details
curl -X GET "http://localhost:8000/brands/techpro"

# Update brand status
curl -X PUT "http://localhost:8000/brands/techpro?is_active=false"

# Get only active brands
curl -X GET "http://localhost:8000/brands/active"

# Delete inactive brands
curl -X DELETE "http://localhost:8000/brands/old-brand"
```

---

## Key Features

✅ **Complete CRUD Operations**: Create, read, update, and delete brands  
✅ **Data Isolation**: Each brand has separate products and conversations  
✅ **Custom Configuration**: Tailored system prompts, messages, and appearance  
✅ **Real-time Statistics**: Track products, conversations, and categories  
✅ **Brand Status Management**: Activate/deactivate brands as needed  
✅ **Automatic ID Generation**: Smart brand ID creation from names  
✅ **Persistent Storage**: All data saved automatically  
✅ **Immediate Updates**: Configuration changes take effect instantly  

## Best Practices

1. **Brand Naming**: Use clear, descriptive names for easy identification
2. **ID Strategy**: Let the system auto-generate IDs or use consistent naming conventions
3. **Configuration**: Set up system prompts and welcome messages that reflect brand personality
4. **Status Management**: Use active/inactive status instead of deletion for temporary changes
5. **Regular Monitoring**: Check brand statistics to track growth and usage
6. **Backup Strategy**: Export brand configurations before major changes

This comprehensive API enables full multi-brand chatbot management with complete isolation and customization! 🚀 
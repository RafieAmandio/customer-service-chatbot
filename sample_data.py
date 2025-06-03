import asyncio
import httpx
from typing import List
from models import Product

# Enhanced product data with more laptops and business context
SAMPLE_PRODUCTS = [
    # Laptops - Business & Professional
    Product(
        id="laptop-001",
        name="MacBook Pro 14-inch M3 Pro",
        description="Premium laptop designed for professionals, creative work, and business applications. Perfect for video editing, software development, and demanding business tasks.",
        category="Laptops",
        price=1999.99,
        features=[
            "M3 Pro chip with 12-core CPU", 
            "14-inch Liquid Retina XDR display", 
            "18GB unified memory", 
            "512GB SSD storage", 
            "Up to 18-hour battery life",
            "Thunderbolt 4 ports",
            "1080p FaceTime HD camera",
            "Six-speaker sound system"
        ],
        specifications={
            "processor": "Apple M3 Pro (12-core CPU, 18-core GPU)",
            "memory": "18GB unified memory",
            "storage": "512GB SSD",
            "display": "14-inch Liquid Retina XDR (3024×1964)",
            "weight": "3.5 lbs (1.6 kg)",
            "color": "Space Gray",
            "ports": "3x Thunderbolt 4, HDMI, SDXC, MagSafe 3",
            "os": "macOS Sonoma",
            "warranty": "1 year limited warranty"
        }
    ),
    Product(
        id="laptop-002",
        name="Dell XPS 13 Plus",
        description="Ultra-portable business laptop with premium design and performance. Ideal for business professionals, consultants, and executives who need mobility without compromising power.",
        category="Laptops", 
        price=1299.99,
        features=[
            "12th Gen Intel Core i7 processor",
            "13.4-inch 4K OLED touchscreen", 
            "16GB LPDDR5 RAM",
            "512GB PCIe SSD",
            "Intel Iris Xe graphics",
            "Premium aluminum build",
            "Backlit keyboard",
            "Windows 11 Pro"
        ],
        specifications={
            "processor": "Intel Core i7-1280P (14-core)",
            "memory": "16GB LPDDR5",
            "storage": "512GB PCIe NVMe SSD",
            "display": "13.4-inch 4K OLED (3840×2400) touchscreen",
            "weight": "2.73 lbs (1.24 kg)",
            "color": "Platinum Silver",
            "ports": "2x Thunderbolt 4, 1x USB-C 3.2",
            "os": "Windows 11 Pro",
            "warranty": "1 year ProSupport"
        }
    ),
    Product(
        id="laptop-003",
        name="ThinkPad X1 Carbon Gen 11",
        description="Legendary business laptop trusted by enterprises worldwide. Built for executives, consultants, and business professionals who demand reliability, security, and performance.",
        category="Laptops",
        price=1699.99,
        features=[
            "13th Gen Intel Core i7 vPro",
            "14-inch 2.8K OLED display",
            "32GB LPDDR5 RAM", 
            "1TB PCIe SSD",
            "Intel Iris Xe graphics",
            "Carbon fiber construction",
            "Fingerprint reader",
            "IR camera with Windows Hello",
            "Military-grade durability"
        ],
        specifications={
            "processor": "Intel Core i7-1365U vPro (10-core)",
            "memory": "32GB LPDDR5",
            "storage": "1TB PCIe NVMe SSD",
            "display": "14-inch 2.8K OLED (2880×1800)",
            "weight": "2.48 lbs (1.12 kg)",
            "color": "Carbon Black",
            "ports": "2x Thunderbolt 4, 2x USB-A 3.2, HDMI 2.1",
            "os": "Windows 11 Pro",
            "warranty": "3 year premier support"
        }
    ),
    Product(
        id="laptop-004",
        name="MacBook Air 15-inch M3",
        description="Thin, light, and powerful laptop perfect for students, creative professionals, and business users who need portability. Great for everyday business tasks and creative work.",
        category="Laptops",
        price=1299.99,
        features=[
            "M3 chip with 8-core CPU",
            "15.3-inch Liquid Retina display",
            "16GB unified memory",
            "512GB SSD storage",
            "Up to 18-hour battery life",
            "1080p FaceTime HD camera",
            "Four-speaker sound system",
            "Fanless design"
        ],
        specifications={
            "processor": "Apple M3 (8-core CPU, 10-core GPU)",
            "memory": "16GB unified memory",
            "storage": "512GB SSD",
            "display": "15.3-inch Liquid Retina (2880×1864)",
            "weight": "3.3 lbs (1.51 kg)",
            "color": "Midnight",
            "ports": "2x Thunderbolt 3, MagSafe 3, 3.5mm headphone",
            "os": "macOS Sonoma",
            "warranty": "1 year limited warranty"
        }
    ),
    Product(
        id="laptop-005",
        name="HP Spectre x360 14",
        description="Versatile 2-in-1 laptop that transforms into a tablet. Perfect for business presentations, creative work, and professionals who need flexibility in their workflow.",
        category="Laptops",
        price=1199.99,
        features=[
            "12th Gen Intel Core i7",
            "13.5-inch 3K2K OLED touchscreen",
            "16GB LPDDR4x RAM",
            "1TB PCIe SSD",
            "Intel Iris Xe graphics",
            "360-degree hinge design",
            "HP Rechargeable MPP2.0 Tilt Pen included",
            "Bang & Olufsen speakers"
        ],
        specifications={
            "processor": "Intel Core i7-1255U (10-core)",
            "memory": "16GB LPDDR4x",
            "storage": "1TB PCIe NVMe SSD",
            "display": "13.5-inch 3K2K OLED (3000×2000) touchscreen",
            "weight": "3.01 lbs (1.36 kg)",
            "color": "Nightfall Black",
            "ports": "2x Thunderbolt 4, 1x USB-A 3.2, microSD",
            "os": "Windows 11 Home",
            "warranty": "1 year limited warranty"
        }
    ),
    
    # Gaming Laptops
    Product(
        id="laptop-006",
        name="ASUS ROG Strix G16",
        description="High-performance gaming laptop also suitable for content creation, 3D modeling, and demanding business applications like data analysis and engineering software.",
        category="Laptops",
        price=1599.99,
        features=[
            "13th Gen Intel Core i7-13650HX",
            "16-inch 165Hz QHD display",
            "16GB DDR5 RAM",
            "1TB PCIe SSD",
            "NVIDIA GeForce RTX 4060",
            "RGB backlit keyboard",
            "Advanced cooling system",
            "Wi-Fi 6E connectivity"
        ],
        specifications={
            "processor": "Intel Core i7-13650HX (14-core)",
            "memory": "16GB DDR5-4800",
            "storage": "1TB PCIe NVMe SSD",
            "display": "16-inch QHD (2560×1600) 165Hz",
            "weight": "5.51 lbs (2.5 kg)",
            "color": "Eclipse Gray",
            "graphics": "NVIDIA GeForce RTX 4060 8GB",
            "ports": "1x Thunderbolt 4, 3x USB-A 3.2, HDMI 2.1",
            "os": "Windows 11 Home"
        }
    ),

    # Other Products for context
    Product(
        id="phone-001",
        name="iPhone 15 Pro",
        description="Latest iPhone with titanium design and advanced camera system. Perfect for business professionals who need reliable communication and productivity tools.",
        category="Smartphones",
        price=999.99,
        features=["Titanium design", "A17 Pro chip", "Pro camera system", "Action Button", "USB-C"],
        specifications={
            "processor": "A17 Pro",
            "storage": "128GB",
            "display": "6.1-inch Super Retina XDR",
            "camera": "48MP main, 12MP ultrawide, 12MP telephoto",
            "color": "Natural Titanium"
        }
    ),
    Product(
        id="monitor-001",
        name="Dell UltraSharp 32 4K Monitor",
        description="Professional 4K monitor perfect for business presentations, design work, and productivity. Ideal companion for laptops in office environments.",
        category="Monitors",
        price=749.99,
        features=[
            "32-inch 4K IPS display", 
            "99% sRGB coverage", 
            "USB-C hub functionality", 
            "Height adjustable stand", 
            "VESA mount compatible",
            "Blue light reduction"
        ],
        specifications={
            "size": "32 inches",
            "resolution": "3840 x 2160 (4K UHD)",
            "panel_type": "IPS",
            "color_gamut": "99% sRGB, 95% DCI-P3",
            "connectivity": "USB-C 90W, HDMI 2.1, DisplayPort 1.4",
            "stand": "Height, tilt, swivel, pivot adjustable"
        }
    ),
    Product(
        id="accessory-001",
        name="Logitech MX Master 3S Business",
        description="Professional wireless mouse designed for business productivity and precision work. Perfect companion for laptops and desktop setups.",
        category="Accessories",
        price=99.99,
        features=[
            "MagSpeed electromagnetic scrolling", 
            "Darkfield 8000 DPI sensor", 
            "Multi-device connectivity", 
            "USB-C quick charging", 
            "Quiet click technology",
            "Customizable buttons"
        ],
        specifications={
            "sensor": "Darkfield high precision (200-8000 DPI)",
            "battery": "70 days on full charge",
            "connectivity": "Bluetooth Low Energy, USB receiver",
            "compatibility": "Windows, macOS, Linux, iPadOS",
            "color": "Graphite",
            "weight": "141g"
        }
    ),
    Product(
        id="accessory-002", 
        name="Apple Magic Keyboard with Touch ID",
        description="Wireless keyboard designed for Mac users, perfect for business professionals using MacBook or iMac setups.",
        category="Accessories",
        price=199.99,
        features=[
            "Touch ID for secure authentication",
            "Low-profile scissor mechanism", 
            "Lightning connector charging",
            "Wireless Bluetooth connectivity",
            "Numeric keypad included",
            "Rechargeable battery"
        ],
        specifications={
            "connectivity": "Bluetooth",
            "compatibility": "Mac with Apple silicon or T2 Security Chip",
            "battery": "1 month or more on single charge",
            "color": "White with silver keys",
            "layout": "Full-size with numeric keypad"
        }
    )
]

# Business/Company Information that the chatbot should know
BUSINESS_CONTEXT = """
**TechPro Solutions - Premium Technology Partner**

**About Our Company:**
- We are TechPro Solutions, a leading technology retailer specializing in premium business and professional equipment
- Founded in 2018, we serve businesses, professionals, and tech enthusiasts across North America
- Our mission is to provide cutting-edge technology solutions that empower productivity and innovation
- We partner with top brands like Apple, Dell, HP, Lenovo, ASUS, and more

**Our Specialties:**
- Business laptops and workstations for professionals
- Creative and gaming systems for content creators
- Enterprise solutions for companies and organizations
- Professional accessories and peripherals
- Expert consultation and technical support

**Why Choose TechPro Solutions:**
- Curated selection of premium, professional-grade equipment
- Expert technical consultation and support
- Competitive pricing with business volume discounts
- Extended warranty options and enterprise support
- Same-day delivery in major metropolitan areas
- Dedicated business account managers for corporate clients

**Customer Support:**
- 24/7 technical support hotline
- Live chat support during business hours (9 AM - 8 PM EST)
- On-site support available for enterprise customers
- 30-day return policy with satisfaction guarantee
- Extended warranty options up to 3 years

**Special Services:**
- Corporate bulk pricing for orders over $10,000
- Custom system configuration and setup
- Data migration and setup services
- IT consultation and planning services
- Lease-to-own options for businesses

**Current Promotions:**
- 10% off business laptop bundles (laptop + monitor + accessories)
- Free setup and data migration with laptop purchases over $1,500
- Extended warranty at 50% off for first-time business customers
- Volume discounts starting at 5 units (5% off) up to 50+ units (15% off)
"""

async def populate_database():
    """Populate the database with sample products"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🔄 Adding sample products to the database...")
        
        # Add all products
        success_count = 0
        for product in SAMPLE_PRODUCTS:
            try:
                response = await client.post(
                    f"{base_url}/products",
                    json=product.model_dump()
                )
                if response.status_code == 200:
                    print(f"✅ Added: {product.name}")
                    success_count += 1
                else:
                    print(f"❌ Failed to add {product.name}: {response.text}")
            except Exception as e:
                print(f"❌ Error adding {product.name}: {e}")
        
        print(f"\n🎉 Sample data population completed!")
        print(f"📊 Successfully added {success_count}/{len(SAMPLE_PRODUCTS)} products")
        print(f"\n📝 Business Context Information:")
        print("The chatbot now knows about TechPro Solutions and can answer questions about:")
        print("- Company background and services")
        print("- Product recommendations and comparisons") 
        print("- Business solutions and enterprise options")
        print("- Support and warranty information")
        print("- Current promotions and discounts")

async def test_chat_functionality():
    """Test the chat functionality with sample queries"""
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing chat functionality...")
    
    test_queries = [
        "Tell me about your company",
        "I need a laptop for business use",
        "What's the best laptop for video editing?",
        "Do you have any current promotions?",
        "Can you compare the MacBook Pro and ThinkPad X1?"
    ]
    
    async with httpx.AsyncClient() as client:
        conversation_id = None
        
        for i, query in enumerate(test_queries, 1):
            try:
                request_data = {"message": query}
                if conversation_id:
                    request_data["conversation_id"] = conversation_id
                
                response = await client.post(
                    f"{base_url}/chat",
                    json=request_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    conversation_id = data.get("conversation_id")
                    print(f"✅ Test {i}: Query processed successfully")
                    print(f"   🤖 Response preview: {data['response'][:100]}...")
                    if data.get('suggested_products'):
                        print(f"   💡 Suggested {len(data['suggested_products'])} products")
                else:
                    print(f"❌ Test {i} failed: {response.text}")
                    
            except Exception as e:
                print(f"❌ Test {i} error: {e}")
        
        print(f"\n✅ Chat testing completed with conversation ID: {conversation_id}")

if __name__ == "__main__":
    print("📚 Populating database with comprehensive sample data...")
    print("⚠️  Make sure the API server is running on http://localhost:8000")
    print("\n" + "="*60)
    print(BUSINESS_CONTEXT)
    print("="*60 + "\n")
    
    try:
        asyncio.run(populate_database())
        print("\n🔍 Testing chat functionality...")
        asyncio.run(test_chat_functionality())
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the server is running with: ./run.sh") 
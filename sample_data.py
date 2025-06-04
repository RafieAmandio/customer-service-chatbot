import asyncio
import httpx
from typing import List
from models import Product

# Enhanced product data with Indonesian products and Rupiah pricing
SAMPLE_PRODUCTS = [
    # Laptop - Bisnis & Profesional
    Product(
        id="laptop-001",
        name="MacBook Pro 14-inch M3 Pro",
        description="Laptop premium yang dirancang untuk profesional, pekerjaan kreatif, dan aplikasi bisnis. Sempurna untuk editing video, pengembangan software, dan tugas bisnis yang menuntut performa tinggi.",
        category="Laptop",
        price=30999000.00,  # ~$2000 in IDR
        features=[
            "Chip M3 Pro dengan CPU 12-core", 
            "Layar Liquid Retina XDR 14-inch", 
            "Memori unified 18GB", 
            "Penyimpanan SSD 512GB", 
            "Baterai hingga 18 jam",
            "Port Thunderbolt 4",
            "Kamera FaceTime HD 1080p",
            "Sistem suara enam speaker"
        ],
        specifications={
            "prosesor": "Apple M3 Pro (CPU 12-core, GPU 18-core)",
            "memori": "18GB unified memory",
            "penyimpanan": "512GB SSD",
            "layar": "14-inch Liquid Retina XDR (3024×1964)",
            "berat": "1.6 kg",
            "warna": "Space Gray",
            "port": "3x Thunderbolt 4, HDMI, SDXC, MagSafe 3",
            "os": "macOS Sonoma",
            "garansi": "1 tahun garansi terbatas"
        }
    ),
    Product(
        id="laptop-002",
        name="Dell XPS 13 Plus",
        description="Laptop bisnis ultra-portabel dengan desain premium dan performa tinggi. Ideal untuk profesional bisnis, konsultan, dan eksekutif yang membutuhkan mobilitas tanpa mengorbankan kekuatan.",
        category="Laptop", 
        price=19999000.00,  # ~$1300 in IDR
        features=[
            "Prosesor Intel Core i7 Generasi ke-12",
            "Layar sentuh OLED 4K 13.4-inch", 
            "RAM LPDDR5 16GB",
            "SSD PCIe 512GB",
            "Grafis Intel Iris Xe",
            "Konstruksi aluminium premium",
            "Keyboard backlit",
            "Windows 11 Pro"
        ],
        specifications={
            "prosesor": "Intel Core i7-1280P (14-core)",
            "memori": "16GB LPDDR5",
            "penyimpanan": "512GB PCIe NVMe SSD",
            "layar": "13.4-inch 4K OLED (3840×2400) touchscreen",
            "berat": "1.24 kg",
            "warna": "Platinum Silver",
            "port": "2x Thunderbolt 4, 1x USB-C 3.2",
            "os": "Windows 11 Pro",
            "garansi": "1 tahun ProSupport"
        }
    ),
    Product(
        id="laptop-003",
        name="ThinkPad X1 Carbon Gen 11",
        description="Laptop bisnis legendaris yang dipercaya oleh perusahaan di seluruh dunia. Dibangun untuk eksekutif, konsultan, dan profesional bisnis yang menuntut keandalan, keamanan, dan performa.",
        category="Laptop",
        price=26499000.00,  # ~$1700 in IDR
        features=[
            "Intel Core i7 vPro Generasi ke-13",
            "Layar OLED 2.8K 14-inch",
            "RAM LPDDR5 32GB", 
            "SSD PCIe 1TB",
            "Grafis Intel Iris Xe",
            "Konstruksi serat karbon",
            "Pembaca sidik jari",
            "Kamera IR dengan Windows Hello",
            "Daya tahan tingkat militer"
        ],
        specifications={
            "prosesor": "Intel Core i7-1365U vPro (10-core)",
            "memori": "32GB LPDDR5",
            "penyimpanan": "1TB PCIe NVMe SSD",
            "layar": "14-inch 2.8K OLED (2880×1800)",
            "berat": "1.12 kg",
            "warna": "Carbon Black",
            "port": "2x Thunderbolt 4, 2x USB-A 3.2, HDMI 2.1",
            "os": "Windows 11 Pro",
            "garansi": "3 tahun premier support"
        }
    ),
    Product(
        id="laptop-004",
        name="MacBook Air 15-inch M3",
        description="Laptop tipis, ringan, dan bertenaga sempurna untuk mahasiswa, profesional kreatif, dan pengguna bisnis yang membutuhkan portabilitas. Sangat baik untuk tugas bisnis sehari-hari dan pekerjaan kreatif.",
        category="Laptop",
        price=20299000.00,  # ~$1300 in IDR
        features=[
            "Chip M3 dengan CPU 8-core",
            "Layar Liquid Retina 15.3-inch",
            "Memori unified 16GB",
            "Penyimpanan SSD 512GB",
            "Baterai hingga 18 jam",
            "Kamera FaceTime HD 1080p",
            "Sistem suara empat speaker",
            "Desain tanpa kipas"
        ],
        specifications={
            "prosesor": "Apple M3 (CPU 8-core, GPU 10-core)",
            "memori": "16GB unified memory",
            "penyimpanan": "512GB SSD",
            "layar": "15.3-inch Liquid Retina (2880×1864)",
            "berat": "1.51 kg",
            "warna": "Midnight",
            "port": "2x Thunderbolt 3, MagSafe 3, 3.5mm headphone",
            "os": "macOS Sonoma",
            "garansi": "1 tahun garansi terbatas"
        }
    ),
    Product(
        id="laptop-005",
        name="HP Spectre x360 14",
        description="Laptop 2-in-1 serbaguna yang dapat berubah menjadi tablet. Sempurna untuk presentasi bisnis, pekerjaan kreatif, dan profesional yang membutuhkan fleksibilitas dalam alur kerja mereka.",
        category="Laptop",
        price=18699000.00,  # ~$1200 in IDR
        features=[
            "Intel Core i7 Generasi ke-12",
            "Layar sentuh OLED 3K2K 13.5-inch",
            "RAM LPDDR4x 16GB",
            "SSD PCIe 1TB",
            "Grafis Intel Iris Xe",
            "Desain engsel 360 derajat",
            "HP Rechargeable MPP2.0 Tilt Pen termasuk",
            "Speaker Bang & Olufsen"
        ],
        specifications={
            "prosesor": "Intel Core i7-1255U (10-core)",
            "memori": "16GB LPDDR4x",
            "penyimpanan": "1TB PCIe NVMe SSD",
            "layar": "13.5-inch 3K2K OLED (3000×2000) touchscreen",
            "berat": "1.36 kg",
            "warna": "Nightfall Black",
            "port": "2x Thunderbolt 4, 1x USB-A 3.2, microSD",
            "os": "Windows 11 Home",
            "garansi": "1 tahun garansi terbatas"
        }
    ),
    
    # Laptop Gaming
    Product(
        id="laptop-006",
        name="ASUS ROG Strix G16",
        description="Laptop gaming performa tinggi yang juga cocok untuk pembuatan konten, pemodelan 3D, dan aplikasi bisnis yang menuntut seperti analisis data dan software engineering.",
        category="Laptop",
        price=24999000.00,  # ~$1600 in IDR
        features=[
            "Intel Core i7-13650HX Generasi ke-13",
            "Layar QHD 165Hz 16-inch",
            "RAM DDR5 16GB",
            "SSD PCIe 1TB",
            "NVIDIA GeForce RTX 4060",
            "Keyboard RGB backlit",
            "Sistem pendingin canggih",
            "Konektivitas Wi-Fi 6E"
        ],
        specifications={
            "prosesor": "Intel Core i7-13650HX (14-core)",
            "memori": "16GB DDR5-4800",
            "penyimpanan": "1TB PCIe NVMe SSD",
            "layar": "16-inch QHD (2560×1600) 165Hz",
            "berat": "2.5 kg",
            "warna": "Eclipse Gray",
            "grafis": "NVIDIA GeForce RTX 4060 8GB",
            "port": "1x Thunderbolt 4, 3x USB-A 3.2, HDMI 2.1",
            "os": "Windows 11 Home"
        }
    ),

    # Produk Lainnya
    Product(
        id="phone-001",
        name="iPhone 15 Pro",
        description="iPhone terbaru dengan desain titanium dan sistem kamera canggih. Sempurna untuk profesional bisnis yang membutuhkan komunikasi andal dan alat produktivitas.",
        category="Smartphone",
        price=15499000.00,  # ~$1000 in IDR
        features=["Desain titanium", "Chip A17 Pro", "Sistem kamera Pro", "Tombol Action", "USB-C"],
        specifications={
            "prosesor": "A17 Pro",
            "penyimpanan": "128GB",
            "layar": "6.1-inch Super Retina XDR",
            "kamera": "48MP utama, 12MP ultrawide, 12MP telephoto",
            "warna": "Natural Titanium"
        }
    ),
    Product(
        id="monitor-001",
        name="Dell UltraSharp 32 4K Monitor",
        description="Monitor 4K profesional sempurna untuk presentasi bisnis, pekerjaan desain, dan produktivitas. Pendamping ideal untuk laptop di lingkungan kantor.",
        category="Monitor",
        price=11699000.00,  # ~$750 in IDR
        features=[
            "Layar IPS 4K 32-inch", 
            "Cakupan 99% sRGB", 
            "Fungsi hub USB-C", 
            "Stand dapat disesuaikan tingginya", 
            "Kompatibel mount VESA",
            "Pengurangan cahaya biru"
        ],
        specifications={
            "ukuran": "32 inches",
            "resolusi": "3840 x 2160 (4K UHD)",
            "jenis_panel": "IPS",
            "gamut_warna": "99% sRGB, 95% DCI-P3",
            "konektivitas": "USB-C 90W, HDMI 2.1, DisplayPort 1.4",
            "stand": "Tinggi, kemiringan, putar, pivot dapat disesuaikan"
        }
    ),
    Product(
        id="accessory-001",
        name="Logitech MX Master 3S Business",
        description="Mouse nirkabel profesional yang dirancang untuk produktivitas bisnis dan pekerjaan presisi. Pendamping sempurna untuk laptop dan setup desktop.",
        category="Aksesoris",
        price=1549000.00,  # ~$100 in IDR
        features=[
            "Scroll elektromagnetik MagSpeed", 
            "Sensor Darkfield 8000 DPI", 
            "Konektivitas multi-device", 
            "Pengisian cepat USB-C", 
            "Teknologi klik senyap",
            "Tombol yang dapat dikustomisasi"
        ],
        specifications={
            "sensor": "Darkfield high precision (200-8000 DPI)",
            "baterai": "70 hari dengan sekali pengisian",
            "konektivitas": "Bluetooth Low Energy, USB receiver",
            "kompatibilitas": "Windows, macOS, Linux, iPadOS",
            "warna": "Graphite",
            "berat": "141g"
        }
    ),
    Product(
        id="accessory-002", 
        name="Apple Magic Keyboard dengan Touch ID",
        description="Keyboard nirkabel yang dirancang untuk pengguna Mac, sempurna untuk profesional bisnis yang menggunakan setup MacBook atau iMac.",
        category="Aksesoris",
        price=3099000.00,  # ~$200 in IDR
        features=[
            "Touch ID untuk autentikasi aman",
            "Mekanisme scissor profil rendah", 
            "Pengisian konektor Lightning",
            "Konektivitas Bluetooth nirkabel",
            "Keypad numerik termasuk",
            "Baterai dapat diisi ulang"
        ],
        specifications={
            "konektivitas": "Bluetooth",
            "kompatibilitas": "Mac dengan Apple silicon atau T2 Security Chip",
            "baterai": "1 bulan atau lebih dengan sekali pengisian",
            "warna": "Putih dengan tombol silver",
            "layout": "Ukuran penuh dengan keypad numerik"
        }
    )
]

# Informasi Bisnis/Perusahaan yang harus diketahui chatbot
BUSINESS_CONTEXT = """
**TechPro Solutions Indonesia - Partner Teknologi Premium**

**Tentang Perusahaan Kami:**
- Kami adalah TechPro Solutions Indonesia, retailer teknologi terkemuka yang mengkhususkan diri pada peralatan bisnis dan profesional premium
- Didirikan pada tahun 2018, kami melayani bisnis, profesional, dan penggemar teknologi di seluruh Indonesia
- Misi kami adalah menyediakan solusi teknologi mutakhir yang memberdayakan produktivitas dan inovasi
- Kami bermitra dengan merek-merek terbaik seperti Apple, Dell, HP, Lenovo, ASUS, dan lainnya

**Spesialisasi Kami:**
- Laptop bisnis dan workstation untuk profesional
- Sistem kreatif dan gaming untuk pembuat konten
- Solusi enterprise untuk perusahaan dan organisasi
- Aksesoris dan periferal profesional
- Konsultasi ahli dan dukungan teknis

**Mengapa Memilih TechPro Solutions:**
- Seleksi peralatan berkualitas premium tingkat profesional yang dikurasi
- Konsultasi teknis ahli dan dukungan
- Harga kompetitif dengan diskon volume bisnis
- Opsi garansi diperpanjang dan dukungan enterprise
- Pengiriman hari yang sama di area metropolitan utama
- Manajer akun bisnis khusus untuk klien korporat

**Dukungan Pelanggan:**
- Hotline dukungan teknis 24/7
- Dukungan live chat selama jam kerja (09.00 - 20.00 WIB)
- Dukungan on-site tersedia untuk pelanggan enterprise
- Kebijakan pengembalian 30 hari dengan jaminan kepuasan
- Opsi garansi diperpanjang hingga 3 tahun

**Layanan Khusus:**
- Harga korporat untuk pesanan di atas Rp 150 juta
- Konfigurasi dan setup sistem khusus
- Layanan migrasi data dan setup
- Layanan konsultasi dan perencanaan IT
- Opsi sewa-beli untuk bisnis

**Promosi Terkini:**
- Diskon 10% untuk bundel laptop bisnis (laptop + monitor + aksesoris)
- Setup gratis dan migrasi data untuk pembelian laptop di atas Rp 23 juta
- Garansi diperpanjang 50% off untuk pelanggan bisnis pertama kali
- Diskon volume mulai dari 5 unit (5% off) hingga 50+ unit (15% off)
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
import os
from PIL import Image, ImageDraw, ImageFont

def create_pink_glitter_typography():
    width = 4500
    height = 5400
    
    # Etsy standartlarında tamamen şeffaf arka plan (DTF baskı için kusursuz)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Pink Coquette & Luxury Renk Paleti
    primary_pink = (219, 112, 147, 255)   # Derin ve şık pembe tonu (Medium Violet Red / Gül Kurusu)
    soft_blush = (255, 182, 193, 255)     # Bebek pembesi yansımalar ve ışıltı dolgusu
    accent_rose = (199, 21, 133, 255)     # Kontur ve derinlik tonu
    sparkle_white = (255, 255, 255, 255)  # Parlak yıldızlar
    
    print("Sıfırdan pembe tonlarında zarif tipografi tasarımı oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Font Yükleme Stratejisi: Sistemdeki en şık fontu arar, yoksa varsayılan yüksek kaliteli ölçeklendirme yapar
    font_size = 280
    font = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except Exception:
                continue
                
    if font is None:
        font = ImageFont.load_default()

    # Tasarım Metinleri (İstediğin şık üst üste iki satırlı yapı)
    line1 = "Merry"
    line2 = "Christmas"
    
    # Metinlerin görseldeki gibi estetik konumlandırılması
    # Gönderdiğin görseldeki o uçları kıvrımlı zarif hatları çizimsel vektörlerle destekliyoruz.
    
    # 1. Satır Arka Plan Işıltı Efekti ve Estetik Bant
    draw.rounded_rectangle(
        [center_x - 1700, center_y - 700, center_x + 1700, center_y - 250],
        radius=50, fill=(255, 240, 245, 180), outline=soft_blush, width=10
    )
    
    # 2. Satır Arka Plan Efekti
    draw.rounded_rectangle(
        [center_x - 1900, center_y - 150, center_x + 1900, center_y + 350],
        radius=50, fill=(255, 240, 245, 180), outline=soft_blush, width=10
    )

    # Görseldeki o akıcı, kıvrımlı harf uçlarını (swash) simüle eden sanat çizgileri
    # Üst satır kıvrımları
    draw.arc([center_x - 1500, center_y - 620, center_x - 1100, center_y - 350], start=20, end=200, fill=primary_pink, width=16)
    draw.arc([center_x + 1100, center_y - 620, center_x + 1500, center_y - 350], start=340, end=160, fill=primary_pink, width=16)
    
    # Alt satır kıvrımları
    draw.arc([center_x - 1700, center_y - 80, center_x - 1300, center_y + 200], start=30, end=210, fill=primary_pink, width=16)
    draw.arc([center_x + 1300, center_y - 80, center_x + 1700, center_y + 200], start=330, end=150, fill=primary_pink, width=16)

    # Metin Çizimi (Gölge ve ana renk katmanıyla lüks 3D glitter hissi)
    # 1. Satır Yazı Gölgesi
    draw.text((center_x - 400 + 8, center_y - 520 + 8), line1, fill=accent_rose, font=font)
    # 1. Satır Ana Metin
    draw.text((center_x - 400, center_y - 520), line1, fill=primary_pink, font=font)
    
    # 2. Satır Yazı Gölgesi
    draw.text((center_x - 700 + 8, center_y + 20 + 8), line2, fill=accent_rose, font=font)
    # 2. Satır Ana Metin
    draw.text((center_x - 700, center_y + 20), line2, fill=primary_pink, font=font)

    # Etrafa serpiştirilmiş lüks ışıltılı yıldızlar (Glitter Sparkles)
    sparkles = [
        (center_x - 1400, center_y - 850, 75),
        (center_x + 1450, center_y - 800, 90),
        (center_x - 1600, center_y + 150, 65),
        (center_x + 1550, center_y + 200, 80),
        (center_x - 1200, center_y + 700, 55),
        (center_x + 1200, center_y + 650, 60)
    ]
    
    for sx, sy, ssize in sparkles:
        # Dört kollu şık yıldız
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//3, sy), (sx + ssize, sy), 
            (sx + ssize//3, sy + ssize//3), (sx, sy + ssize), (sx - ssize//3, sy + ssize//3), 
            (sx - ssize, sy), (sx - ssize//3, sy)
        ], fill=sparkle_white)
        # İç parıltı çemberi
        draw.ellipse([sx - ssize//3, sy - ssize//3, sx + ssize//3, sy + ssize//3], fill=soft_blush)

    # Çıktı Klasörü ve Kayıt İşlemi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_pink_glitter_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Pembe tonlarındaki zarif tipografi başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_pink_glitter_typography()

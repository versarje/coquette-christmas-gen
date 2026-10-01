import os
from PIL import Image, ImageDraw, ImageFont

def create_real_script_typography():
    width = 4500
    height = 5400
    
    # Tamamen şeffaf arka plan (DTF baskı ve Etsy için)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # İstediğin Lüks Pembe Renk Paleti
    primary_pink = (214, 90, 127, 255)    # Derin ve çekici gül kurusu / pembe
    shadow_pink = (150, 50, 80, 255)      # Derinlik gölgesi
    sparkle_white = (255, 255, 255, 255)  # Parlak yıldızlar
    
    print("Gerçek kaligrafi fontuyla coquette tasarımı oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Repoya yükleyeceğin script.ttf fontunu yüklüyoruz
    font_path = "script.ttf"
    font_size = 420  # Devasa ve şık görünüm için büyük boyut
    
    if os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        # Eğer font yüklenmediyse hata vermemesi için sistem fontuna düşer
        font = ImageFont.load_default()
        print("UYARI: script.ttf bulunamadı! Lütfen depoya script.ttf fontunu ekleyin.")

    line1 = "Merry"
    line2 = "Christmas"
    
    # Metinlerin kusursuz ortalanması ve çizilmesi (Gölge efektiyle 3D lüks duruş)
    
    # 1. Satır: Merry
    bbox1 = font.getbbox(line1)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    x1 = center_x - (w1 // 2)
    y1 = center_y - 600
    
    # Gölge
    draw.text((x1 + 10, y1 + 10), line1, fill=shadow_pink, font=font)
    # Ana Metin
    draw.text((x1, y1), line1, fill=primary_pink, font=font)

    # 2. Satır: Christmas (Daha da gösterişli olması için biraz daha büyük boyutta)
    font_large = font
    if os.path.exists(font_path):
        font_large = ImageFont.truetype(font_path, 480)
        
    bbox2 = font_large.getbbox(line2)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]
    x2 = center_x - (w2 // 2)
    y2 = center_y + 50
    
    # Gölge
    draw.text((x2 + 12, y2 + 12), line2, fill=shadow_pink, font=font_large)
    # Ana Metin
    draw.text((x2, y2), line2, fill=primary_pink, font=font_large)

    # 3. Etraftaki Etsy Tarzı Işıltılı Yıldız Detayları (Glitter Sparkles)
    def draw_sparkle(d, sx, sy, size):
        # 4 kollu zarif yıldız
        d.polygon([
            (sx, sy - size), (sx + size//4, sy - size//4),
            (sx + size, sy), (sx + size//4, sy + size//4),
            (sx, sy + size), (sx - size//4, sy + size//4),
            (sx - size, sy), (sx - size//4, sy - size//4)
        ], fill=sparkle_white)
        # İç parlama çemberi
        d.ellipse([sx - size//3, sy - size//3, sx + size//3, sy + size//3], fill=(255, 200, 215, 255))

    sparkles = [
        (center_x - 1300, center_y - 750, 95),
        (center_x + 1350, center_y - 700, 110),
        (center_x - 1550, center_y + 100, 85),
        (center_x + 1500, center_y + 150, 100),
        (center_x - 1100, center_y + 750, 75),
        (center_x + 1100, center_y + 700, 80)
    ]
    for sx, sy, ssize in sparkles:
        draw_sparkle(draw, sx, sy, ssize)

    # Çıktı Kaydı
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "pink_christmas_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Gerçek script fontlu tasarım kaydedildi: {file_path}")

if __name__ == "__main__":
    create_real_script_typography()

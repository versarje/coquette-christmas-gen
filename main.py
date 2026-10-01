
import os
import math
from PIL import Image, ImageDraw

def draw_swash_letter_m(draw, x, y, size, color):
    """Zarif kıvrımlı harf detayı (M harfi stili)."""
    # Kıvrımlı şık hatlar
    draw.arc([x, y, x + size, y + size], start=180, end=360, fill=color, width=22)
    draw.line([(x + size//2, y + size//2), (x + size//2, y + size + 100)], fill=color, width=22)
    # Uçlardaki coquette kıvrımları (Swash)
    draw.arc([x - 50, y - 50, x + 50, y + 50], start=0, end=270, fill=color, width=16)

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Metnin üzerindeki zarif Coquette kurdele."""
    left_wing = [
        (center_x, top_y),
        (center_x - bow_width // 2, top_y - bow_height // 2),
        (center_x - bow_width, top_y + bow_height // 3),
        (center_x, top_y + bow_height // 4)
    ]
    right_wing = [
        (center_x, top_y),
        (center_x + bow_width // 2, top_y - bow_height // 2),
        (center_x + bow_width, top_y + bow_height // 3),
        (center_x, top_y + bow_height // 4)
    ]
    draw.polygon(left_wing, fill=color)
    draw.polygon(right_wing, fill=color)
    
    knot_radius = bow_width // 6
    draw.ellipse([center_x - knot_radius, top_y - knot_radius, center_x + knot_radius, top_y + knot_radius], fill=color)
    
    # Sarkan kurdele uçları
    draw.line([(center_x - 20, top_y + 15), (center_x - 140, top_y + 350), (center_x - 100, top_y + 700)], fill=color, width=30)
    draw.line([(center_x + 20, top_y + 15), (center_x + 140, top_y + 350), (center_x + 180, top_y + 700)], fill=color, width=30)

def create_elegant_script_typography():
    width = 4500
    height = 5400
    
    # Etsy standartlarında tamamen şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Pink Coquette & Luxury Renk Paleti (Işıltılı gül kurusu & bebek pembesi)
    deep_rose = (180, 70, 95, 255)       # Ana şık yazı rengi (Derin Gül Kurusu)
    glitter_sparkle = (255, 220, 230, 220) # Işıltılı parlama tonu
    baby_pink = (250, 210, 225, 255)     # Kurdele rengi
    accent_gold = (235, 180, 140, 255)   # Detay renk
    
    print("Zarif kıvrımlı Etsy tipografi tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # 1. Üst Kısıma Coquette Kurdele
    bow_top_y = center_y - 950
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=700, bow_height=280, color=baby_pink)
    
    # 2. "MERRY" Kelimesi Alanı (Zarif script / swash tarzı estetik bant)
    # Arkaya hafif parıltılı lüks bir zemin ekleyelim
    draw.rounded_rectangle(
        [center_x - 1600, center_y - 650, center_x + 1600, center_y - 250],
        radius=60, fill=(255, 248, 247, 210), outline=accent_gold, width=12
    )
    
    # "MERRY" metni için lüks serif/script simülasyonu ve kıvrımlar
    # Harflerin etrafındaki o sanatsal swash (kıvrım) çizgileri
    draw.arc([center_x - 1400, center_y - 580, center_x - 1100, center_y - 350], start=30, end=210, fill=deep_rose, width=18)
    draw.arc([center_x + 1100, center_y - 580, center_x + 1400, center_y - 350], start=330, end=150, fill=deep_rose, width=18)
    
    # 3. "CHRISTMAS" veya "COQUETTE" Kelimesi Alanı (Görseldeki gibi alt alta gösterişli yapı)
    draw.rounded_rectangle(
        [center_x - 1800, center_y - 150, center_x + 1800, center_y + 350],
        radius=60, fill=(255, 248, 247, 210), outline=accent_gold, width=12
    )
    
    # Alt kelime etrafındaki zarif kıvrımlar
    draw.arc([center_x - 1600, center_y - 80, center_x - 1300, center_y + 150], start=40, end=220, fill=deep_rose, width=18)
    draw.arc([center_x + 1300, center_y - 80, center_x + 1600, center_y + 150], start=320, end=140, fill=deep_rose, width=18)

    # 4. Etrafa Işıltılı Glitter / Yıldız Detayları (Etsy satıcılarının favorisi)
    sparkles = [
        (center_x - 1400, center_y - 800, 80),
        (center_x + 1450, center_y - 750, 95),
        (center_x - 1550, center_y + 200, 70),
        (center_x + 1500, center_y + 250, 85),
        (center_x - 1200, center_y + 600, 60),
        (center_x + 1200, center_y + 600, 60)
    ]
    for sx, sy, ssize in sparkles:
        # Şık 4 kollu glitter yıldız
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//4, sy), (sx + ssize, sy), 
            (sx + ssize//4, sy + ssize//4), (sx, sy + ssize), (sx - ssize//4, sy + ssize//4), 
            (sx - ssize, sy), (sx - ssize//4, sy)
        ], fill=(255, 255, 255, 255))
        # İç parıltı
        draw.ellipse([sx - ssize//3, sy - ssize//3, sx + ssize//3, sy + ssize//3], fill=glitter_sparkle)

    # Kayıt İşlemi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_luxury_script_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Zarif tipografi tasarımı başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_elegant_script_typography()

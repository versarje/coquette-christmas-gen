import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Zarif ve büyük Coquette kurdele tasarımı."""
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
    
    knot_radius = bow_width // 5
    draw.ellipse(
        [center_x - knot_radius, top_y - knot_radius, center_x + knot_radius, top_y + knot_radius],
        fill=color
    )
    
    # Uzun ve estetik sarkan kurdele kuyrukları
    draw.line([(center_x - 30, top_y + 20), (center_x - 150, top_y + 400), (center_x - 100, top_y + 800)], fill=color, width=35)
    draw.line([(center_x + 30, top_y + 20), (center_x + 150, top_y + 400), (center_x + 180, top_y + 800)], fill=color, width=35)

def draw_snowflake(draw, x, y, size, color):
    """Etrafına yılbaşı havası katmak için zarif kar taneleri çizer."""
    for i in range(4):
        angle = i * math.pi / 4
        dx = int(size * math.cos(angle))
        dy = int(size * math.sin(angle))
        draw.line([(x - dx, y - dy), (x + dx, y + dy)], fill=color, width=8)

def create_christmas_coquette_disco():
    width = 4500
    height = 5400
    
    # Etsy standartlarına uygun şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Pink Coquette & Christmas Renk Paleti
    baby_pink = (250, 210, 225, 255)     # #FAD2E1 (Kurdele)
    soft_rose = (226, 149, 120, 255)     # #E29578 (Dış Çerçeve)
    silver_base = (216, 226, 220, 255)   # #D8E2DC (Disko Topu Tabanı)
    grid_color = (165, 185, 180, 240)    # Izgara çizgileri
    sparkle_white = (255, 255, 255, 255) # Parlama ve kar taneleri
    
    print("Yılbaşı temalı kusursuz Coquette Disko tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 100
    radius = 900
    
    # 1. Disko Topu Tabanı ve Çerçevesi
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_base,
        outline=soft_rose,
        width=28
    )
    
    # 2. Temiz ve Düzenli Izgara (Ayna Facetleri)
    step = 100
    # Dikey çizgiler (Küre sınırları içinde)
    for x in range(center_x - radius + 80, center_x + radius, step):
        dx = x - center_x
        if abs(dx) < radius:
            h = int(math.sqrt(radius**2 - dx**2))
            draw.line([(x, center_y - h), (x, center_y + h)], fill=grid_color, width=10)
            
    # Yatay çizgiler
    for y in range(center_y - radius + 80, center_y + radius, step):
        dy = y - center_y
        if abs(dy) < radius:
            w = int(math.sqrt(radius**2 - dy**2))
            draw.line([(center_x - w, y), (center_x + w, y)], fill=grid_color, width=10)

    # 3. Üst Kısıma Şık Parlama Efekti (Yumuşak Beyaz Kavis)
    draw.arc(
        [center_x - radius + 150, center_y - radius + 150, center_x + radius - 150, center_y],
        start=180, end=360, fill=(255, 255, 255, 200), width=25
    )

    # 4. Coquette Kurdele (Disko Topunun Üzerine Oturan)
    bow_top_y = center_y - radius - 120
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=700, bow_height=300, color=baby_pink)
    
    # 5. Etrafa Yılbaşı Teması (Kar Taneleri ve Parıltılar)
    # Kar tanesi koordinatları
    snowflakes = [
        (center_x - 1300, center_y - 1000, 70),
        (center_x + 1250, center_y - 900, 90),
        (center_x - 1150, center_y + 800, 60),
        (center_x + 1200, center_y + 700, 80),
        (center_x - 1400, center_y - 100, 50),
        (center_x + 1350, center_y + 100, 65)
    ]
    for sx, sy, ssize in snowflakes:
        draw_snowflake(draw, sx, sy, ssize, sparkle_white)

    # Ekstra Parlak Yıldız Süsleri
    stars = [
        (center_x - 900, center_y - 700),
        (center_x + 950, center_y - 650),
        (center_x - 850, center_y + 500),
        (center_x + 900, center_y + 450)
    ]
    for st_x, st_y in stars:
        draw.polygon([
            (st_x, st_y - 80), (st_x + 20, st_y), (st_x + 80, st_y), 
            (st_x + 20, st_y + 20), (st_x, st_y + 80), (st_x - 20, st_y + 20), 
            (st_x - 80, st_y), (st_x - 20, st_y)
        ], fill=sparkle_white)

    # Kayıt İşlemi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_christmas_disco_bow.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Yılbaşı temalı şeffaf tasarım başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_christmas_coquette_disco()

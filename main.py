import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Disko topunun üzerine zarif bir Coquette kurdele çizer."""
    # Sol kurdele kanadı
    left_wing = [
        (center_x, top_y),
        (center_x - bow_width // 2, top_y - bow_height // 2),
        (center_x - bow_width, top_y + bow_height // 2),
        (center_x, top_y + bow_height // 3)
    ]
    # Sağ kurdele kanadı
    right_wing = [
        (center_x, top_y),
        (center_x + bow_width // 2, top_y - bow_height // 2),
        (center_x + bow_width, top_y + bow_height // 2),
        (center_x, top_y + bow_height // 3)
    ]
    
    draw.polygon(left_wing, fill=color)
    draw.polygon(right_wing, fill=color)
    
    # Kurdele merkezi (düğüm kısmı)
    knot_radius = bow_width // 6
    draw.ellipse(
        [center_x - knot_radius, top_y - knot_radius, center_x + knot_radius, top_y + knot_radius],
        fill=color
    )
    
    # Kurdele sarkıntıları (kuyrukları)
    draw.line([(center_x - 30, top_y + 20), (center_x - 120, top_y + 250)], fill=color, width=25)
    draw.line([(center_x + 30, top_y + 20), (center_x + 120, top_y + 250)], fill=color, width=25)

def create_coquette_christmas_design():
    width = 4500
    height = 5400
    
    # Şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Renk Paleti
    baby_pink = (250, 210, 225, 255)   # #FAD2E1 (Kurdele için)
    soft_rose = (226, 149, 120, 255)   # #E29578
    silver_chrome = (216, 226, 220, 255) # #D8E2DC (Disko topu tabanı)
    sparkle_color = (255, 255, 255, 230) # Parlama efekti
    
    print("Pink Coquette Disko Topu tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 200
    radius = 900
    
    # 1. Disko Topu Gövdesi
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_chrome,
        outline=soft_rose,
        width=20
    )
    
    # Disko topu kare dokusu (Yatay ve dikey çizgiler)
    step = 120
    for x in range(center_x - radius + 100, center_x + radius, step):
        draw.line([(x, center_y - int(math.sqrt(max(0, radius**2 - (x - center_x)**2)))), 
                   (x, center_y + int(math.sqrt(max(0, radius**2 - (x - center_x)**2))))], 
                  fill=(180, 195, 190, 200), width=10)
                  
    for y in range(center_y - radius + 100, center_y + radius, step):
        draw.line([(center_x - int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y), 
                   (center_x + int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y)], 
                  fill=(180, 195, 190, 200), width=10)

    # 2. Üzerine Coquette Kurdele Eklenmesi (Disko topunun tam tepesine)
    bow_top_y = center_y - radius - 50
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=500, bow_height=300, color=baby_pink)
    
    # 3. Çevresine Yıldız / Parıltı Efektleri Eklenmesi
    sparkles = [
        (center_x - 1100, center_y - 800),
        (center_x + 1050, center_y - 700),
        (center_x - 950, center_y + 600),
        (center_x + 1000, center_y + 500)
    ]
    for sx, sy in sparkles:
        draw.polygon([
            (sx, sy - 80), (sx + 20, sy), (sx + 80, sy), 
            (sx + 20, sy + 20), (sx, sy + 80), (sx - 20, sy + 20), 
            (sx - 80, sy), (sx - 20, sy)
        ], fill=sparkle_color)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_disco_bow_1.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Detaylı tasarım başarıyla oluşturuldu: {file_path}")

if __name__ == "__main__":
    create_coquette_christmas_design()

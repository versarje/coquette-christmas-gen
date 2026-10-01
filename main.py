import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Disko topunun üzerine daha büyük, zarif ve uzun sarkıntılı Coquette kurdele çizer."""
    left_wing = [
        (center_x, top_y),
        (center_x - bow_width // 2, top_y - bow_height // 2 - 20),
        (center_x - bow_width, top_y + bow_height // 2),
        (center_x, top_y + bow_height // 3)
    ]
    right_wing = [
        (center_x, top_y),
        (center_x + bow_width // 2, top_y - bow_height // 2 - 20),
        (center_x + bow_width, top_y + bow_height // 2),
        (center_x, top_y + bow_height // 3)
    ]
    
    draw.polygon(left_wing, fill=color)
    draw.polygon(right_wing, fill=color)
    
    # Kurdele merkezi (düğüm kısmı)
    knot_radius = bow_width // 5
    draw.ellipse(
        [center_x - knot_radius, top_y - knot_radius, center_x + knot_radius, top_y + knot_radius],
        fill=color
    )
    
    # Uzun ve sarkık Coquette kurdele kuyrukları
    draw.line([(center_x - 40, top_y + 30), (center_x - 180, top_y + 350)], fill=color, width=35)
    draw.line([(center_x + 40, top_y + 30), (center_x + 180, top_y + 350)], fill=color, width=35)

def create_coquette_christmas_design():
    width = 4500
    height = 5400
    
    # Şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Renk Paleti
    baby_pink = (250, 210, 225, 255)   # #FAD2E1
    soft_rose = (226, 149, 120, 255)   # #E29578
    silver_chrome = (216, 226, 220, 255) # #D8E2DC
    sparkle_color = (255, 255, 255, 240)
    
    print("Geliştirilmiş Pink Coquette Disko Topu tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 200
    radius = 900
    
    # Disko Topu Gövdesi
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_chrome,
        outline=soft_rose,
        width=25
    )
    
    # Disko topu kare dokusu (Daha net çizgiler)
    step = 120
    for x in range(center_x - radius + 100, center_x + radius, step):
        draw.line([(x, center_y - int(math.sqrt(max(0, radius**2 - (x - center_x)**2)))), 
                   (x, center_y + int(math.sqrt(max(0, radius**2 - (x - center_x)**2))))], 
                  fill=(170, 190, 185, 220), width=12)
                  
    for y in range(center_y - radius + 100, center_y + radius, step):
        draw.line([(center_x - int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y), 
                   (center_x + int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y)], 
                  fill=(170, 190, 185, 220), width=12)

    # Coquette Kurdele (Boyutları artırıldı)
    bow_top_y = center_y - radius - 40
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=600, bow_height=350, color=baby_pink)
    
    # Çevresine Yıldız / Parıltı Efektleri
    sparkles = [
        (center_x - 1200, center_y - 900),
        (center_x + 1150, center_y - 800),
        (center_x - 1050, center_y + 700),
        (center_x + 1100, center_y + 600)
    ]
    for sx, sy in sparkles:
        draw.polygon([
            (sx, sy - 100), (sx + 25, sy), (sx + 100, sy), 
            (sx + 25, sy + 25), (sx, sy + 100), (sx - 25, sy + 25), 
            (sx - 100, sy), (sx - 25, sy)
        ], fill=sparkle_color)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_disco_bow_2.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Geliştirilmiş tasarım başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_coquette_christmas_design()

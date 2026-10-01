import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Disko topunun üzerine kusursuz oturan ve sarkan Coquette kurdele çizer."""
    # Kurdele kanatları (Fiyonk kısmı)
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
    
    # Kurdele düğüm merkezi
    knot_radius = bow_width // 5
    draw.ellipse(
        [center_x - knot_radius, top_y - knot_radius, center_x + knot_radius, top_y + knot_radius],
        fill=color
    )
    
    # Aşağı doğru süzülen uzun ve estetik kurdele kuyrukları
    # Sol kuyruk kıvrımı
    draw.line([(center_x - 30, top_y + 20), (center_x - 120, top_y + 250), (center_x - 80, top_y + 400)], fill=color, width=30)
    # Sağ kuyruk kıvrımı
    draw.line([(center_x + 30, top_y + 20), (center_x + 120, top_y + 250), (center_x + 160, top_y + 400)], fill=color, width=30)

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
    
    print("Mükemmelleştirilmiş Pink Coquette Disko Topu tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 200
    radius = 900
    
    # 1. Disko Topu Gövdesi
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_chrome,
        outline=soft_rose,
        width=25
    )
    
    # Disko topu kare dokusu
    step = 120
    for x in range(center_x - radius + 100, center_x + radius, step):
        draw.line([(x, center_y - int(math.sqrt(max(0, radius**2 - (x - center_x)**2)))), 
                   (x, center_y + int(math.sqrt(max(0, radius**2 - (x - center_x)**2))))], 
                  fill=(170, 190, 185, 220), width=12)
                  
    for y in range(center_y - radius + 100, center_y + radius, step):
        draw.line([(center_x - int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y), 
                   (center_x + int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y)], 
                  fill=(170, 190, 185, 220), width=12)

    # 2. Coquette Kurdele (Disko topunun tam üstüne konumlandırıldı)
    bow_top_y = center_y - radius - 150
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=700, bow_height=300, color=baby_pink)
    
    # 3. Çevresine Parıltı Efektleri
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
    
    file_path = os.path.join(output_dir, "coquette_disco_bow_final.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Final tasarım başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_coquette_christmas_design()

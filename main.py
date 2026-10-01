import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
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
    
    draw.line([(center_x - 30, top_y + 20), (center_x - 150, top_y + 400), (center_x - 100, top_y + 800)], fill=color, width=35)
    draw.line([(center_x + 30, top_y + 20), (center_x + 150, top_y + 400), (center_x + 180, top_y + 800)], fill=color, width=35)

def create_transparent_coquette_design():
    width = 4500
    height = 5400
    
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    baby_pink = (250, 210, 225, 255)     # #FAD2E1
    soft_rose = (226, 149, 120, 255)     # #E29578
    silver_chrome = (216, 226, 220, 255) # #D8E2DC
    sparkle_color = (255, 255, 255, 240)
    
    print("Etsy standartlarına uygun şeffaf Coquette tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 100
    radius = 900
    
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_chrome,
        outline=soft_rose,
        width=25
    )
    
    step = 120
    for x in range(center_x - radius + 100, center_x + radius, step):
        draw.line([(x, center_y - int(math.sqrt(max(0, radius**2 - (x - center_x)**2)))), 
                   (x, center_y + int(math.sqrt(max(0, radius**2 - (x - center_x)**2))))], 
                  fill=(170, 190, 185, 220), width=12)
                  
    for y in range(center_y - radius + 100, center_y + radius, step):
        draw.line([(center_x - int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y), 
                   (center_x + int(math.sqrt(max(0, radius**2 - (y - center_y)**2))), y)], 
                  fill=(170, 190, 185, 220), width=12)

    bow_top_y = center_y - radius - 120
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=700, bow_height=300, color=baby_pink)
    
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

    # Mutlak dizin (Absolute path) kullanarak output klasörünü garantiye alıyoruz
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_christmas_disco_bow.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Baskıya hazır şeffaf tasarım başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_transparent_coquette_design()

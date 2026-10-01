import os
import math
from PIL import Image, ImageDraw

def draw_coquette_bow(draw, center_x, top_y, bow_width, bow_height, color):
    """Bayanların çok sevdiği zarif Coquette kurdele tasarımı."""
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

def create_realistic_disco_ball():
    width = 4500
    height = 5400
    
    # Etsy standartlarına uygun şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Pink Coquette ve Krom Renk Paleti
    baby_pink = (250, 210, 225, 255)     # #FAD2E1
    soft_rose = (226, 149, 120, 255)     # #E29578
    sparkle_color = (255, 255, 255, 250)
    
    print("Gerçekçi, 3 boyutlu disko topu tasarımı üretiliyor...")
    
    center_x = width // 2
    center_y = height // 2 + 100
    radius = 900
    
    # 1. Küresel Derinlik İçin Çok Katmanlı Metalik Taban
    # Kenarlardan merkeze doğru yumuşak krom tonları
    for r in range(radius, 0, -15):
        # Küre efekti için dışarıdan içeriye ton değişimi
        factor = r / radius
        gray_val = int(180 + 75 * (1 - factor))
        layer_color = (gray_val, gray_val + 5, gray_val + 10, 255)
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=layer_color
        )

    # Dış Çerçeve (Soft Rose)
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        outline=soft_rose,
        width=25
    )

    # 2. Küresel Kavisli Izgaralar (Ayna Facetleri)
    # Dikey kavisli dilimler (Boylamlar)
    step_deg = 12
    for angle in range(-90, 91, step_deg):
        rad = math.radians(angle)
        x_offset = int(radius * math.sin(rad))
        # Kavisli görünüm için elips yayları veya bükümlü çizgiler simüle ediyoruz
        draw.arc(
            [center_x - abs(x_offset) - 200, center_y - radius, center_x + abs(x_offset) + 200, center_y + radius],
            start=0, end=360, fill=(140, 155, 150, 180), width=10
        )

    # Yatay kavisli kuşaklar (Enlemler)
    step_y = 100
    for y in range(center_y - radius + 100, center_y + radius, step_y):
        # Yüksekliğe göre kavis yarıçapı
        h_factor = abs(y - center_y) / radius
        arc_width_factor = int(radius * math.sqrt(max(0, 1 - h_factor**2)))
        if arc_width_factor > 50:
            draw.ellipse(
                [center_x - arc_width_factor, y - 25, center_x + arc_width_factor, y + 25],
                outline=(140, 155, 150, 180), width=10
            )

    # 3. Üstün Parlaklık / Işık Yansıması (Glossy Highlight)
    # Gerçek bir disko topunun o karakteristik beyaz parlama lekesi
    highlight_box = [center_x - 450, center_y - 650, center_x + 150, center_y - 250]
    draw.ellipse(highlight_box, fill=(255, 255, 255, 160))

    # 4. Coquette Kurdele Eklenmesi
    bow_top_y = center_y - radius - 120
    draw_coquette_bow(draw, center_x, bow_top_y, bow_width=700, bow_height=300, color=baby_pink)
    
    # 5. Etrafa Şık Parıltı Efektleri
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

    # Kayıt İşlemi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "coquette_christmas_disco_bow.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Gerçekçi disko topu tasarımı başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_realistic_disco_ball()

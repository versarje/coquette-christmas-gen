import os
from PIL import Image, ImageDraw, ImageFont

def create_coquette_design():
    width = 4500
    height = 5400
    
    # Tamamen şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Zarif Coquette Renk Paleti
    pink_bg = (255, 230, 238, 220)       # Yumuşak pudra pembe kutu arka planı
    pink_border = (245, 150, 175, 255)   # Şık ince pembe çerçeve
    text_color = (190, 60, 95, 255)      # Derin lüks gül kurusu yazı rengi
    sparkle_color = (255, 255, 255, 255) # Beyaz ışıltılar
    
    print("Profesyonel coquette tasarımı oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Güvenli font seçimi (Sistem fontlarından en kalın ve modern olanı seçer)
    font = None
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 280)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    # 1. Şık ve geniş arka plan rozetleri (Kutuları)
    # Üst Kutu (Merry)
    draw.rounded_rectangle(
        [center_x - 1400, center_y - 550, center_x + 1400, center_y - 200],
        radius=70, fill=pink_bg, outline=pink_border, width=12
    )
    # Alt Kutu (Christmas)
    draw.rounded_rectangle(
        [center_x - 1700, center_y - 50, center_x + 1700, center_y + 300],
        radius=70, fill=pink_bg, outline=pink_border, width=12
    )

    # 2. Metinlerin Kusursuz Yerleşimi (bbox ile tam ortalama)
    line1 = "MERRY"
    line2 = "CHRISTMAS"
    
    # Metin 1 Ölçümü ve Çizimi
    bbox1 = font.getbbox(line1)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    x1 = center_x - (w1 // 2)
    y1 = (center_y - 375) - (h1 // 2)
    draw.text((x1, y1), line1, fill=text_color, font=font)

    # Metin 2 İçin Daha Büyük Font Denemesi (Christmas için)
    font_large = font
    try:
        for path in [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]:
            if os.path.exists(path):
                font_large = ImageFont.truetype(path, 340)
                break
    except Exception:
        pass

    bbox2 = font_large.getbbox(line2)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]
    x2 = center_x - (w2 // 2)
    y2 = (center_y + 125) - (h2 // 2)
    draw.text((x2, y2), line2, fill=text_color, font=font_large)

    # 3. Etraftaki Estetik Parlayan Yıldız Detayları
    def draw_star(d, sx, sy, size):
        d.polygon([
            (sx, sy - size), (sx + size//4, sy - size//4),
            (sx + size, sy), (sx + size//4, sy + size//4),
            (sx, sy + size), (sx - size//4, sy + size//4),
            (sx - size, sy), (sx - size//4, sy - size//4)
        ], fill=sparkle_color)

    stars = [
        (center_x - 1200, center_y - 700, 90),
        (center_x + 1250, center_y - 650, 110),
        (center_x - 1500, center_y + 150, 80),
        (center_x + 1450, center_y + 200, 100),
        (center_x - 900, center_y + 600, 70),
        (center_x + 900, center_y + 550, 75)
    ]
    for sx, sy, ssize in stars:
        draw_star(draw, sx, sy, ssize)

    # Çıktı Kaydı
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "pink_christmas_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Temiz coquette tasarımı başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_coquette_design()

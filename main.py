import os
from PIL import Image, ImageDraw, ImageFont

def create_pure_pink_typography():
    width = 4500
    height = 5400
    
    # Tamamen şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Kadınlar için lüks pembe renk paleti
    deep_pink = (219, 112, 147, 255)      # Gül kurusu / Pembe ana yazı
    soft_glow = (255, 192, 203, 230)      # Yumuşak pembe parıltı
    accent_shadow = (180, 70, 100, 255)   # Derinlik gölgesi
    sparkle_white = (255, 255, 255, 255)  # Beyaz parıltılı yıldızlar
    
    print("Saf pembe tipografi tasarımı oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Font ayarlaması
    font_size = 290
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

    line1 = "Merry"
    line2 = "Christmas"
    
    # Estetik arka plan şık bantlar (Yazıların arkasında duran yumuşak pembe zeminler)
    draw.rounded_rectangle(
        [center_x - 1700, center_y - 650, center_x + 1700, center_y - 200],
        radius=50, fill=(255, 240, 245, 200), outline=soft_glow, width=12
    )
    draw.rounded_rectangle(
        [center_x - 1900, center_y - 100, center_x + 1900, center_y + 400],
        radius=50, fill=(255, 240, 245, 200), outline=soft_glow, width=12
    )

    # Sanatsal kıvrım çizgileri (Swash detayları)
    draw.arc([center_x - 1500, center_y - 570, center_x - 1100, center_y - 300], start=20, end=200, fill=deep_pink, width=18)
    draw.arc([center_x + 1100, center_y - 570, center_x + 1500, center_y - 300], start=340, end=160, fill=deep_pink, width=18)
    draw.arc([center_x - 1700, center_y - 30, center_x - 1300, center_y + 250], start=30, end=210, fill=deep_pink, width=18)
    draw.arc([center_x + 1300, center_y - 30, center_x + 1700, center_y + 250], start=330, end=150, fill=deep_pink, width=18)

    # Metinler (Gölge ve ana katman)
    draw.text((center_x - 380 + 8, center_y - 480 + 8), line1, fill=accent_shadow, font=font)
    draw.text((center_x - 380, center_y - 480), line1, fill=deep_pink, font=font)
    
    draw.text((center_x - 680 + 8, center_y + 60 + 8), line2, fill=accent_shadow, font=font)
    draw.text((center_x - 680, center_y + 60), line2, fill=deep_pink, font=font)

    # Etraftaki ışıltılı yıldızlar
    sparkles = [
        (center_x - 1400, center_y - 800, 80),
        (center_x + 1450, center_y - 750, 95),
        (center_x - 1600, center_y + 200, 70),
        (center_x + 1550, center_y + 250, 85),
        (center_x - 1200, center_y + 750, 60),
        (center_x + 1200, center_y + 700, 65)
    ]
    for sx, sy, ssize in sparkles:
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//3, sy), (sx + ssize, sy), 
            (sx + ssize//3, sy + ssize//3), (sx, sy + ssize), (sx - ssize//3, sy + ssize//3), 
            (sx - ssize, sy), (sx - ssize//3, sy)
        ], fill=sparkle_white)
        draw.ellipse([sx - ssize//3, sy - ssize//3, sx + ssize//3, sy + ssize//3], fill=soft_glow)

    # Çıktı dosya adı tamamen değiştirildi (Eski önbelleğe takılmamak için)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "pink_christmas_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Saf pembe tipografi kaydedildi: {file_path}")

if __name__ == "__main__":
    create_pure_pink_typography()

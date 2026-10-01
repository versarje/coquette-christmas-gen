import os
from PIL import Image, ImageDraw, ImageFont

def create_guaranteed_pink_typography():
    width = 4500
    height = 5400
    
    # Tamamen şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Renk Paleti (Canlı ve net pembe tonları)
    deep_pink = (219, 112, 147, 255)      # Ana pembe
    accent_shadow = (180, 70, 100, 255)   # Gölge
    soft_glow = (255, 192, 203, 220)      # Arka plan yumuşak zemin
    sparkle_white = (255, 255, 255, 255)  # Yıldızlar
    
    print("Garantili pembe tipografi tasarımı oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Font güvenli yükleme (Sistemde font bulamazsa varsayılanı güvenle ölçeklendirir)
    font = None
    try:
        # Standart Linux font yolları
        for path in [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        ]:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 320)
                break
    except Exception:
        pass
        
    if font is None:
        font = ImageFont.load_default()

    line1 = "MERRY"
    line2 = "CHRISTMAS"
    
    # Estetik arkalık bantlar (Yazıların net okunması ve Etsy şıklığı için)
    draw.rounded_rectangle(
        [center_x - 1600, center_y - 600, center_x + 1600, center_y - 180],
        radius=60, fill=(255, 240, 245, 210), outline=soft_glow, width=15
    )
    draw.rounded_rectangle(
        [center_x - 1800, center_y - 50, center_x + 1800, center_y + 370],
        radius=60, fill=(255, 240, 245, 210), outline=soft_glow, width=15
    )

    # Sanatsal kıvrım hatları (Swash detayları)
    draw.arc([center_x - 1400, center_y - 520, center_x - 1000, center_y - 260], start=20, end=200, fill=deep_pink, width=20)
    draw.arc([center_x + 1000, center_y - 520, center_x + 1400, center_y - 260], start=340, end=160, fill=deep_pink, width=20)
    draw.arc([center_x - 1600, center_y + 20, center_x - 1200, center_y + 300], start=30, end=210, fill=deep_pink, width=20)
    draw.arc([center_x + 1200, center_y + 20, center_x + 1600, center_y + 300], start=330, end=140, fill=deep_pink, width=20)

    # Metinlerin kusursuz ortalanarak çizilmesi
    # MERRY
    draw.text((center_x - 520 + 10, center_y - 440 + 10), line1, fill=accent_shadow, font=font)
    draw.text((center_x - 520, center_y - 440), line1, fill=deep_pink, font=font)
    
    # CHRISTMAS
    draw.text((center_x - 980 + 10, center_y + 20 + 10), line2, fill=accent_shadow, font=font)
    draw.text((center_x - 980, center_y + 20), line2, fill=deep_pink, font=font)

    # Etraftaki parıltılı yıldızlar
    sparkles = [
        (center_x - 1300, center_y - 750, 90),
        (center_x + 1350, center_y - 700, 100),
        (center_x - 1500, center_y + 250, 80),
        (center_x + 1450, center_y + 300, 90),
        (center_x - 1100, center_y + 700, 70),
        (center_x + 1100, center_y + 650, 75)
    ]
    for sx, sy, ssize in sparkles:
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//3, sy), (sx + ssize, sy), 
            (sx + ssize//3, sy + ssize//3), (sx, sy + ssize), (sx - ssize//3, sy + ssize//3), 
            (sx - ssize, sy), (sx - ssize//3, sy)
        ], fill=sparkle_white)
        draw.ellipse([sx - ssize//3, sy - ssize//3, sx + ssize//3, sy + ssize//3], fill=soft_glow)

    # Çıktı Kaydı
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "pink_christmas_typography.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Garantili pembe tipografi başarıyla kaydedildi: {file_path}")

if __name__ == "__main__":
    create_guaranteed_pink_typography()

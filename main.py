import os
from PIL import Image, ImageDraw, ImageFont

def generate_merry_christmas_design():
    # Devasa DTF Baskı Boyutu (4500x5400 px, 300 DPI)
    width = 4500
    height = 5400
    
    # Tamamen şeffaf arka plan
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Lüks Gül Kurusu / Pembe Renk Tonu
    text_color = (210, 75, 110, 255)     # Canlı pembe
    shadow_color = (140, 40, 70, 255)    # Derinlik gölgesi
    sparkle_white = (255, 255, 255, 255) # Yıldızlar
    
    print("Merry Christmas tasarımı sıfırdan oluşturuluyor...")
    
    center_x = width // 2
    center_y = height // 2
    
    # Font yükleme (script.ttf varsa onu kullanır, yoksa güvenli varsayılana geçer)
    font_path = "script.ttf"
    font_size = 500
    
    if os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
        print("script.ttf başarıyla yüklendi!")
    else:
        font = ImageFont.load_default()
        print("DİKKAT: script.ttf bulunamadı, varsayılan font kullanılıyor.")

    # Yazılacak Metinler
    line1 = "Merry"
    line2 = "Christmas"
    
    # 1. Satır: Merry
    bbox1 = font.getbbox(line1)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    x1 = center_x - (w1 // 2)
    y1 = center_y - 500
    
    # Gölge ve Ana Metin Çizimi
    draw.text((x1 + 10, y1 + 10), line1, fill=shadow_color, font=font)
    draw.text((x1, y1), line1, fill=text_color, font=font)

    # 2. Satır: Christmas
    bbox2 = font.getbbox(line2)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]
    x2 = center_x - (w2 // 2)
    y2 = center_y + 100
    
    draw.text((x2 + 10, y2 + 10), line2, fill=shadow_color, font=font)
    draw.text((x2, y2), line2, fill=text_color, font=font)

    # Etraftaki Parıltılı Yıldızlar
    sparkles = [
        (center_x - 1200, center_y - 700, 90),
        (center_x + 1250, center_y - 650, 100),
        (center_x - 1400, center_y + 300, 80),
        (center_x + 1350, center_y + 350, 90),
        (center_x - 1000, center_y + 700, 70),
        (center_x + 1000, center_y + 650, 75)
    ]
    for sx, sy, ssize in sparkles:
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//4, sy - ssize//4),
            (sx + size if 'size' in locals() else sx + ssize, sy), (sx + ssize//4, sy + ssize//4),
            (sx, sy + ssize), (sx - ssize//4, sy + ssize//4),
            (sx - ssize, sy), (sx - ssize//4, sy - ssize//4)
        ], fill=sparkle_white) if False else None # Güvenli yıldız çizimi için aşağıdakini kullanalım:
        
    # Yıldızların hatasız çizimi
    for sx, sy, ssize in sparkles:
        draw.polygon([
            (sx, sy - ssize), (sx + ssize//3, sy), (sx + ssize, sy), 
            (sx + ssize//3, sy + ssize//3), (sx, sy + ssize), (sx - ssize//3, sy + ssize//3), 
            (sx - ssize, sy), (sx - ssize//3, sy)
        ], fill=sparkle_white)
        draw.ellipse([sx - ssize//3, sy - ssize//3, sx + ssize//3, sy + ssize//3], fill=(255, 190, 205, 255))

    # Çıktı Kaydı (Yeni ve net isimle kaydediyoruz)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "merry_christmas_pure.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Merry Christmas tasarımı kaydedildi: {file_path}")

if __name__ == "__main__":
    generate_merry_christmas_design()

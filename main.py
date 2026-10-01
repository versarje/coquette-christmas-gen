import os
from PIL import Image, ImageDraw, ImageFont

def create_coquette_christmas_design():
    # Etsy DTF / Tişört baskısı için standart yüksek çözünürlük (300 DPI karşılığı)
    width = 4500
    height = 5400
    
    # Şeffaf arka plana sahip yeni bir görsel oluştur (RGBA)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Belirlediğimiz Coquette & Pastel Renk Paleti (HEX -> RGB)
    baby_pink = (250, 210, 225, 255)   # #FAD2E1
    soft_rose = (226, 149, 120, 255)   # #E29578
    silver_chrome = (216, 226, 220, 255) # #D8E2DC
    cream_white = (253, 240, 237, 255) # #FDF0ED
    
    print("Pink Coquette Christmas tasarım altyapısı başlatıldı...")
    
    # Örnek test çizimi: Disko topu ve kurdele teması için merkez koordinatları
    center_x = width // 2
    center_y = height // 2
    
    # Geçici test çemberi (Disko Topu Gövdesi için yer tutucu)
    radius = 800
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=silver_chrome,
        outline=soft_rose,
        width=30
    )
    
    # Çıktı klasörünü oluştur
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Şeffaf PNG olarak kaydet
    file_path = os.path.join(output_dir, "coquette_disco_sample_1.png")
    img.save(file_path, "PNG", dpi=(300, 300))
    print(f"Tasarım başarıyla oluşturuldu ve kaydedildi: {file_path}")

if __name__ == "__main__":
    create_coquette_christmas_design()

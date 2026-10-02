import os
import glob
import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ColorClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import edge_tts
import asyncio

TEXT_CONTENT = (
    "Mentioned in sacred texts across multiple major religions. "
    "High up on Mount Ararat in Turkey, satellite images captured a strange, boat-shaped anomaly. "
    "Hidden deep beneath thick layers of ice and mud, untouched for centuries. "
    "Roughly 150 meters long, matching the exact dimensions of history's most famous vessel. "
    "Is it just a bizarre coincidence of nature, or the greatest secret frozen right there?"
)

AUDIO_FILE = "voiceover.mp3"
OUTPUT_FILE = "output.mp4"

async def generate_audio():
    print("Ses dosyası oluşturuluyor...")
    communicate = edge_tts.Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    await communicate.save(AUDIO_FILE)
    print("Ses dosyası hazır.")

def get_best_font():
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    for font in candidates:
        if os.path.exists(font):
            return font
    all_ttfs = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
    return all_ttfs[0] if all_ttfs else None

def create_text_image(text, font_path, font_size=50, text_color=(255, 215, 0), max_width=950):
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path and os.path.exists(font_path) else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    wrapped_lines = textwrap.wrap(text, width=25)
    if not wrapped_lines:
        wrapped_lines = [text]

    line_height = font_size + 15
    padding_y = 25
    padding_x = 30
    
    total_height = len(wrapped_lines) * line_height + (padding_y * 2)
    
    # Yarı saydam siyah arka plan kutusu (RGBA formatında, son değer alfa/saydamlık 160)
    img = Image.new("RGBA", (max_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Kutuyu çiz (köşeleri hafif yumuşatılmış veya direkt dikdörtgen)
    draw.rounded_rectangle(
        [(0, 0), (max_width, total_height)], 
        radius=15, 
        fill=(0, 0, 0, 160)
    )

    y_text = padding_y
    for line in wrapped_lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = len(line) * (font_size / 2)
            
        x_text = (max_width - w) / 2
        
        # Yazı rengi ve gölgesi
        draw.text((x_text + 2, y_text + 2), line, font=font, fill=(0, 0, 0, 255))
        draw.text((x_text, y_text), line, font=font, fill=(text_color[0], text_color[1], text_color[2], 255))
        y_text += line_height

    return np.array(img)

def create_video():
    print("Video oluşturuluyor...")
    
    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"{AUDIO_FILE} bulunamadı!")

    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    # Görselleri ayarla
    image_paths = sorted(glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg"))
    if image_paths:
        duration_per_image = total_duration / len(image_paths)
        image_clips = [
            ImageClip(img).with_duration(duration_per_image).resized(width=1080).resized(lambda t: 1.0 + 0.05 * (t / duration_per_image))
            for img in image_paths
        ]
        video_sequence = concatenate_videoclips(image_clips, method="compose")
    else:
        video_sequence = ColorClip(size=(1080, 1920), color=(0, 0, 0)).with_duration(total_duration)
    
    font_path = get_best_font()
    
    # Metni cümlelere bölme
    sentences = [s.strip() for s in TEXT_CONTENT.replace("?", ".").split(".") if s.strip()]
    total_chars = sum(len(s) for s in sentences)
    
    sub_clips = []
    current_time = 0.0
    
    for sentence in sentences:
        duration = (len(sentence) / total_chars) * total_duration
        duration = max(duration, 1.5) # Minimum süre
        
        sub_img_array = create_text_image(sentence, font_path, font_size=50)
        
        sub_clip = (ImageClip(sub_img_array)
                    .with_start(current_time)
                    .with_duration(duration)
                    .with_position(('center', 1050)))
        
        sub_clips.append(sub_clip)
        current_time += duration

    final_video = CompositeVideoClip([video_sequence] + sub_clips).with_audio(audio_clip)
    
    final_video.write_videofile(
        OUTPUT_FILE,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="5M"
    )
    print(f"Video başarıyla oluşturuldu: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    create_video()

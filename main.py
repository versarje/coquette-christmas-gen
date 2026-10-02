import asyncio
import os
import glob
import textwrap
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ColorClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, VideoClip

TEXT_CONTENT = (
    "Mentioned in sacred texts across multiple major religions. "
    "High up on Mount Ararat in Turkey, satellite images captured a strange, boat-shaped anomaly. "
    "Hidden deep beneath thick layers of ice and mud, untouched for centuries. "
    "Roughly 150 meters long, matching the exact dimensions of history's most famous vessel. "
    "Is it just a bizarre coincidence of nature, or the greatest secret frozen right there?"
)

AUDIO_FILE = "voiceover.mp3"
OUTPUT_FILE = "output.mp4"

# Kelime zamanlamalarını tutacağımız liste
word_timestamps = []

async def generate_audio_and_timestamps():
    global word_timestamps
    print("Generating voiceover and word timestamps...")
    
    communicate = edge_tts.Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    
    audio_data = bytearray()
    word_timestamps = []
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            # edge-tts offset ve duration değerlerini 100ns cinsinden verir (saniyeye çevirmek için / 10_000_000)
            start_time = chunk["offset"] / 10_000_000
            duration = chunk["duration"] / 10_000_000
            word = chunk["text"]
            word_timestamps.append({
                "word": word,
                "start": start_time,
                "end": start_time + duration
            })

    with open(AUDIO_FILE, "wb") as f:
        f.write(audio_data)
        
    print(f"Voiceover generated successfully. Total words tracked: {len(word_timestamps)}")

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
    if all_ttfs:
        return all_ttfs[0]
        
    return None

def create_text_image(text, font_path, font_size=55, text_color=(255, 215, 0, 255), bg_color=(0, 0, 0, 160), max_width=950):
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    wrapped_lines = textwrap.wrap(text, width=22)
    if not wrapped_lines:
        wrapped_lines = [text]

    line_height = font_size + 15
    padding_y = 20
    
    total_height = len(wrapped_lines) * line_height + (padding_y * 2)
    total_width = max_width

    img = Image.new("RGBA", (total_width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    y_text = padding_y
    for line in wrapped_lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = len(line) * (font_size / 2)
            
        x_text = (total_width - w) / 2
        
        draw.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += line_height

    return np.array(img)

def create_video():
    print("Creating video with synchronized word-by-word subtitles...")
    
    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"{AUDIO_FILE} bulunamadı!")

    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    # Görselleri otomatik tara ve sırala
    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(ext))
    image_paths.sort()
    
    if image_paths:
        print(f"Bulunan görseller: {image_paths}")
        duration_per_image = total_duration / len(image_paths)
        
        image_clips = []
        for img in image_paths:
            clip = (ImageClip(img)
                    .with_duration(duration_per_image)
                    .resized(width=1080)
                    .resized(lambda t: 1.0 + 0.07 * (t / duration_per_image)))
            image_clips.append(clip)
        
        video_sequence = concatenate_videoclips(image_clips, method="compose")
    else:
        print("Ana dizinde görsel bulunamadı, siyah arka plan kullanılıyor.")
        video_sequence = ColorClip(size=(1080, 1920), color=(0, 0, 0)).with_duration(total_duration)
    
    font_path = get_best_font()
    print(f"Selected font path: {font_path}")

    # Kelime kelime eş zamanlı alt yazı üretimi için VideoClip tabanlı dinamik yapı
    words = word_timestamps if word_timestamps else [{"word": TEXT_CONTENT, "start": 0, "end": total_duration}]
    
    # Her 5-6 kelimede bir alt yazıyı gruplayarak ekranda akıcı görünmesini sağlayalım
    chunk_size = 5
    subtitle_chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join([w["word"] for w in chunk_words])
        start_t = chunk_words[0]["start"]
        end_t = chunk_words[-1]["end"] if i + chunk_size < len(words) else total_duration
        
        # Son kelimenin bitişiyle bir sonraki kelimenin başlangıcına kadar süreyi uzat
        if i + chunk_size < len(words):
            end_t = words[i + chunk_size]["start"]
            
        subtitle_chunks.append({
            "text": chunk_text,
            "start": start_t,
            "end": max(end_t, start_t + 0.5) # Minimum 0.5 saniye ekranda kalma garantisi
        })

    sub_clips = []
    for sub in subtitle_chunks:
        sub_img_array = create_text_image(
            sub["text"], 
            font_path, 
            font_size=55, 
            text_color=(255, 215, 0, 255), 
            bg_color=(0, 0, 0, 160)
        )
        sub_clip = (ImageClip(sub_img_array)
                    .with_start(sub["start"])
                    .with_duration(sub["end"] - sub["start"])
                    .with_position(('center', 1500)))
        sub_clips.append(sub_clip)

    clips = [video_sequence] + sub_clips

    final_video = CompositeVideoClip(clips).with_audio(audio_clip)
    
    final_video.write_videofile(
        OUTPUT_FILE,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="5M"
    )
    print(f"Video successfully created: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_audio_and_timestamps())
    create_video()

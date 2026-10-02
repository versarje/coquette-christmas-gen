import asyncio
import os
import glob
import textwrap
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

TEXT_CONTENT = (
    "Mentioned in sacred texts across multiple major religions. "
    "High up on Mount Ararat in Turkey, satellite images captured a strange, boat-shaped anomaly. "
    "Hidden deep beneath thick layers of ice and mud, untouched for centuries. "
    "Roughly 150 meters long, matching the exact dimensions of history's most famous vessel. "
    "Is it just a bizarre coincidence of nature, or the greatest secret frozen right there?"
)

AUDIO_FILE = "voiceover.mp3"
SUBTITLE_FILE = "subtitles.srt"
OUTPUT_FILE = "output.mp4"

async def generate_audio_and_subtitles():
    print("Generating voiceover and synchronized subtitles via Edge-TTS SubMaker...")
    communicate = edge_tts.Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    
    submaker = edge_tts.SubMaker()
    
    with open(AUDIO_FILE, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    srt_content = submaker.get_srt()
    if not srt_content.strip():
        raise RuntimeError("HATA: SubMaker altyazı verisi üretemedi!")

    with open(SUBTITLE_FILE, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print("Subtitles successfully generated.")

def parse_srt(file_path):
    subtitles = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"HATA: {file_path} dosyası bulunamadı!")
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n\n")
        
    for block in content:
        lines = block.split("\n")
        if len(lines) >= 3:
            time_line = lines[1]
            text_line = " ".join(lines[2:])
            
            if " --> " not in time_line:
                continue
                
            start_str, end_str = time_line.split(" --> ")
            
            def time_to_seconds(t_str):
                parts = t_str.split(":")
                h = int(parts[0])
                m = int(parts[1])
                s_ms = parts[2].replace(".", ",")
                s, ms = s_ms.split(",")
                return h * 3600 + m * 60 + int(s) + int(ms) / 1000
                
            try:
                start_sec = time_to_seconds(start_str)
                end_sec = time_to_seconds(end_str)
                
                subtitles.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": text_line
                })
            except Exception:
                continue
                
    if not subtitles:
        raise ValueError("HATA: SRT dosyası okundu ancak geçerli altyazı satırı bulunamadı!")
            
    return subtitles

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

def create_subtitle_image(text, font_path, font_size=42, max_width=950):
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    wrapped_lines = textwrap.wrap(text, width=34)
    if not wrapped_lines:
        wrapped_lines = [text]

    line_height = font_size + 12
    padding_y = 15
    
    total_height = len(wrapped_lines) * line_height + (padding_y * 2)
    total_width = max_width

    # Yarı saydam siyah arka plan (RGBA)
    img = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 160))
    draw = ImageDraw.Draw(img)

    y_text = padding_y
    for line in wrapped_lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = len(line) * (font_size / 2)
            
        x_text = (total_width - w) / 2
        
        # Altın sarısı harfler (#FFD700)
        draw.text((x_text, y_text), line, font=font, fill=(255, 215, 0, 255))
        y_text += line_height

    return np.array(img)

def create_video():
    print("Creating video with synchronized subtitles and zoom effect...")
    
    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"{AUDIO_FILE} bulunamadı!")

    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    image_paths = [
        "IMG_2047.jpeg",
        "IMG_2048.jpeg",
        "IMG_2049.webp",
        "IMG_2050.jpeg",
        "IMG_2051.jpeg"
    ]
    
    for img in image_paths:
        if not os.path.exists(img):
            raise FileNotFoundError(f"{img} ana dizinde bulunamadı!")

    duration_per_image = total_duration / len(image_paths)
    
    image_clips = []
    for img in image_paths:
        clip = (ImageClip(img)
                .with_duration(duration_per_image)
                .resized(width=1080)
                .resized(lambda t: 1.0 + 0.07 * (t / duration_per_image)))
        image_clips.append(clip)
    
    video_sequence = concatenate_videoclips(image_clips, method="compose")
    
    font_path = get_best_font()
    print(f"Selected font path: {font_path}")

    subs = parse_srt(SUBTITLE_FILE)
    
    subtitle_clips = []
    for sub in subs:
        start_time = sub["start"]
        duration = max(1.0, sub["end"] - start_time)
        text = sub["text"]
        
        sub_img_array = create_subtitle_image(text, font_path)
        
        txt_clip = (ImageClip(sub_img_array)
                    .with_start(start_time)
                    .with_duration(duration)
                    .with_position(('center', 1650)))
        
        subtitle_clips.append(txt_clip)

    final_video = CompositeVideoClip([video_sequence] + subtitle_clips).with_audio(audio_clip)
    
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
    asyncio.run(generate_audio_and_subtitles())
    create_video()

import asyncio
import os
import json
import edge_tts
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

TEXT_CONTENT = (
    "Mentioned in sacred texts across multiple major religions... "
    "High up on Mount Ararat in Turkey, satellite images captured a strange, boat-shaped anomaly. "
    "Hidden deep beneath thick layers of ice and mud, untouched for centuries. "
    "Roughly 150 meters long... matching the exact dimensions of history's most famous vessel. "
    "Is it just a bizarre coincidence of nature... or the greatest secret frozen right there?"
)

AUDIO_FILE = "voiceover.mp3"
OUTPUT_FILE = "output.mp4"
TIMESTAMPS_FILE = "timestamps.json"

async def generate_audio_and_timestamps():
    print("Generating voiceover and word-level timestamps...")
    communicate = edge_tts.Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    
    submaker = edge_tts.SubMaker()
    
    with open(AUDIO_FILE, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    words_data = []
    for start, end, text in submaker.offset:
        words_data.append({
            "start": start / 10000000,
            "end": end / 10000000,
            "word": text
        })
        
    with open(TIMESTAMPS_FILE, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

def create_video():
    print("Creating video with golden subtitles, background boxes, and male voice...")
    
    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"{AUDIO_FILE} bulunamadı!")

    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    image_paths = [
        "IMG_2047.jpeg",
        "IMG_2048.jpeg",
        "IMG_2049.webp",
        "IMG_2050.jpeg",
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
                .resized(width=1080))
        image_clips.append(clip)
    
    video_sequence = concatenate_videoclips(image_clips, method="compose")
    
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "Arial"

    with open(TIMESTAMPS_FILE, "r", encoding="utf-8") as f:
        words_data = json.load(f)

    subtitle_clips = []
    chunk_size = 4
    for i in range(0, len(words_data), chunk_size):
        chunk = words_data[i:i+chunk_size]
        if not chunk:
            continue
            
        chunk_text = " ".join([w["word"] for w in chunk])
        start_time = chunk[0]["start"]
        end_time = chunk[-1]["end"]
        duration = max(0.5, end_time - start_time + 0.3) 
        
        # color='gold' (altın sarısı) olarak ayarlandı
        txt_clip = (TextClip(text=chunk_text,
                             font=font_path,
                             font_size=55,
                             color='gold',
                             bg_color='rgba(0, 0, 0, 0.6)', 
                             margin_top=20,
                             margin_bottom=20,
                             margin_left=30,
                             margin_right=30,
                             method='caption',
                             size=(900, None),
                             text_align='center')
                    .with_start(start_time)
                    .with_duration(duration)
                    .with_position(('center', 1300)))
        
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
    asyncio.run(generate_audio_and_timestamps())
    create_video()

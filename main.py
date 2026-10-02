import asyncio
import os
import edge_tts
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

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
    print("Generating voiceover and subtitles...")
    communicate = edge_tts.Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    
    submaker = edge_tts.SubMaker()
    
    with open(AUDIO_FILE, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open(SUBTITLE_FILE, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())

def parse_srt(file_path):
    subtitles = []
    if not os.path.exists(file_path):
        return subtitles
        
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
                
                # Çok kısa parçaları birleştirmek veya minimum süre vermek için
                subtitles.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": text_line
                })
            except Exception as e:
                continue
            
    return subtitles

def create_video():
    print("Creating video with visible golden subtitles...")
    
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

    subs = parse_srt(SUBTITLE_FILE)
    
    subtitle_clips = []
    for sub in subs:
        start_time = sub["start"]
        duration = max(1.0, sub["end"] - start_time) # Altyazıların ekranda rahat okunması için min 1 saniye süre
        text = sub["text"]
        
        # Yazı rengi altın sarısı (gold), arkasında net okunabilirlik için siyah şerit kutu (bg_color)
        txt_clip = (TextClip(text=text,
                             font=font_path,
                             font_size=50,
                             color='gold',
                             bg_color='black',  # Şeffaflık yerine net siyah kutu ile garanti görünürlük
                             margin_top=15,
                             margin_bottom=15,
                             margin_left=25,
                             margin_right=25,
                             method='caption',
                             size=(950, None),
                             text_align='center')
                    .with_start(start_time)
                    .with_duration(duration)
                    .with_position(('center', 1350)))
        
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

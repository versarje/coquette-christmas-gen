import asyncio
import os
from edge_tts import Communicate
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

async def generate_audio():
    print("Generating voiceover...")
    communicate = Communicate(TEXT_CONTENT, "en-US-AndrewNeural")
    await communicate.save(AUDIO_FILE)

def create_video():
    print("Creating video with resized images, male voice, and subtitles...")
    
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
            raise FileNotFoundError(f"{img} ana dizinde bulunamadı! Lütfen dosya adını kontrol et.")

    duration_per_image = total_duration / len(image_paths)
    
    image_clips = []
    for img in image_paths:
        clip = (ImageClip(img)
                .with_duration(duration_per_image)
                .resized(width=1080))
        image_clips.append(clip)
    
    video_sequence = concatenate_videoclips(image_clips, method="compose")
    
    txt_clip = (TextClip(text=TEXT_CONTENT,
                         font="Arial-Bold",
                         font_size=60,
                         color='white',
                         stroke_color='black',
                         stroke_width=2,
                         size=(1000, None),
                         method='caption',
                         text_align='center')
                .with_duration(total_duration)
                .with_position(('center', 'center')))

    final_video = CompositeVideoClip([video_sequence, txt_clip]).with_audio(audio_clip)
    
        final_video.write_videofile(
        OUTPUT_FILE,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="5M"  # Bit hızını yükseltiyoruz
    )

    print(f"Video successfully created: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    create_video()

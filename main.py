import asyncio
import os
from edge_ts import Communicate
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

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
    communicate = Communicate(TEXT_CONTENT, "en-US-AriaNeural")
    await communicate.save(AUDIO_FILE)

def create_video():
    print("Creating video with 5 images...")
    
    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    # 5 görselin dosya yolları (örneğin assets/1.jpg, assets/2.jpg ... assets/5.jpg)
    image_paths = [
        "assets/1.jpg",
        "assets/2.jpg",
        "assets/3.jpg",
        "assets/4.jpg",
        "assets/5.jpg"
    ]
    
    for img in image_paths:
        if not os.path.exists(img):
            raise FileNotFoundError(f"{img} bulunamadı! Lütfen tüm görselleri assets klasörüne ekle.")

    # Her bir görsele düşen süre (Toplam süreyi 5'e bölüyoruz)
    duration_per_image = total_duration / len(image_paths)
    
    # Görsel kliplerini oluştur ve sürelerini ata
    image_clips = [ImageClip(img).set_duration(duration_per_image) for img in image_paths]
    
    # Görselleri arka arkaya birleştir
    video_sequence = concatenate_videoclips(image_clips, method="compose")
    
    # Ses klibini videoya ekle
    final_video = video_sequence.set_audio(audio_clip)
    
    # Videoyu kaydet (1080x1920 dikey Shorts formatı)
    final_video.write_videofile(
        OUTPUT_FILE,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )
    print(f"Video successfully created: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    create_video()

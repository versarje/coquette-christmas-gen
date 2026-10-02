import asyncio
import os
from edge_tts import Communicate
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
    print("Creating video with 6 images from the root directory...")
    
    audio_clip = AudioFileClip(AUDIO_FILE)
    total_duration = audio_clip.duration
    
    # Ana dizine yüklediğin görsellerin tam dosya adları ve uzantıları
    image_paths = [
        "IMG_2047.jpeg",
        "IMG_2048.jpeg",
        "IMG_2049.webp",
        "IMG_2050.jpeg",
        "IMG_2050.jpeg", # Eğer biri farklıysa burayı güncelleyebilirsin
        "IMG_2051.jpeg"
    ]
    
    for img in image_paths:
        if not os.path.exists(img):
            raise FileNotFoundError(f"{img} ana dizinde bulunamadı! Lütfen dosya adını kontrol et.")

    # Toplam süreyi 6 görsele eşit olarak paylaştırıyoruz
    duration_per_image = total_duration / len(image_paths)
    
    # Görsel kliplerini oluşturuyoruz (webp ve jpeg formatlarını MoviePy destekler)
    image_clips = [ImageClip(img).set_duration(duration_per_image) for img in image_paths]
    
    # Görselleri arka arkaya birleştir
    video_sequence = concatenate_videoclips(image_clips, method="compose")
    
    # Ses klibini videoya ekle
    final_video = video_sequence.set_audio(audio_clip)
    
    # Dikey Shorts formatında kaydet
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

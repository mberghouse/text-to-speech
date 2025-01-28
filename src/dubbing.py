from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import requests
from io import BytesIO
import time

load_dotenv()

client = ElevenLabs()

target_lang = "es"  # Spanish

audio_url = (
    "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3"
)
response = requests.get(audio_url)

audio_data = BytesIO(response.content)
audio_data.name = "audio.mp3"

# Start dubbing
dubbed = client.dubbing.dub_a_video_or_an_audio_file(
    file=audio_data, target_lang=target_lang
)

while True:
    status = client.dubbing.get_dubbing_project_metadata(dubbed.dubbing_id).status
    if status == "dubbed":
        dubbed_file = client.dubbing.get_dubbed_file(dubbed.dubbing_id, target_lang)
        play(dubbed_file)
        break
    else:
        print("Audio is still being dubbed...")
        time.sleep(5)

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import requests
from io import BytesIO

load_dotenv()

client = ElevenLabs()

audio_url = "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/fin.mp3"
response = requests.get(audio_url)
audio_data = BytesIO(response.content)

audio_stream = client.audio_isolation.audio_isolation(audio=audio_data)

play(audio_stream)

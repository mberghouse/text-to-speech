# Audio Processing Suite

A Streamlit application that provides various audio processing capabilities using the ElevenLabs API.

## Features

- **Text to Speech**: Convert text to natural-sounding speech with multiple voice options
  - Direct text input or text file upload
  - Multiple voice options to choose from

- **Voice Changer**: Transform audio using different voice profiles
  - Support for MP3 and WAV files
  - Convert any voice to another voice style

- **Voice Isolator**: Extract clean vocal tracks from audio or video
  - Supports both audio (MP3, WAV) and video (MP4, MOV) files
  - Removes background noise and music

- **Video Dubbing**: Create dubbed versions of videos
  - Upload MP4 or MOV files
  - Add custom dubbing scripts
  - Choose from various voice options

- **Voice Creator**: Generate custom voice previews
  - Create voices using natural language descriptions
  - Generate multiple preview options
  - Test voices with custom text

## Setup

1. Install the required packages:

bash 

pip install streamlit elevenlabs python-dotenv

2. Get your ElevenLabs API key:
   - Sign up at [ElevenLabs](https://elevenlabs.io)
   - Go to your profile settings
   - Copy your API key

3. Set up your environment variable:
   - Create a `.env` file in the project root
   - Add your API key:

bash
ELEVENLABS_API_KEY=your-api-key-here

Or set it directly in your environment:

bash
# Windows (Command Prompt)
set ELEVENLABS_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:ELEVENLABS_API_KEY="your-api-key-here"

# Linux/MacOS
export ELEVENLABS_API_KEY=your-api-key-here

## Running the App

Start the Streamlit app by running:
```bash
streamlit run src/app.py
```

The app will open in your default web browser. Use the sidebar to navigate between different features.

## Usage Notes

- For text-to-speech, you can either type text directly or upload a text file
- Voice changing requires clear audio input for best results
- Voice isolation works best with high-quality audio/video input
- For voice creation, descriptions should be detailed and text must be at least 100 characters
- Video dubbing is an asynchronous process and may take some time to complete

## API Limitations

Features are subject to ElevenLabs API limits based on your subscription tier. Check your API usage and limits in your ElevenLabs dashboard.
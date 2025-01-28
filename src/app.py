import streamlit as st
from elevenlabs.client import ElevenLabs
import tempfile
import os
from pathlib import Path
import base64

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def text_to_speech_page():
    st.header("Text to Speech")
    
    # Text input method selection
    input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
    
    text_input = ""
    if input_method == "Text Input":
        text_input = st.text_area("Enter your text:", height=200)
    else:
        uploaded_file = st.file_uploader("Upload a text file", type=['txt'])
        if uploaded_file:
            text_input = uploaded_file.getvalue().decode("utf-8")
            st.text_area("File contents:", text_input, height=200)

    # Get available voices
    voices_response = client.voices.get_all()
    if not voices_response.voices:  # Access the voices list from the response
        st.error("No voices found. Check your API Key.")
        return

    voice_dict = {voice.name: voice.voice_id for voice in voices_response.voices}
    selected_voice_name = st.selectbox("Choose a voice", list(voice_dict.keys()))

    if st.button("Generate Speech"):
        if not text_input.strip():
            st.warning("Please enter some text or upload a file.")
            return
        
        with st.spinner("Generating audio..."):
            # Convert generator to bytes
            audio_generator = client.text_to_speech.convert(
                text=text_input,
                voice_id=voice_dict[selected_voice_name],
                model_id="eleven_multilingual_v2"
            )
            audio_data = b"".join(audio_generator)
            st.audio(audio_data, format="audio/mp3")
            st.success("Audio generated successfully!")

def voice_changer_page():
    st.header("Voice Changer")
    
    uploaded_file = st.file_uploader("Upload audio file", type=['mp3', 'wav'])
    if uploaded_file:
        voices_response = client.voices.get_all()
        voice_dict = {voice.name: voice.voice_id for voice in voices_response.voices}
        target_voice = st.selectbox("Select target voice", list(voice_dict.keys()))
        
        if st.button("Transform Voice"):
            with st.spinner("Processing audio..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    audio_generator = client.speech_to_speech.convert(
                        voice_id=voice_dict[target_voice],
                        audio=uploaded_file,
                        model_id="eleven_multilingual_sts_v2"
                    )
                    audio_data = b"".join(audio_generator)
                    st.audio(audio_data, format="audio/mp3")
                    st.success("Voice transformed successfully!")
                finally:
                    os.unlink(tmp_path)

def voice_isolator_page():
    st.header("Voice Isolator")
    
    file_type = st.radio("Select file type:", ["Audio", "Video"])
    uploaded_file = st.file_uploader(
        "Upload file", 
        type=['mp3', 'wav'] if file_type == "Audio" else ['mp4', 'mov']
    )
    
    if uploaded_file and st.button("Isolate Voice"):
        with st.spinner("Processing..."):
            audio_generator = client.audio_isolation.audio_isolation(audio=uploaded_file)
            audio_data = b"".join(audio_generator)
            st.audio(audio_data, format="audio/mp3")
            st.success("Voice isolated successfully!")

def dubbing_page():
    st.header("Video Dubbing")
    
    video_file = st.file_uploader("Upload video file", type=['mp4', 'mov'])
    if video_file:
        st.video(video_file)
        
        text_input = st.text_area("Enter the dubbing script:")
        voices_response = client.voices.get_all()
        voice_dict = {voice.name: voice.voice_id for voice in voices_response.voices}
        selected_voice = st.selectbox("Select dubbing voice", list(voice_dict.keys()))
        
        if st.button("Generate Dub"):
            with st.spinner("Processing..."):
                dubbed = client.dubbing.dub_a_video_or_an_audio_file(
                    file=video_file,
                    target_lang="en"  # You might want to make this selectable
                )
                st.success(f"Dubbing started! Project ID: {dubbed.dubbing_id}")
                
                # Note: Dubbing is an asynchronous process, you might want to add
                # a way to check the status and retrieve the result later

def voice_creator_page():
    st.header("Voice Creator")
    
    # Voice description input
    voice_description = st.text_area(
        "Describe the voice you want to create",
        placeholder="Example: A sassy squeaky mouse, A deep-voiced wise old wizard, etc.",
        help="Be as descriptive as possible about the voice characteristics you want"
    )
    
    # Sample text input with longer default text
    default_text = (
        "Every act of kindness, no matter how small, carries value and can make a difference. "
        "In our interconnected world, these moments of compassion ripple outward, touching lives "
        "in ways we may never fully understand. Each smile, each helping hand, each word of "
        "encouragement contributes to a tapestry of positive change that transforms our communities "
        "and uplifts the human spirit."
    )
    
    sample_text = st.text_area(
        "Enter sample text for the voice to speak",
        value=default_text,
        help="Text must be at least 100 characters long"
    )
    
    # Display character count
    char_count = len(sample_text)
    st.caption(f"Character count: {char_count}/100 (minimum required: 100)")
    
    if st.button("Generate Voice Preview"):
        if not voice_description:
            st.warning("Please provide a voice description.")
            return
            
        if char_count < 100:
            st.error("Sample text must be at least 100 characters long.")
            return
            
        with st.spinner("Generating voice previews..."):
            voices = client.text_to_voice.create_previews(
                voice_description=voice_description,
                text=sample_text,
            )
            
            # Display all previews
            for i, preview in enumerate(voices.previews, 1):
                st.subheader(f"Preview {i}")
                audio_bytes = base64.b64decode(preview.audio_base_64)
                st.audio(audio_bytes, format="audio/mp3")
                
                # Add a button to use this voice
                if st.button(f"Use Voice {i}", key=f"use_voice_{i}"):
                    st.info("This would save/select the voice for future use. Implementation needed.")

def main():
    st.title("Audio Processing Suite")
    
    page = st.sidebar.selectbox(
        "Choose a function",
        ["Text to Speech", "Voice Changer", "Voice Isolator", "Video Dubbing", "Voice Creator"]
    )
    
    if page == "Text to Speech":
        text_to_speech_page()
    elif page == "Voice Changer":
        voice_changer_page()
    elif page == "Voice Isolator":
        voice_isolator_page()
    elif page == "Voice Creator":
        voice_creator_page()
    else:
        dubbing_page()

if __name__ == "__main__":
    main()

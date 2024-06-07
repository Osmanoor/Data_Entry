import streamlit as st
import requests
import json

# Deepgram API key
API_KEY = '78991ac3114d0f0dbe2d518c028e1f5bce0a2723'

def transcribe_audio(file):
    headers = {
        'Authorization': f'Token {API_KEY}',
        'Content-Type': 'audio/ogg'  # Adjust this if you're using a different audio format
    }

    response = requests.post(
        'https://api.deepgram.com/v1/listen',
        headers=headers,
        data=file
    )

    if response.status_code == 200:
        result = response.json()
        return result['results']['channels'][0]['alternatives'][0]['transcript']
    else:
        return "Transcription failed."

st.title("Audio Transcription Application")

st.write("Upload an audio file to get the transcription.")

uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    if st.button("Transcribe"):
        with st.spinner('Transcribing...'):
            transcription = transcribe_audio(uploaded_file)
            st.write("Transcription:")
            st.write(transcription)

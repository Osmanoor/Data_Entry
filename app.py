import streamlit as st
import requests
import json
import tempfile

# AssemblyAI API key
API_KEY = '97fc12eb385d474aaddee82c27971132'

def transcribe_audio(audio_file, language_code):
    # Upload audio file to AssemblyAI
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio.seek(0)

    headers = {
        'authorization': API_KEY,
        'content-type': 'application/json'
    }

    upload_response = requests.post(
        'https://api.assemblyai.com/v2/upload',
        headers=headers,
        files={'file': open(temp_audio.name, 'rb')}
    )

    audio_url = upload_response.json()['upload_url']

    # Request transcription
    transcription_request = {
        'audio_url': audio_url,
        'language_code': language_code
    }

    transcription_response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        headers=headers,
        json=transcription_request
    )

    transcript_id = transcription_response.json()['id']

    # Retrieve transcription result
    while True:
        result_response = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers=headers
        )
        result = result_response.json()

        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'failed':
            return "Transcription failed."


st.title("Audio Transcription Application")

st.write("Upload a WAV audio file to get the transcription.")

uploaded_file = st.file_uploader("Choose an audio file...", type=["wav"])

language = st.selectbox("Select the language of the audio", ("en", "ar"))

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    if st.button("Transcribe"):
        with st.spinner('Transcribing...'):
            transcription = transcribe_audio(uploaded_file, language)
            st.write("Transcription:")
            st.write(transcription)

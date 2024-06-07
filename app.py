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

        if result

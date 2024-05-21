import whisper
from langdetect import detect
from pytube import YouTube
from models.response import Response
import os
import tempfile
from io import BytesIO
import subprocess

def convert_yt_to_text(urlYT: str):
    yt = YouTube(urlYT)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_buffer = BytesIO()
    audio_stream.stream_to_buffer(audio_buffer)
    audio_buffer.seek(0)

    # Use ffmpeg to convert the audio buffer to WAV format that whisper can use
    process = subprocess.Popen(
        ["ffmpeg", "-i", "pipe:0", "-f", "wav", "pipe:1"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    wav_data, _ = process.communicate(input=audio_buffer.read())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
        temp_wav_file.write(wav_data)
        temp_wav_file_path = temp_wav_file.name

    # Load the base model and transcribe the audio
    model = whisper.load_model("small")
    result = model.transcribe(temp_wav_file_path)
    transcribed_text = result["text"]
    language = detect(transcribed_text)
    
    # Clean up the temporary file
    os.remove(temp_wav_file_path)
    print(f"Transcribed text: {transcribed_text}")

    return Response(url=urlYT, message=transcribed_text, lang=language).to_dict()

def convert_audio_to_text(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file.save(temp_file.name)

    # Load the base model and transcribe the audio
    model = whisper.load_model("small")
    result = model.transcribe(temp_file.name)
    transcribed_text = result["text"]
    language = detect(transcribed_text)

    os.remove(temp_file.name)

    print(f"Transcribed text: {transcribed_text}")
    return Response(url="", message=transcribed_text, lang=language).to_dict()
import whisper
from langdetect import detect
from pytube import YouTube
from models.response import Response

def convert_yt_to_text(urlYT: str):
    # Create a YouTube object from the URL
    yt = YouTube(urlYT)

    # Get the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream
    output_path = "YoutubeAudios"
    filename = "audio.mp3"
    audio_stream.download(output_path=output_path, filename=filename)

    print(f"Audio downloaded to {output_path}/{filename}")

    # Load the base model and transcribe the audio
    model = whisper.load_model("small")
    result = model.transcribe("YoutubeAudios/audio.mp3")
    transcribed_text = result["text"]
    language = detect(transcribed_text)
    print(f"Transcribed text: {transcribed_text}")
    return Response(url=urlYT, message=transcribed_text, lang=language).to_dict()
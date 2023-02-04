import whisper
import hashlib

from pytube import YouTube
from datetime import timedelta
import os

def download_video(url):
    print("Start downloading", url)
    yt = YouTube(url)

    hash_file = hashlib.md5()
    hash_file.update(yt.title.encode())

    file_name = f'{hash_file.hexdigest()}.mp4'

    yt.streams.first().download("", file_name)
    print("Downloaded to", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }

def transcribe_audio(path):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    video = download_video(path)
    transcribe = model.transcribe(video["file_name"])
    os.remove(video["file_name"])
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srtFilename = os.path.join(r"/Users/michaelhenderson/Desktop/YoutubeWhisperTests/", "test06.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

        txtFilename = os.path.join(r"/Users/michaelhenderson/Desktop/YoutubeWhisperTests/", "test06.txt")
        with open(txtFilename, 'w', encoding='utf-8') as txtFile:
            txtFile.write("".join([segment['text'] for segment in segments]))

    return srtFilename

criticallink = "https://www.youtube.com/watch?v=dh1yF476ZSw"
secondlink = "https://www.youtube.com/watch?v=evfcSvSQ0bE"
link = "https://www.youtube.com/watch?v=OxNsx_wYrw8"
result = transcribe_audio(criticallink)
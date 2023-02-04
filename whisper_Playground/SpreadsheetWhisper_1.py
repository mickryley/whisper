import whisper
import hashlib
import pandas as pd

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


def get_video_info(video_url):
    yt = YouTube(video_url)
    video_title = yt.title
    channel_name = yt.author
    return video_title, channel_name


def transcribe_audio(path):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    video = download_video(path)
    transcribe = model.transcribe(video["file_name"], fp16=False)
    os.remove(video["file_name"])
    segments = transcribe['segments']

    txt_output = "".join([segment['text'] for segment in segments])

    return txt_output

df = pd.read_csv("/Users/michaelhenderson/Desktop/YoutubeWhisperTests/YTQueue.csv")
for index, row in df.iterrows():
    link = row["Video_URL"]
    print("New CSV Row")

    if pd.isna(row["Transcript"]):
        print("No Transcript Found")
        txt_file = transcribe_audio(link)
        df.at[index, "Transcript"] = txt_file
    else:
        print("Transcript Found")
        txt_file = row["Transcript"]
        print(txt_file)

    video_title, channel_name = get_video_info(link)
    df.at[index, "Transcript"] = txt_file
    df.at[index, "Video_Title"] = video_title
    df.at[index, "Channel_Name"] = channel_name
    print("Row Edited")

df.to_csv("/Users/michaelhenderson/Desktop/YoutubeWhisperTests/YTQueueOut.csv", index=False)


from datetime import timedelta
import os
import whisper

def transcribe_audio(path):
    model = whisper.load_model("large") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path, language="Korean")
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srtFilename = os.path.join("/Users/michaelhenderson/Desktop/KoreanWhisperTests/SRT/", f"exportWhisperKorean.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

def translate_audio(path):
    model = whisper.load_model("large") # Change this to your desired model
    print("Whisper model loaded.")
    translate = model.transcribe(audio=path, task="translate", language="Korean")
    segments = translate['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srtFilename = os.path.join("/Users/michaelhenderson/Desktop/KoreanWhisperTests/SRT/", f"exportWhisperEnglish.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

filepath = "/Users/michaelhenderson/Desktop/KoreanWhisperTests/WhisperAudio.wav"

result = translate_audio(filepath)
result = transcribe_audio(filepath)


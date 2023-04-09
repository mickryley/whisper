import whisper
#file dialogue reqs
import tkinter as tk
from tkinter import filedialog

model = whisper.load_model("base")

#Input# Open a file browser and ask the user to select the input file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

with open(file_path, "rb") as file:

# load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    

# print the recognized text
print(result.text)

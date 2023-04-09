
from datetime import timedelta
import time
import os
import whisper

#file dialogue reqs input
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
#prompt dropdown input
import pyinputplus as pyip


def transcribe_audio(path, _language, _model):
    
    progressLabel.config(text="Loading Whisper model for Transcription")
    languageRoot.update_idletasks()
    time.sleep(1)
    model = whisper.load_model(_model) # Change this to your desired model
    print("Whisper model loaded.")
    progressLabel.config(text="Transcription model loaded! Transcription in Progress...")
    languageRoot.update_idletasks()
    time.sleep(1)
    transcribe = model.transcribe(audio=path, language=_language, fp16=False)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        pathRoot, pathExt = os.path.splitext(path)
       
        srtScribeFilename = pathRoot + "_" + _language + f"_Scribe.srt"
        if os.path.exists(srtScribeFilename):
            os.remove(srtScribeFilename)
        with open(srtScribeFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    progressLabel.config(text="Transcription Complete!")
    transcribeLabel.config(text="Transcription: " + srtScribeFilename)
    languageRoot.update_idletasks()
    time.sleep(1)
    return srtScribeFilename

def translate_audio(path, _language, _model):

    progressLabel.config(text="Loading Whisper model for Translation")
    languageRoot.update_idletasks()
    time.sleep(1)
    model = whisper.load_model(_model) # Change this to your desired model
    print("Whisper model loaded.")
    progressLabel.config(text="Translation model loaded! Translation in Progress...")
    languageRoot.update_idletasks()
    time.sleep(1)
    translate = model.transcribe(audio=path, task="translate", language=_language, fp16=False)
    segments = translate['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"
        pathRoot, pathExt = os.path.splitext(path)
        srtSlateFilename = pathRoot + "_" + _language + f"_Slate.srt"
        if os.path.exists(srtSlateFilename):
            os.remove(srtSlateFilename)
        with open(srtSlateFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    progressLabel.config(text="Translation Complete!")
    translateLabel.config(text="Translation: " + srtSlateFilename)
    languageRoot.update_idletasks()
    time.sleep(1)
    return srtSlateFilename

#Input# Open a file browser and ask the user to select the input file
##root = tk.Tk()
##root.withdraw()


file_path = ""

#def selection_callback(event):
 #   print(selected_language.get())
languageRoot = tk.Tk()
languageRoot.title("Whisper SRT Generator")


def browse_file():
    languageRoot.update_idletasks()
    global file_path 
    file_path = filedialog.askopenfilename()
    fileAddlabel.config(text=file_path)
    languageRoot.update_idletasks()
    print("File Path is: " + file_path)
    ##languageRoot.mainloop()

frame = ttk.Frame(languageRoot, width=1280, height=640)
##frame.pack(pady=20, padx=20)
frame.grid(columnspan=3, rowspan=7, pady=20, padx=20)

file_button = tk.Button(languageRoot, text="Change Selected File (Video/Audio)", command=browse_file)
##file_button.grid(row=0, column=1, pady=5)
file_button.grid(row=0, columnspan=3, pady=5, padx=50)

filelabel = ttk.Label(frame, text="Selected File:")
filelabel.grid(row=1, column=0, sticky='W', pady=50)

fileAddlabel = ttk.Label(frame, text=file_path)
fileAddlabel.grid(row=1, column=1, sticky='W', pady=50)

label = ttk.Label(frame, text="What language is the video/audio?")
language_options = ["Korean", "English"]
selected_language = tk.StringVar()
selected_language.set(language_options[0])

label.grid(row=2, column=0, sticky='W', pady=5)

language_dropdown = ttk.Combobox(frame, textvariable=selected_language, values=language_options, state="readonly")
language_dropdown.grid(row=2, column=1, pady=5)

secondLabel = ttk.Label(frame, text="What model size do you want to use?")
model_options = ["tiny", "base", "large"]
selected_model = tk.StringVar()
selected_model.set(model_options[0])

secondLabel.grid(row=3, column=0, sticky='W', pady=5)

model_dropdown = ttk.Combobox(frame, textvariable=selected_model, values=model_options, state="readonly")
model_dropdown.grid(row=3, column=1, pady=5)

def run_code():
  
    run_button.config(text="Whispering... Please Wait...", state="disabled")
    progressLabel.config(text="Initialising...")
    languageRoot.update_idletasks()
    time.sleep(1)

    print("File Path is: " + file_path)

    with open(file_path, "rb") as file:
        if(selected_language.get() == "Korean"):
            progressLabel.config(text="Beginning Translation (to English)...")
            translateLabel.config(text="Translating...")
            languageRoot.update_idletasks()
            time.sleep(1)
            result = translate_audio(file_path, selected_language.get(), selected_model.get())
        else:
            translateLabel.config(text="No Translation Required")
        
        progressLabel.config(text="Beginning Transcription...")
        transcribeLabel.config(text='Transcribing...')
        languageRoot.update_idletasks()
        time.sleep(1)
        result = transcribe_audio(file_path, selected_language.get(), selected_model.get())
    
    progressLabel.config(text="Whisper Complete! Press 'Shift-Q' to exit!")
    run_button.config(text="Start", state="normal")
    languageRoot.update_idletasks()
    
    #languageRoot.quit()



translateLabel = ttk.Label(frame, text="")
translateLabel.grid(row=4, columnspan=3, pady=5, padx=20)

transcribeLabel = ttk.Label(frame, text="")
transcribeLabel.grid(row=5, columnspan=3, pady=5, padx=20)

progressLabel = ttk.Label(frame, text="")
progressLabel.grid(row=6, columnspan=3, pady=5, padx=20)

run_button = tk.Button(languageRoot, text="Start", command=run_code)
run_button.grid(row=7, columnspan=3, pady=5, padx=50)

languageRoot.bind('Escape', lambda e: quit())
languageRoot.bind('Q', lambda e: quit())


##file_path = filedialog.askopenfilename()

languageRoot.update_idletasks()

browse_file()

##languageRoot.protocol("WM_DELETE_WINDOW", quit())

##def nope():
  ##  print("Window Close Pressed")

##languageRoot.protocol("WM_DELETE_WINDOW", nope())


languageRoot.mainloop()

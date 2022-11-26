from asyncio.windows_events import NULL
from fpdf import FPDF
import pyaudio
import wave
import json
import nltk
import os
import sounddevice as sd
import soundfile as sf

import pyttsx3
import apiai as sr
import speech_recognition as sr

from google.cloud import speech
from gtts import gTTS
from playsound import playsound

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

#initializes the cloud speech to text client
client = speech.SpeechClient.from_service_account_file('venv\\key.json')

samplerate = 44100  # Hertz
duration = 3  # seconds
filename = 'output.wav'

converter = pyttsx3.init()
# Can be more than 100
converter.setProperty('rate', 200)
# Set volume 0-1
converter.setProperty('volume', 0.5)

r = sr.Recognizer()
r.energy_threshold = 4000
r.dynamic_energy_threshold = True

# function records audio for sentence analytics.
# For now, this will have a static listening time of 3 seconds until
# a more intuitive usage is found
#returns type ndarray of sounddevice
def recordAudio():
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=2, blocking=True)
    return mydata

#this function accesses the google sppech to text api
# then returns the transcript from the audio recording
#returns a string
#IndexError thrown if nothing is said
def transcribeAudio():
    wrongRead = True
    audio = 0
    while wrongRead:
        print("You may speak now......")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, .25)
            audio = r.listen(source)
        # name = transcribeAudio(data, "output.wav")
        try:
            name = r.recognize_google(audio)
            wrongRead = False
        except:
            textToAudio("Could Not Recognize what you said, try again")
            #converter.runAndWait()
    
    return name

#this function will convert the text to audio, then also play the audio
def textToAudio(transcript):
    converter.say(transcript)
    print(transcript)
    converter.runAndWait()

def wordAnalyzer(word):
    typeOfSpeech = set()
    for data in wn.synsets(word):
        if data.name().split('.')[0] == word:
            typeOfSpeech.add(data.pos())
    return (typeOfSpeech)


def turnArrToPDF(storyArr):
    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Courier', 'B', 16)
    pdf.cell(0, 10, 'Story:', 0, 1)
    pdf.set_font('Times', '', 12)
    for i in range(0, len(storyArr)):
        pdf.cell(0, 10, storyArr[i], 0, 1)
    pdf.output('Users_Story.pdf', 'F')

def word_count(string):
    # Here we are removing the spaces from start and end,
    # and breaking every word whenever we encounter a space
    # and storing them in a list. The len of the list is the
    # total count of words.
    return(len(string.strip().split(" ")))

def helpPage():
    return "Say \"Finish Story\" to export the story you have into a pdf file. Say \"Read Story\" to be able to hear the story you have made so far. Saying \"Help\" takes you to this screen so you can see the commands. If you are hearing this prior to starting the game, then you wont be able to read or finish the story, as I have not began reading it to you. The game will continue now from your current point"

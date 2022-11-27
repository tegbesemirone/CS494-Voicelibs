from asyncio.windows_events import NULL
from fpdf import FPDF
import json
import nltk
import os

import pyttsx3
import apiai as sr
import speech_recognition as sr

from google.cloud import speech

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

#parameters for converter. Can be changed
converter = pyttsx3.init()
converter.setProperty('rate', 220)
converter.setProperty('volume', 0.5)

r = sr.Recognizer()
Lem = WordNetLemmatizer()

#this function accesses the google sppech to text api
# then returns the transcript from the audio recording
#returns a string
#IndexError thrown if nothing is said
def transcribeAudio():
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    wrongRead = True
    audio = 0
    while wrongRead:
        print("You may speak now......")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, .25)
            audio = r.listen(source)
        try:
            name = r.recognize_google(audio)
            wrongRead = False
        except:
            textToAudio("Could Not Recognize what you said, try again")
    
    return name

#this function will convert the text to audio, then also play the audio
def textToAudio(transcript):
    converter.say(transcript)
    print(transcript)
    converter.runAndWait()

#returns the set of wordtypes a word can be. Analyzes without context of prior sentence
def wordAnalyzer(word):
    typeOfSpeech = set()
    lemword = Lem.lemmatize(word)

    for data in wn.synsets(lemword):
        if data.name().split('.')[0] == lemword:
            typeOfSpeech.add(data.pos())
    return (typeOfSpeech)


# turns the current story into a pdf file that is then exported
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

# Here we are removing the spaces from start and end,
# and breaking every word whenever we encounter a space
# and storing them in a list. The len of the list is the
# total count of words.
def word_count(string):
    return(len(string.strip().split(" ")))

#returns help screen. 
def helpPage():
    return "Say \"Finish Story\" to export the story you have into a pdf file. Say \"Read Story\" to be able to hear the story you have made so far. Saying \"Help\" takes you to this screen so you can see the commands. If you are hearing this prior to starting the game, then you wont be able to read or finish the story, as I have not began reading it to you. The game will continue now from your current point"

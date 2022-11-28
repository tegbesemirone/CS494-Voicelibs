from asyncio.windows_events import NULL
from fpdf import FPDF
import json
import nltk
import ssl
import os

import pyttsx3
import apiai as sr
import speech_recognition as sr

from google.cloud import speech

#this helps with nltk downloads on macOS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

#parameters for converter. Can be changed
converter = pyttsx3.init()


r = sr.Recognizer()
Lem = WordNetLemmatizer()

#this function accesses the google sppech to text api
# then returns the transcript from the audio recording
#returns a string
#IndexError thrown if nothing is said
def transcribeAudio():
    
    r.dynamic_energy_threshold = True
    wrongRead = True
    audio = 0
    while wrongRead:
        r.energy_threshold = 400
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
    converter.setProperty('rate', 200)
    converter.setProperty('volume', 0.5)
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

#reads out current story
def readStory(newMadlib):
    story = ""
    for a in newMadlib:
        story += a
    textToAudio(story)

#reads out the help screen 
def helpPage():
    textToAudio("This is the Voice-Libs help page. Voice-libs is a take on mad-libs, the phrasal template word game, except instead of writing words, you can just say them!")
    textToAudio("Throughout the game, you can ask me to read your story, and I'll read out your current story. If you ever want to finish the story, just ask me to finish your story, and i'll export it to a pdf for you!")
    textToAudio("If you need to listen to something again, just ask me to repeat what I just said, and I'll recite the last line for you.")
    textToAudio("Otherwise, I will assume the one word phrases you mention are entries for the game. I will now resume from the current play state, if you need to hear this again, just ask for help.")

#reads out intro audio for game
def introAudio(userName):
    textToAudio("Hello " + userName + " Welcome to Voice-libs, a phrasel template word game, that you can controll with just your voice.")
    textToAudio("While I read the story to you, i'll add blanks in each section of the sentence for you to replace, then i will give you some time to give me a response.")
    #textToAudio("I will now take you to the help page, to familiarize you with some of the commands I can accept.")
    #helpPage()
    textToAudio("I'll also tell you what type of word I need, whether it's a noun, verb, or adjective. If you need additional help, just ask for it. Do you understand?")

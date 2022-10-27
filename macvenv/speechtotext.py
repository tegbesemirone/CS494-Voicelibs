from fpdf import FPDF
import json
import nltk
import os
import sounddevice as sd
import soundfile as sf

from google.cloud import speech
from gtts import gTTS
from playsound import playsound
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

#initializes the cloud speech to text client
client = speech.SpeechClient.from_service_account_file('macvenv/key.json')

samplerate = 44100  # Hertz
duration = 3  # seconds
filename = 'output.wav'

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
def transcribeAudio(mydata, filename):
    sf.write(filename, mydata, samplerate)

    with open(filename, 'rb') as f:
        mp3_data = f.read()

    audio_file = speech.RecognitionAudio(content=mp3_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code='en-US',
        audio_channel_count=2
    )

    response = client.recognize(
        config=config,
        audio=audio_file
    )

    # This segment of code converts the json string to a json object

    json_file = type(response).to_json(response)
    wjdata = json.loads(json_file)

    # Static call to transcript will always be wjdata['results'][0]['alternatives'][0]['transcript']
    try:
        transcript = str(wjdata['results'][0]['alternatives'][0]['transcript'])
    except:
        textToAudio("I did not hear anything from the user")
        transcript = " "

    # converts the text string from the transcript to mp3 audio

    return transcript #return audio object

#this function will convert the text to audio, then also play the audio
def textToAudio(transcript):
    myObj = gTTS(text=transcript,lang='en', slow=False)
    myObj.save('tester3.mp3')
    print(transcript)
    playsound('tester3.mp3')
    os.remove('tester3.mp3')

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

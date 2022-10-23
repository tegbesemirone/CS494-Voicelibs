import pyaudio
import wave
import json
import os
import sounddevice as sd
import soundfile as sf
from google.cloud import speech
from gtts import gTTS

#initializes the cloud speech to text client
client = speech.SpeechClient.from_service_account_file('key.json')

samplerate = 44100  # Hertz
duration = 5  # seconds
filename = 'output.wav'

#mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
#                channels=2, blocking=True)


# function records audio for sentence analytics.
# For now, this will have a static listening time of 5 seconds until
# a more intuitive usage is found
#returns type ndarray of sounddevice
def recordAudio():
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=2, blocking=True)
    return mydata

#this function accesses the google sppech to text api
# then returns the transcript from the audio recording
#returns a string
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
    transcript = str(wjdata['results'][0]['alternatives'][0]['transcript'])

    # converts the text string from the transcript to mp3 audio
    #myObj = gTTS(text=wjdata['results'][0]['alternatives'][0]['transcript'], lang='en', slow=False)
    return transcript #return audio object




#myObj.save("tester.mp3")

#os.system("start tester.mp3")
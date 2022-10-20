import pyaudio
import wave
import json
import os
from google.cloud import speech
from gtts import gTTS

#initializes the cloud speech to text client
client = speech.SpeechClient.from_service_account_file('key.json')

#initializes the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
frames = []

# this loop records audio input from the user
try:
    while True:
        data = stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass
#ends of audio recroding
stream.stop_stream()
stream.close()
audio.terminate()

#transcribes audio into .wav file
sound_file = wave.open("myrecording.wav","wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()

file_name = "myrecording.wav"

with open(file_name, 'rb') as f:
    mp3_data = f.read()

audio_file = speech.RecognitionAudio(content=mp3_data)

config = speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US'
)

response = client.recognize(
    config=config,
    audio=audio_file
)

json_file = type(response).to_json(response)
wjdata = json.loads(json_file)
print(wjdata['results'][0]['alternatives'][0]['transcript'])
myObj = gTTS(text=wjdata['results'][0]['alternatives'][0]['transcript'], lang='en', slow=False)

myObj.save("tester.mp3")

os.system("start tester.mp3")
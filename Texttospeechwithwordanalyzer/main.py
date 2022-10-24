from speechtotext import *


def main():
    #print(wordAnalyzer("love")) prints a set of the possible types of parts of speech
    textToAudio("Hello, what is your name?")
    data = recordAudio()
    name = transcribeAudio(data, "output.wav")
    textToAudio("Hello "+ name)


if __name__ == '__main__':
    main()
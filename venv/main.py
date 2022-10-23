from speechtotext import *


def main():
    textToAudio("Hello, what is your name?")
    data = recordAudio()
    name = transcribeAudio(data, "output.wav")
    textToAudio("Hello "+ name)


if __name__ == '__main__':
    main()
from speechtotext import *

print("Hello")

print("__name__ value: ", __name__)


def main():
    textToAudio("Hello, what is your name?")
    data = recordAudio()
    name = transcribeAudio(data, "output.wav")
    textToAudio("Hello "+ name)


if __name__ == '__main__':
    main()
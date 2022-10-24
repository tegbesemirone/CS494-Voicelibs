from speechtotext import *


def main():
    #Example on How To Use turnArrToPDF
    arr = ["This is the story", "Then this happened", "Now we are here", "The End", "--- this was the end", "el fin", "no seriously this be done", "Ok", "bye", "hello world"]
    turnArrToPDF(arr)
    #Example on How to use wordAnalyzer
    print(wordAnalyzer("love"))
    #textToAudio("Hello, what is your name?")
    #data = recordAudio()
    #name = transcribeAudio(data, "output.wav")
    #textToAudio("Hello "+ name)


if __name__ == '__main__':
    main()

from flask import Flask, render_template
import speech_recognition as sr
import pyttsx3


app = Flask(__name__)

currMadlib = ["Once upon a blank, in a kingdom far, far away ", ", there lived a blank princess. ",
"Princess blank was loved by everyone ", "in the kingdom of blank-shire, ", "whether they were members of the royal blank, ", "Knights of the blank Table, ",
"or blank vendors in the town square. ", "Even the blank farmers who lived ","far outisde the tall castle blank adored her!"]
newMadlib = []
wordtype = [". can you say a noun please", " please say an adjective to discribe the princess",
 ". say a silly word, needs to be a noun", ". say an animal", ". Mention a place, a noun of course", ". give me a descriptive adjective please",
  ". give a noun for what the vendors are selling", ". mention a food the farmers are growing", ". give a plural noun"]
wordMatch = ['n', 'a', 'n', 'n', 'n', 'a', 'n', 'n', 'n']
wordAlt = ['n', 's','n','n','n', 's', 'n', 'n', 'n']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story')
def story():
    return render_template('story.html')
@app.route('/about')
def about():
    return render_template('about.html')
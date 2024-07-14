import speech_recognition as sr
from gtts import gTTS
import os
from flask import Flask, render_template, request

import openai

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
        print("You said: " + response)
        return response
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "API unavailable."

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")


openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_recipe(ingredients):
    prompt = f"Suggest a recipe using the following ingredients: {ingredients}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def get_cooking_instructions(recipe_name):
    prompt = f"Provide step-by-step cooking instructions for {recipe_name}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe_route():
    ingredients = request.form['ingredients']
    recipe = get_recipe(ingredients)
    return render_template('recipe.html', recipe=recipe)

@app.route('/get_instructions', methods=['POST'])
def get_instructions_route():
    recipe_name = request.form['recipe_name']
    instructions = get_cooking_instructions(recipe_name)
    return render_template('instructions.html', instructions=instructions)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000)

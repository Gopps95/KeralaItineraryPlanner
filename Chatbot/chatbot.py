from flask import Flask, request, jsonify
import random
import json
import nltk
import pickle
import numpy as np
<<<<<<< HEAD
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from flask_cors import CORS
=======
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import requests
>>>>>>> f937a280e0c2187a592a7b11cdaae72bfe503cf2

app = Flask(__name__)
CORS(app)

# Load necessary resources
lemmatizer = WordNetLemmatizer()
<<<<<<< HEAD
intents = json.loads(open('D:/College/S8/Major/Code/KeralaItineraryPlanner/Chatbot/intents.json').read())  # Adjust the path accordingly
=======
intents = json.loads(open(r'C:\Users\ALEENA\Desktop\project\KeralaItineraryPlanner\Chatbot\intents.json').read())
>>>>>>> f937a280e0c2187a592a7b11cdaae72bfe503cf2

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.h5')

<<<<<<< HEAD
# Functions to preprocess input and generate responses
=======
>>>>>>> f937a280e0c2187a592a7b11cdaae72bfe503cf2
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

<<<<<<< HEAD
# Define API endpoints
@app.route('/api/chatbot', methods=['POST', 'GET'])
def chatbot():
    if request.method == 'GET':
        return "Chatbot API is up and running."
    if request.method == 'OPTIONS':
        return '', 200  # Empty response for OPTIONS request
    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        message = data['message']
        
        # Predict the intent of the user's message
        intents_list = predict_class(message)
        
        # Get a response based on the predicted intent
        response = get_response(intents_list, intents)
        
        # Return the response as JSON
        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)  # You can set debug=False for production
=======
def weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key=3ae3dea5a8864fd6bf2140701230606&q={city}"
    r = requests.get(url)
    weather_data = json.loads(r.text)
    temperature = weather_data['current']['temp_c']
    return f"The Temperature of {city} is {temperature}"

print("GO! Bot is running")

while True:
    message = input("")
    if message.startswith("What is the weather in "):
        city = message[23:]
        print(weather(city))
    else:
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)
>>>>>>> f937a280e0c2187a592a7b11cdaae72bfe503cf2

from random import choice
from json import loads
from pickle import load
from numpy import array
from time import strftime
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# lemmatizer instantiation
lemmatizer = WordNetLemmatizer()

# storing the json file as a dictionary
intents = loads(open('./Seri/intents.json').read())

# storing the data into its variable
words = load(open('./Seri/words.pkl', 'rb'))
classes = load(open('./Seri/classes.pkl', 'rb'))
model = load_model('./Seri/Seri_model.h5')


# lemmatizing the sentence
class Chatbot():
    def __init__(self):
        pass

    def clean_up_sentence(self, sentence):
        sentence_words = word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
        # returns list of words in a sentence
        return sentence_words

    # checking if the word is in the bag of words using 0's and 1's
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for w in sentence_words:
            for i, word in enumerate(words):
                if word == w:
                    bag[i] = 1
        return array(bag)

    # probability of the class
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = model.predict(array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        # storing [index, class]
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        # sorting the probability in reverse order: highest probability first
        results.sort(key=lambda x: x[1], reverse=True)
        self.return_list = []
        for r in results:
            self.return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        return self.return_list

    # getting response from the data
    def get_response(self, intent_list, intent_json):
        self.result = ''
        tag = intent_list[0]['intent']
        list_of_intents = intent_json['intents']

        for i in list_of_intents:
            if tag == 'date':
                day = strftime("%A")
                date = strftime("%B %d %Y")
                self.result = f"Today is {day}, {date}"
                break

            elif tag == 'time':
                time_today = strftime("%I: %M %p")
                self.result = f"It is {time_today}."
                break

            elif i['tag'] == tag:
                self.result = choice(i['responses'])
                break
        return self.result

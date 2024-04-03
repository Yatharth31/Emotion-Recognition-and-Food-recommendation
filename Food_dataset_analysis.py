import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
import seaborn as sns
from plotly.offline import init_notebook_mode, plot
# init_notebook_mode()
from collections import Counter
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
stop = set(stopwords)
stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', ''])
from nltk.stem import WordNetLemmatizer

import Food_dictionary

food_data = pd.read_csv('food_choices - food_choices.csv')
# print(food_data.info())

def search_comfort(mood):
    lemmatizer = WordNetLemmatizer()
    foodcount = {}
    for i in range(148):
        temp = [temps.strip().replace('.', '').replace(',', '').lower() for temps in
                str(food_data["comfort_food_reasons"][i]).split(' ') if temps.strip() not in stop]
        if mood in temp:
            foodtemp = [lemmatizer.lemmatize(temps.strip().replace('.', '').replace(',', '').lower()) for temps in
                        str(food_data["comfort_food"][i]).split(',') if temps.strip() not in stop]
            for a in foodtemp:
                if a not in foodcount.keys():
                    foodcount[a] = 1
                else:
                    foodcount[a] += 1
    sorted_food = []
    sorted_food = sorted(foodcount, key=foodcount.get, reverse=True)
    return sorted_food


def find_my_comfort_food(mood):
    topn = []
    topn = search_comfort(mood)  # function create dictionary only for particular mood
    print("3 popular comfort foods in %s are:" % (mood))
    if(len(topn)==0):
        # topn.append(Food_dictionary.comfort_food)
        for item in Food_dictionary.comfort_food:
            topn.append(item)
    print(topn)
    return topn



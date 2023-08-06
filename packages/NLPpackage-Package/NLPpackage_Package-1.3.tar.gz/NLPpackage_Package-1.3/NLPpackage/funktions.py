# import libraries

import numpy as np
import pandas as pd
import csv
from sqlalchemy import create_engine
import sqlite3
import pickle
import joblib

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize, TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download ('punkt')
nltk.download ('stopwords')
nltk.download ('wordnet')

tknzr = TweetTokenizer ()
import re



def split_categories(cat_file):
    '''
        This function is not used, it could be removed.
        But it was intended to get the categories separated.
        Maybe it has some use and so I'll kept it.
    '''

    cat_split = cat_file['categories'].str.split (';', expand = True)
    i = 0
    cat3 = []
    del cat3
    cat3 = cat_split
    while i < cat_split.shape[1]:
        cat_split2 = cat_split[i].str.split ('-', expand = True)
        category = cat_split2 [0].iloc [1]
        cat = str('_cat')
        cat_split2.rename(columns= {1: category + cat}, inplace = True)
        cat3 = cat3.merge (cat_split2[(category + cat)].astype(int), left_index = True, right_index = True)
        i += 1
    categories = cat3
    categories_names = ['related_cat', 'request_cat', 'offer_cat', 'aid_related_cat',
     'medical_help_cat', 'medical_products_cat', 'search_and_rescue_cat', 'security_cat',
     'military_cat', 'child_alone_cat', 'water_cat', 'food_cat', 'shelter_cat',
     'clothing_cat', 'money_cat', 'missing_people_cat', 'refugees_cat', 'death_cat', 'other_aid_cat',
     'infrastructure_related_cat', 'transport_cat', 'buildings_cat', 'electricity_cat', 'tools_cat',
     'hospitals_cat', 'shops_cat', 'aid_centers_cat', 'other_infrastructure_cat', 'weather_related_cat',
     'floods_cat', 'storm_cat', 'fire_cat', 'earthquake_cat', 'cold_cat', 'other_weather_cat', 'direct_report_cat']
    categories = categories [categories_names]
    return categories, categories_names

def tokenize (tweet):

    '''
        Decided to take a lemmatizer - sometimes the lemmatized words make no sence,
        but they can be connected and that is the main thing...
    '''

    tweet = re.sub(r"[^a-zA-Z0-9?#-]", " ", tweet.lower())
    tweet = tknzr.tokenize(tweet)
    tweet = [WordNetLemmatizer().lemmatize (a) for a in tweet]
    tweet = [word for word in tweet if word not in stopwords.words('english')]
    return tweet

def dummies (tokenize):

    '''
        aktually no need of this funtion because it is a pandas module!!!
    '''
    test = pd.get_dummies(tokenize).sum (axis = 0)
    return test


def get_predictions (in_arg):

    '''
        loading in the classifier,
        and get the predictions on each category.

        function works with the non optimized / standard parameters.
    '''

    filename = './Models/finalized_model.sav'
    dt_model = joblib.load(filename)
    predictions = dt_model.predict ([in_arg])
    predictions = pd.DataFrame (predictions)

    predictions.rename (columns = {0: 'related',
     1: 'request', 2: 'offer', 3: 'aid related',
     4: 'medical help', 5: 'medical products',
     6: 'search and rescue', 7:'security',
     8: 'military', 9:'child alone',
     10: 'water', 11: 'food', 12: 'shelter',
     13: 'clothing', 14: 'money', 15: 'missing people',
     16: 'refugees', 17: 'death', 18: 'other aid',
     19: 'infrastructure related', 20: 'transport',
     21: 'buildings', 22: 'electricity', 23: 'tools',
     24: 'hospitals', 25: 'shops', 26: 'aid centers',
     27: 'other infrastructure', 28: 'weather related',
     29: 'floods', 30: 'storm', 31: 'fire',
     32: 'earthquake', 33: 'cold',
     34: 'other weather', 35: 'direct report'}, inplace = True)

    sumation = predictions.sum (axis = 1)
    print (sumation)
    result = pd.DataFrame(predictions)
    return result

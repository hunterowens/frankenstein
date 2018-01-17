"""
Makes and returns the trained Sentiment extration models
"""

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import pickle
def catagorize(row):
    """
    apply function to catagorize a set of traing data values into 
    catagories. 
    """
    sentiment = row['Sentiment']
    focus = row['Focus'] 
    energy_level = row['Energy Level']
    if sentiment > 0:
        if focus > 0: # focus outward
            if energy_level > .25:
                return "connected"
            elif energy_level < -.25:
                return "tolerant"
            else:
                return "vunerable"
        else: # focus inward
            if energy_level > .25:
                return "hopeful" 
            elif energy_level < -.25:
                return "calm" 
            else:
                return "happy"
    elif sentiment <= 0:
        if focus > 0: #focus outward
            if energy_level > .25:
                return "angry"
            elif energy_level < -.25:
                return "lonely" 
            else:
                return "guarded"
        else: #focus inward 
            if energy_level > .25:
                return  "anxious" 
            elif energy_level < -.25:
                return "sad"
            else:
                return "fearful"

def stemming_tokenizer(text):
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]

def train(classifier, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print("Accuracy: %s" % classifier.score(X_test, y_test))
    return classifier

def generate_model(data):
    """
    Generates the cataogrization model
    """
    le = preprocessing.LabelEncoder()
    le.fit(data['cat'])
    data['target'] = le.transform(data['cat'])
    trial = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer,
                                 stop_words=stopwords.words('english') + list(string.punctuation))),
        ('classifier', MultinomialNB(alpha=0.5)),
    ])

    t= train(trial, data['Text'], data['target'])
    return t, le

if __name__ == '__main__':
    data  = pd.read_csv('./sentiment/training_data.csv', skiprows=[1])
    data['cat'] = data.apply(catagorize, axis = 1)
    t, le = generate_model(data)
    pickle.dump(t, open('saved/cat_model.p', 'wb'))
    pickle.dump(le, open('saved/classes.p', 'wb'))

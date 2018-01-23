"""
Makes and returns the trained Sentiment extration models
"""

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import os
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import markovify
import joblib 

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
        ('vectorizer', TfidfVectorizer()), 
        ('classifier', MultinomialNB(alpha=0.5)),
    ])

    t= train(trial, data['Text'], data['target'])
    return t, le

def gen_markov(fp,lines):
    """
    Generates a markov model and saves to /saved/
    """
    print('making ', fp)
    try:
        m = markovify.Text("\n".join(lines))
    except KeyError:
        print("Couldn't make model for ", fp)
        return 
    joblib.dump(m, open(fp, 'wb'))
    print('saved ', fp)
    return m

if __name__ == '__main__':
    from api import db, Sentence, Sentence_Shelly
    data  = pd.read_csv('./sentiment/training_data.csv', skiprows=[1])
    data['cat'] = data.apply(catagorize, axis = 1)
    t, le = generate_model(data)
    joblib.dump(t, open('saved/cat_model.p', 'wb'))
    joblib.dump(le.classes_, open('saved/classes.p', 'wb'))
    # Fakenstein Markov
    with open('./data/fakenstein.txt') as f:
        text = f.read()
    lines = text.split('\n')
    if not os.path.exists('./saved/cat_data.p'):
        cat_data = {k: [] for k in le.classes_}
        from tqdm import tqdm
        for line in tqdm(lines):
            cat = le.classes_[t.predict([line])][0]
            s = Sentence(text=line, cat = cat) 
            cat_data[cat].append(line)
            db.session.add(s)
        db.session.commit()
        joblib.dump(cat_data, open('./saved/cat_data.p', 'wb')) 
    else:
        cat_data = joblib.load(open('./saved/cat_data.p','rb'))
    
    # actual frankenstein
    print("actually frankenstein now")
    with open('./data/frankenstein_org.txt') as f:
        text = f.read()
    lines = text.split('\n')
    from tqdm import tqdm
    for line in tqdm(lines):
        cat = le.classes_[t.predict([line])][0]
        s = Sentence_Shelly(text=line, cat = cat) 
        db.session.add(s)
    
    for key in cat_data.keys():
        gen_markov('./saved/faken-markov/' + key + '.p', cat_data[key])
    # Questions Markov
    questions = pd.read_csv('./questions.csv', header=None)
    cat_questions = {k: [] for k in le.classes_}
    for q in questions[0].tolist():
        cat = le.classes_[t.predict([q])][0]
        cat_questions[cat].append(q)
    for key in cat_questions.keys():
        gen_markov('./saved/faken-questions/' + key + '.p', cat_questions[key])

    


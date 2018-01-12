# coding: utf-8
get_ipython().magic('ls ')
get_ipython().magic('run sentiment.py')
data = load_data.py
import pandas as pd
pd.read_csv('./training_data.csv'
'
)
pd.read_csv('./training_data.csv', skiprows=1)
data = pd.read_csv('./training_data.csv', skiprows=1)
get_ipython().magic('ls ')
data.keys()
data = pd.read_csv('./training_data.csv', skiprows=[1])
data.keys()
data['sentiment_cat'] = data['Sentiment'].apply(lambda x: "Positive" if x > 0 else "Negative")
data['sentiment_cat']
from sklearn.datasets import fetch_20newsgroups
news = fetch_20newsgroups(subset='all')
from sklearn.cross_validation import train_test_split
def train(classifier, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print "Accuracy: %s" % classifier.score(X_test, y_test)
    return classifier
from sklearn.cross_validation import train_test_split
def train(classifier, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print "Accuracy: %s" % classifier.score(X_test, y_test)
    return classifier
def train(classifier, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print("Accuracy: %s" % classifier.score(X_test, y_test))
    return classifier
from sklearn.cross_validation import train_test_splitfrom sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
trial1 = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB()),
])
train(trial1, news.data, news.target)
trial1
trial1.fit
trial1.fit()
train(trial1, news.data, news.target)
train(trial1, news.data, news.target)
t= train(trial1, news.data, news.target)
news.data
news.data[0]
news.target
news.target
data.keys
data.keys()
t= train(trial1, data['Text'], data['Sentiment'])
t= train(trial1, data['Text'], data['Sentiment'].values())
t= train(trial1, data['Text'], data['Sentiment'].values)
news.target
data['Sentiment'].value
data['Sentiment'].values
news.target
type(news.target)
type(data['Sentiment'].values)
t= train(trial1, data['Text'], data['Sentiment'].values)
t= train(trial1, news.data, news.target)
get_ipython().magic('ls ')
data.target = data['sentiment_cat'].apply(lambda x: 1 if "Positive" else 2)
data.target
t= train(trial1, data['Text'], data['Target'])
t= train(trial1, data['Text'], data['target'])
t= train(trial1, data['Text'], data.target)
data.target
data['target']
data['sentiment_cat'].apply(lambda x: 1 if "Positive" else 2)
data['sentiment_cat']
data['sentiment_cat'].apply(lambda x: 1 if "Positive" else 2)
data['sentiment_cat'].apply(lambda x: 1 if x == "Positive" else 2)
data['target'] data['sentiment_cat'].apply(lambda x: 1 if x == "Positive" else 2)
data['target']=  data['sentiment_cat'].apply(lambda x: 1 if x == "Positive" else 2)
t= train(trial1, data['Text'], data.target)
t= train(trial1, data['Text'], data['target)
]
t= train(trial1, data['Text'], data['target'])
trial2 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
    ('classifier', MultinomialNB()),
])
from nltk.corpus import stopwords
trial2 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
    ('classifier', MultinomialNB()),
])
t= train(trial2, data['Text'], data['target'])
trial3 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
    ('classifier', MultinomialNB(alpha=0.05)),
])
t= train(trial3, data['Text'], data['target'])
t= train(trial3, data['Text'], data['target'])
trial3 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
    ('classifier', MultinomialNB(alpha=0.5)),
])
t= train(trial3, data['Text'], data['target'])
trial4 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'),
                             min_df=5)),
    ('classifier', MultinomialNB(alpha=0.05)),
])
trial4 = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'),
                             min_df=5)),
    ('classifier', MultinomialNB(alpha=0.5)),
])
t= train(trial4, data['Text'], data['target'])
t= train(trial3, data['Text'], data['target'])
import string
from nltk.stem import PorterStemmer
from nltk import word_tokenize
def stemming_tokenizer(text):
        stemmer = PorterStemmer()
        return [stemmer.stem(w) for w in word_tokenize(text)]
 
trial5 = Pipeline([
    ('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer,
                             stop_words=stopwords.words('english') + list(string.punctuation))),
    ('classifier', MultinomialNB(alpha=0.05)),
])
trial5 = Pipeline([
    ('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer,
                             stop_words=stopwords.words('english') + list(string.punctuation))),
    ('classifier', MultinomialNB(alpha=0.5)),
])
t= train(trial3, data['Text'], data['target'])
t= train(trial5, data['Text'], data['target'])
get_ipython().magic('history')
get_ipython().magic('save test.py')

import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
import pickle

data = pd.read_csv('./sentiment/training_data.csv', skiprows=[1])

trial = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('regression', linear_model.LinearRegression()),
])

def train(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    model.fit(X_train, y_train)
    return model

def main():
    m_senti = train(trial, data['Text'], data['Sentiment'])

    #Energy
    m_energy = train(trial, data['Text'], data['Energy Level'])

    # focus
    m_focus = train(trial, data['Text'], data['Focus'])
    
    pickle.dump(m_senti, open('./saved/m_senti.p','wb'))
    pickle.dump(m_energy, open('./saved/m_energy.p','wb'))
    pickle.dump(m_focus, open('./saved/m_focus.p','wb'))

if __name__ == '__main__':
    print("making scoring models")
    main()


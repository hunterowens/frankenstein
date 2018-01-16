"""
Makes and returns the trained Sentiment extration models
"""

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

def load_data():
    return pd.read_csv('./training_data.csv', skiprows=[1])

def catagorize(row):
    """
    apply function to catagorize a set of traing data values into 
    catagories. 
    """
    sentiment = 0
    focus = 0 
    energy_level = 0 ## TODO replace with real
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


def generate_model():
    # Generate counts from text using a vectorizer.  There are other vectorizers available, and lots of options you can set.
    # This performs our step of computing word counts.
    vectorizer = CountVectorizer(stop_words='english')
    train_features = vectorizer.fit_transform([r[0] for r in reviews])
    test_features = vectorizer.transform([r[0] for r in test])

    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, and the existing classifications in the training set.
    nb = MultinomialNB()
    nb.fit(train_features, [int(r[1]) for r in reviews])

    # Now we can use the model to predict classifications for our test features.
    predictions = nb.predict(test_features)

    # Compute the error.  It is slightly different from our model because the internals of this process work differently from our implementation.
    fpr, tpr, thresholds = metrics.roc_curve(actual, predictions, pos_label=1)
    print("Multinomial naive bayes AUC: {0}".format(metrics.auc(fpr, tpr)))

if __name__ == '__main__':
    pass

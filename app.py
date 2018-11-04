import flask
import sqlite3
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime 
import os
import joblib
import pandas as pd
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
import nltk 
from nltk import word_tokenize
from nltk.corpus import stopwords
import itertools

from flask_alembic import Alembic
import enum

alembic = Alembic()
app = Flask(__name__)
alembic.init_app(app)
print("Database URL: ", os.environ.get('DATABASE_URL', 'postgresql://hunterowens:@localhost/frankenstein'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://hunterowens:@localhost/frankenstein')
db = SQLAlchemy(app)

class StatusEnum(enum.Enum):
    preshow = 'preshow'
    in_progress = 'in_progress'
    complete = 'complete'


class ShowRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(StatusEnum))
    act = db.Column(db.Integer)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sentiment = db.Column(db.Float)
    focus = db.Column(db.Float)
    energy = db.Column(db.Float)
    text = db.Column(db.String(5000))
    showrun = db.Column(db.Integer, db.ForeignKey('show_run.id')) 
    

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    data = db.Column(db.JSON)
    showrun = db.Column(db.Integer, db.ForeignKey('show_run.id'))

class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    text = db.Column(db.String(5000))
    cat = db.Column(db.String(50))
    showrun = db.Column(db.Integer, db.ForeignKey('show_run.id'))

class Sentence_Shelly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    text = db.Column(db.String(5000))
    cat = db.Column(db.String(50))
    showrun = db.Column(db.Integer, db.ForeignKey('show_run.id'))

def tokenize_nltk(text):
    """
    Note: 	This function imports a list of custom stopwords from the user
        If the user does not modify custom stopwords (default=[]),
        there is no substantive update to the stopwords.
    """
    tokens = word_tokenize(text)
    text = nltk.Text(tokens)
    stop_words = set(stopwords.words('english'))
    # stop_words.update(custom_stopwords)
    words = [w.lower() for w in text if w.isalpha() and w.lower() not in stop_words]
    return words

@app.route('/')
def test():
    """
    fake home                 
    """
    return jsonify({'data': "api_online"})

@app.route('/start-show')
def start_show():
    """
    starts a show by saving it in the intial state in the db
    ret: dict of show. 
    """
    show = ShowRun(status='preshow')
    db.session.add(show)
    db.session.commit()
    return jsonify({'data': [{'show_id': show.id,
                              'show_date': show.created_date,
                              'show_status': show.status.name  
                             }]})

@app.route('/list-shows')
def list_shows():
    """
    return all the shows
    """ 
    shows = ShowRun.query.all()
    ret = []
    for show in shows:
        ret.append({'show_id': show.id,
                    'show_date': show.created_date,
                    'show_status': show.status.name})
    return jsonify({'date': ret})

@app.route('/update-show', methods=['POST'])
def update_show():
    """
    Update show status. 
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        show_id = data['show_id']
        show_status = data['show_status']
        show = ShowRun.query.get(show_id)
        show.status=show_status
        db.session.add(show)
        db.session.commit()
        return jsonify({'record_updates': show_id})
@app.route("/reset")
def reset():
    """
    Resets the state and API to null
    """
    s = State(sentiment=0, focus=0, energy=0, text="reset_triggered")
    db.session.add(s)
    db.session.commit()
    return "Reset the state to 0"

@app.route("/interact", methods=['GET','POST'])
def interact():
    """
    Interact with the API. 

    When post, either submits Surface Data (as JSON) or text content from Audience. 
    Post then updates state db. 

    Get requests returns AI state, possible text and next question all as JSON
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        senti_model = joblib.load(open('./saved/m_senti.p', 'rb'))
        focus_model = joblib.load(open('./saved/m_focus.p','rb'))
        energy_model = joblib.load(open('./saved/m_energy.p','rb'))
        string = data['string']
        print(data)
        # print(string)
        show_id = data['show_id']
        print(show_id)
        def get_pred(model, string):
            return model.predict([string])[0]
        s = State(sentiment=get_pred(senti_model, string),
                  focus = get_pred(focus_model, string),
                  energy = get_pred(energy_model, string),
                  text = string,
                  showrun = show_id)
        db.session.add(s)
        db.session.commit()
        # print('saved ', s)
        return jsonify({'saved': data})
    elif request.method == 'GET':
        ## Get most recent state info
        showrun = request.args.get('show_id')
        s = State.query.filter_by(showrun = int(showrun)).order_by(State.created_date.desc()).first()
        data={}
        data['sentiment'] = s.sentiment
        data['focus'] = s.focus
        data['energy'] = s.energy
        # parse the text into a catagory
        text = s.text
        le = joblib.load(open('./saved/classes.p','rb'))
        cat_model = joblib.load(open('./saved/cat_model.p','rb'))
        probs = pd.concat([pd.Series(le), pd.Series(cat_model.predict_proba([text])[0])], axis=1)
        list_probs = list(probs.sort_values(by=[1], ascending=False)[0][:3]) 
        cat = list_probs[0]
        data['state'] = list_probs[0]
        data['state2'] = list_probs[1]
        data['state3'] = list_probs[2]
        data['text'] = text
        # start making new text and questions
        #if os.path.exists('./saved/faken-markov/' + cat + '.p'):
        #    f_mark = joblib.load(open('./saved/faken-markov/' + cat + '.p', 'rb'))
        #    data['sentence'] = f_mark.make_sentence()
        #else:
        #    f_mark = joblib.load(open('./saved/faken-markov/connected.p', 'rb'))
        #    data['sentence'] = f_mark.make_sentence()

        # quetion time

        if os.path.exists('./saved/faken-questions/' + cat + '.p'):
            f_mark = joblib.load(open('./saved/faken-questions/' + cat + '.p', 'rb'))
            data['questions'] = {i: f_mark.make_sentence() for i in range(4)}
        else:
            f_mark = joblib.load(open('./saved/faken-questions/guarded.p', 'rb'))
            data['questions'] = {i: f_mark.make_sentence() for i in range(4)}
        
        return jsonify(data)

@app.route("/interact-surface", methods=['POST'])
def interact_surface():
    data = request.get_json(force=True)
    s = State(sentiment=data['sentiment'],
              focus = data['focus'],
              energy = data['energy'],
              text = "surface text")
    db.session.add(s)
    db.session.commit()
    return "surface data saved"

@app.route("/talk", methods=["GET"])
def talk():
    showrun = request.args.get('show_id')
    s = State.query.filter_by(showrun = int(showrun)).order_by(State.created_date.desc()).first()
    data={}
    data['sentiment'] = s.sentiment
    data['focus'] = s.focus
    data['energy'] = s.energy
    # parse the text into a catagory
    text = s.text
    le = joblib.load(open('./saved/classes.p','rb'))
    cat_model = joblib.load(open('./saved/cat_model.p','rb'))
    probs = pd.concat([pd.Series(le), pd.Series(cat_model.predict_proba([text])[0])], axis=1)
    list_probs = list(probs.sort_values(by=[1], ascending=False)[0][:3]) 
    cat = list_probs[0]
    data['state'] = list_probs[0]
    data['state2'] = list_probs[1]
    data['state3'] = list_probs[2]
    data['statement'] = None
    sentences = Sentence.query.filter_by(cat = cat).limit(100).all()
    texts = [np.random.choice(sentences).text for s in range(8)]
    data['statement'] = texts
    data['statement_real'] = None
    sentences_shelly = Sentence_Shelly.query.filter_by(cat = cat).limit(100).all()
    texts_org = [np.random.choice(sentences).text for s in range(8)]
    data['statement_real'] = texts_org
    data['reddit'] = ["some","fake", "reddit"]
    return jsonify(data)

@app.route("/form-data", methods=['GET','POST'])
def form_data():
    """
    Form templates
    """
    if request.method == 'POST':
        data = dict(request.form)
        d = FormData(data=data)
        db.session.add(d)
        db.session.commit()
        ## TODO actually saved
        return "data saved"
    else:
        return render_template('pre-show_web_form.html')

@app.route("/form-data/all", methods=['GET'])
def color_form_data():
    query = FormData.query.order_by(FormData.created_date.desc()).limit(10)
    data = [fd.data for fd in query]
    return jsonify(data)

@app.route('/summary', methods=['GET'])
def summary():
    if 'show_id' in request.args:
        showrun = request.args.get('show_id')
        states = State.query.filter_by(showrun = int(showrun)).order_by(State.created_date.desc()).all()
        texts = [s.text for s in states]
    else: 
        texts = []
        show_ids = request.args.get('show_ids')
        show_ids = [int(x) for x in show_ids.split(',')]
        for show_id in show_ids:
            states = State.query.filter_by(showrun = show_id).order_by(State.created_date.desc()).all()
            t = [s.text for s in states]
            texts.extend(t)
    vectorizer = TfidfVectorizer(stop_words='english', min_df=1, tokenizer=tokenize_nltk)
    dtm = vectorizer.fit_transform(texts).toarray()
    vocab = np.array(vectorizer.get_feature_names())    
    #Define Topic Model: LatentDirichletAllocation (LDA)
    clf = decomposition.LatentDirichletAllocation(n_topics=5, random_state=3)
    num_top_words = 3
    doctopic = clf.fit_transform(dtm)
    topic_words = []
    for topic in clf.components_:
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words.append([vocab[i] for i in word_idx])
    merged = list(set(itertools.chain.from_iterable(topic_words))) # use set for unique items
    return jsonify({'data': {'topics': merged}})



@app.route("/submitted")
def thanks():
    """
    Thank you for completing form
    """
    return render_template('submitted.html')


if __name__ == '__main__':
    env = os.environ.get('ENV', 'dev')
    if env == 'prod':
        app.run(host='0.0.0.0')
    else:
        app.run(debug=True)



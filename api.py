import flask
import sqlite3
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime 
import os
import pickle
from sentiment.sentiment import stemming_tokenizer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/test.db')
db = SQLAlchemy(app)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sentiment = db.Column(db.Float)
    focus = db.Column(db.Float)
    energy = db.Column(db.Float)
    text = db.Column(db.String(5000))

@app.route('/')
def test():
    """
    fake home                 
    """
    return "Test works"

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
            ## TODO: store_content
            ## TODO: change sentiment/state db
            new_data(get)
            pass
    elif request.method == 'GET':
        ## Get most recent state info 
        s = State.query.order_by(State.created_date.desc()).first()
        data={}
        data['sentiment'] = s.sentiment
        data['focus'] = s.focus
        data['energy'] = s.energy
        # parse the text into a catagory
        text = s.text
        le = pickle.load(open('./saved/classes.p','rb'))
        cat_model = pickle.load(open('./saved/cat_model.p','rb'))
        cat = le[cat_model.predict([text])][0]
        # start making new text and questions
        if os.path.exists('./saved/faken-markov/' + cat + '.p'):
            f_mark = pickle.load(open('./saved/faken-markov/' + cat + '.p', 'rb'))
            data['sentence'] = f_mark.make_sentence()
        else:
            f_mark = pickle.load(open('./saved/faken-markov/connected.p', 'rb'))
            data['sentence'] = f_mark.make_sentence()

        # quetion time

        if os.path.exists('./saved/faken-questions/' + cat + '.p'):
            f_mark = pickle.load(open('./saved/faken-questions/' + cat + '.p', 'rb'))
            data['question'] = f_mark.make_sentence()
        else:
            f_mark = pickle.load(open('./saved/faken-questions/guarded.p', 'rb'))
            data['question'] = f_mark.make_sentence()
        return jsonify(data)

@app.route("/interact-surface", methods=['POST'])
def interact_surface():
    content = request.get_json(silent=True)


@app.route("/form-data", methods=['GET','POST'])
def form_data():
    """
    Takes the form data as an HTTP Post, 
    returns the canned hello for http GET sentence. 
    """
    return "test"

if __name__ == '__main__':
    env = os.environ.get('ENV', 'dev')
    if env == 'prod':
        app.run(host='0.0.0.0')
    else:
        db.create_all()
        app.run(debug=True)



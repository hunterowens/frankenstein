import flask
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime 
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/test.db')
db = SQLAlchemy(app)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sentiment = db.Column(db.Float)
    focus = db.Column(db.Float)
    energy = db.Column(db.Float)

class Text(db.Model):
    """
    class to store text in. 
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(5000))

@app.route("/reset")
def reset():
    """
    Resets the state and API to null
    """
    s = State(sentiment=0, focus=0, energy=0)
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
        if surface == True:
            ## TODO implement surface reciever
            pass
        else:
            ## TODO: store_content
            ## TODO: change sentiment/state db
            new_data(get)
            pass
    elif request.method == 'GET':
        ## TODO generate questions
        ## get the chat content
        ## TODO setup json object
        return the_json_object

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



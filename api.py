import flask
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)

@app.route("/reset")
def reset():
    """
    Resets the state and API to null
    """
    ## TODO: Implement state DB 
    ## TODO:set to 0
    return 

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
        ## TODO setup json object
        return the_json_object

@app.route("/form-data", method=['GET','POST'])
def form_data():
    """
    Takes the form data as an HTTP Post, 
    returns the canned hello for http GET sentence. 
    """
    return "test"

if __name__ == '__main__':
    app.run(debug=True)



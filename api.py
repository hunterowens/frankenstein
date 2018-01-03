import flask
import sqlite3
app = flask.Flask(__name__)

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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

if __name__ == '__main__':
    app.run(debug=True)



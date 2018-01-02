import json
import pythonosc
import chatbot
import argparse
import math
import asyncio
import datetime
from pythonosc import dispatcher, osc_server, udp_client

current_sentiment = None 
current_focus = None 
current_energy = None

async def sent_state_to_ai(current_focus, current_energy, current_sentiment):
    """
    sents the state as JSON to the AI 
    """
    ## TODO: Implement read 
    ## TODO: Implement sent to AI 
    pass

def get_sentiment_from_ai():
    ## TODO implement get methods
    ## TODO turn sentiments into state
    """
    Gets state from AI, transforms into sentiment
    """
    return {"state": "curious", "action": "talking"} 

def setup():
    """
    sets AI in waiting state
    """
    current_sentiment = 0
    current_focus = 0
    current_energy = 0
    sent_state_to_ai(current_focus, current_energy, current_sentiment)
    print("AI Init State Waiting")
    return None

async def osc_dispatch(addr, msg, ip='127.0.0.1', port=5050):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    client = udp_client.SimpleUDPClient(ip, port)
    print(client.send_message(addr, msg))
    return None

async def broadcast_state():  
    """
    Broadcasts state
    """
    state = get_state_from_ai()
    for k,v in state:
        print("Distpaching {0} with value {1}", k,v)
        osc_dispatch(k,v)
    return

async def broadcast_questions():
    """
    broadcast the questions
    """
    questions = {"text1": "Why is this night different from all other nights?",
                 "text2": "Why do we eat Matzah?",
                 "text3": "Why do we recline?",
                 "text4": "What about those damn bitter herbs",
                 "text0": "statements statements statements"}
    for k,v in questions:
        print("Sending questions to editor")
        osc_dispatch(k,v)
    return

def surface_handler(unused_addr, args, string):
    """
    Handles the surface messages, alts sentiment

    Surface argument to be OSC String Formatted as followed
    "sentiment: value; focus: value; energy: value"
    """
    try: 
        vals = json.load(string)
    except ValueError:
        print("Unable to decode JSON from Surface")
        exit()
    current_sentiment = vals['sentiment']
    current_focus = vals['focus']
    current_energy = vals['energy']
    send_to_ai(current_focus, current_energy, current_sentiment)
    print("Surface updated AI State at: ", datetime.datetime.now().time())
    
def reset_handler(unused_addr, args, boolean):
    """

    Handles the reset from Editor

    """
    ## TODO: Implement
    print("reset handler")
    
    return

def talking_handler(unused_addr, args, boolean):
    """
    Starts talking
    """
    print("talking handler")
    ## TODO 

    return

def silent_handler(unused_addr, args, boolean):
    """
    silences the system after TTS
    """
    print("silience handles")
    ## TODO 

    return

async def osc_server(ip='127.0.0.1', port=5050):
    """
    sets up and runs the OSC server. 
    """
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/surface-sentiments", surface_handler, string)
    dispatcher.map("/reset", reset_handler, boolean)
    dispatcher.map("/silent", silent_handler, boolean)

    server = pythonosc.osc_server.ThreadingOSCUDPServer(
         (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
          help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
          help="The port the OSC server is listening on")
    parser.add_argument('--server', action='store_true', default=True,
                        help="Run in server mode")
    parser.add_argument('--state', action='store_true',default=True,
                        help="Broadcast the state")
    parser.add_argument('--text', action='store_true', default=False,
                        help="broadcast the text questions")
    args = parser.parse_args()
    
    if args.server:
        osc_server()
    if args.state:
        broadcast_state()
    if args.text:
        broadcast_questions()

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
    
def osc_server(ip='127.0.0.1', port=5050):
    """
    sets up and runs the OSC server. 
    """
    dispatch = dispatcher.Dispatcher()
    dispatcher.map("/surface-sentiments", surface_handler, string)
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
    parser.add_argument("--act", type=int, default=1,
          help="which act the performacne is on")
    args = parser.parse_args()
    osc_server()

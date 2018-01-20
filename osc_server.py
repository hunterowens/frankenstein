"""
Code to run the OSC server that listens for various 
inputs. 

Usage: python osc_server.py
"""


import json
import pythonosc
import argparse
import math
import datetime
from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder
import requests
from collections import OrderedDict
from statistics import mean
import logging

logger = logging.getLogger('osc_server')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('osc_server.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

from util import ip_osc, ip_osc_server, ip_osc_editor, port_server,port_client, port_client_editor, osc_dispatch, api_url   
current_state = OrderedDict()
current_state["/state"] = "calm"
current_state["/action"] = "start"
current_state["/sentiment"] = 0.0
current_state["/energy"] = 0.0
current_state["/focus"] = 0.0


def change_state(current_state, new_state):
    """
    Change the current state dict to 
    reflect state param: new_state
    return current_state
    """
    current_state['/state'] = new_state
    logger.info("New State Set to {0}".format(current_state))
    return current_state

def send_surface_state_to_ai(sentiment, energy, focus):
    """
    sents the state / new talking  as JSON to the AI
    focus, energy, and sentiment are floats; unit is a string; words and parts are arrays of strings where the indexes correspond, so words[0] goes with parts[0]
    """
    
    logger.info("AI State is: {0} focus, {1} energy, and {2} sentiment".format(current_focus, current_energy, current_sentiment))
    data = {
            'focus': focus,
            'sentiment': sentiment,
            'energy': energy
            } 
    r = requests.post(api_url + 'interact-surface', data = data)
    return r


def send_answer_to_ai(answer):
    """
    Sents an answer to the AI 
    """
    logger.info("Answer sending ", answer)

    headers = {
        "content-type": "application/json"
    }

    r = requests.post(api_url + 'interact', 
                      json={'string': answer},
                      headers=headers)
    return r

def get_api_interact_data():
    """
    Gets state from AI, transforms into sentiment.

    Returns a string of JSON
    """
    logger.info("Getting Data from AI")
    r = requests.get(api_url + 'interact')
    if r.status_code == 200:
        data = r.json()
    else: 
        data = pickle.load(open('./default-api-response.p','rb'))
        logger.info("Using Default Data: {}".format(data))
        
    if data['state'] != current_state['/state']:
        current_state['/state'] = data['state']
    else:
        current_state['/state'] = data['state2']
    current_state['/sentiment'] = data['sentiment']
    current_state['/focus'] = data['focus']
    current_state['/energy'] = data['energy']
    logger.info('state updated from API with {0}'.format(data))
    return data
    

def setup():
    """
    sets AI in waiting state
    """
    r = requests.get(api_url + "reset")
    logger.info("AI Init State Waiting")
    current_state = get_api_interact_data()
    ##pull text from AI 
    return None



def broadcast_state(state=current_state, ip=ip_osc, port=port_client, num_tries=3):  
    """
    Broadcasts state
    """
    logger.info("Called Broadcast State Function")
    client = udp_client.UDPClient(ip, port,1)
    builder = osc_message_builder.OscMessageBuilder(address='/status')
    for k,v in state.items():
        builder.add_arg(v)

    for _ in range(num_tries):
        client.send(builder.build()) 
        logger.info("sent {0} to {1}:{2}. Attempt {3}".format(builder.args, ip, port, _))
    return None

def broadcast_text(AItext):
    """
    send a fixed piece of text from the AI
    add delay into this OSC as second args
    get text somehow 
    """
    
    osc_dispatch('/textnoquest', AItext, port=port_client_editor)
    logger.info("Updating State")
    broadcast_state(num_tries=3)
    return None

def send_questions_to_line_editor(num_tries=3):
    """
    Sends data for display to Line Editor
    """
    data = get_api_interact_data()['questions']
    logger.info("Called send question to the line editor")
    ip=ip_osc
    port=port_client_editor
    client = udp_client.UDPClient(ip, port,1)
    logger.info("Prepping to send Data to Line Editor {}:{}", ip, port)
    builder = osc_message_builder.OscMessageBuilder(address='/textques')
    for k,v in data.items():
        logger.info(k,v)
        builder.add_arg(v)
    for _ in range(num_tries):
        client.send(builder.build()) 
        logger.info("sent {0} to {1}:{2}. Attempt {3}".format(builder.args, ip, port, _))
    broadcast_state()
    return None

surface_data = []

def surface_handler(unused_addr, args):
    """
    Handles the surface messages, alts sentiment
    Surface argument to be OSC String Formatted as followed
    "sentiment: value; focus: value; energy: value"
    """
    logger.info("Got Surface Message")
    try: 
        vals = json.loads(args)
        ## surfaces need to be directed to pi, look in js/machineConfiguration.json
    except ValueError:
        logger.info("Unable to decode JSON from Surface")
        exit()
    current_sentiment = vals['sentiment']
    current_focus = vals['focus']
    current_energy = vals['energy']
    current_unit = vals['unit']
    logger.info("From Surface Unit {0}".format(current_unit))
    current_words = vals['words']
    current_parts = vals['parts']
    surface_data.append(vals)
    return None
 
def reset_handler(unused_addr, args):
    """
    Handles the reset from Editor
    """
    logger.info('reset handler')
    current_state.update({'/action': 'start'})
    broadcast_state()
    return None

def answer_handler(unused_addr, args):
    """
    Starts answering
    """
    logger.info("answer handler")
    send_answer_to_ai(args)
    current_state.update({'/action': 'thinking'})
    broadcast_state(num_tries=3)

    send_questions_to_line_editor()
    return None

def refresh_handler(unused_addr, args):
    """
    Refresh text
    """
    logger.info("Refreshing text")
    send_questions_to_line_editor()
    return None


def talking_handler(unused_addr, args):
    """
    Starts talking
    """
    logger.info("talking handler")
            
    current_state.update({'/action': 'talking'})
    broadcast_state()
    
    return None

def question_handler(unused_addr, args):
    """
    shuts the machine up
    """
    logger.info('question handler')
    current_state.update({'/action': 'question'})
    broadcast_state()
    
    return None

def thinking_handler(unsused_addr, args):
    """
    shuts the machine up
    """
    logger.info('thinking handler')
    current_state.update({'/action': 'thinking'})
    broadcast_state()
    
    return None   

def silent_handler(unused_addr, args):
    """
    silences the system after TTS
    """
    logger.info("silence handles")
    current_state.update({'/action': 'expectant'})
    broadcast_state()

    return None

def surfacestart_handler(unused_addr, args):
    """
    blasts start to the surfaces
    """
    logger.info("Blasting Start to the Surfaces")
    osc_dispatch('/start-surface', 1, ip='192.168.1.255', num_tries=3)

def surfacereset_handler(unused_addr, args):
    """
    blasts reset to surface
    """

    logger.info("Blasting Reset to the Surface")
    osc_dispatch('/reset-surface', 1, ip='192.168.1.255', num_tries=3)

def surfacestop_handler(unused_addr, args):
    """
    blasts stop to surface
    """

    logger.info("Blasting Stop to the Surface")
    if len(surface_data) != 0:
        sentiment = mean([d['sentiment'] for d in surface_data])
        energy = mean([d['energy'] for d in surface_data])
        focus = mean([d['focus'] for d in surface_data])
        send_surface_state_to_ai(sentiment, energy, focus) 
    osc_dispatch('/stop-surface', 1, ip='192.168.1.255', num_tries=3)

def end_handler(unused_addr, args):
    """
    ends the show
    """
    logger.info("end of show")
    current_state.update({'/action': 'end'})
    broadcast_state()

    return

def new_state_handler(unused_addr, args):
    logger.info('New State {} recieved'.format(args))
    current_state['/state'] = args
    logger.info("Updated current_state to {}".format(current_state))
    return 


def osc_server(ip=ip_osc_server, port=port_server):
    """
    sets up and runs the OSC server. 
    """
    dispatch = dispatcher.Dispatcher()
    
    """
    dispatch.map("/surface-sentiments", surface_handler)
    dispatch.map("/reset", reset_handler)
    dispatch.map("/silent", silent_handler)
    """
    
    dispatch.map("/surface-sentiments", surface_handler)
    dispatch.map("/reset", reset_handler)
    dispatch.map("/silent", silent_handler)
    dispatch.map("/answer", answer_handler)
    dispatch.map("/refresh", refresh_handler)
    dispatch.map("/talking", talking_handler)
    dispatch.map("/end", end_handler)
    dispatch.map("/question", question_handler)
    dispatch.map("/thinking", thinking_handler)
    dispatch.map("/startsurface", surfacestart_handler)
    dispatch.map("/closesurface", surfacestop_handler)
    dispatch.map("/resetsurface", surfacereset_handler)
    dispatch.map("/newstate", new_state_handler)

    server = pythonosc.osc_server.ThreadingOSCUDPServer(
         (ip, port), dispatch)
    logger.info("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == '__main__':
    osc_server()

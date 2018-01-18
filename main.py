import json
import pythonosc
## import chatbot
import argparse
import math
import asyncio
import datetime
from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder
import requests


## added variables to change the ip and port easily

ip_osc = '192.168.1.255'
##ip_osc = '192.168.0.255'
ip_osc_server='0.0.0.0'
## ip_osc = '10.253.0.255'
port_server = 7007
port_client = 7007
port_client_editor = 7008

## this is the dictionary for the OSC meeting/ osc_dispatch
currentState = {"/state":"happy", "/action":"talking", "/sentiment": -0.5, "/energy": 0.25, "/focus": -0.5 }
##currentState = {"/state":"tolerant", "/action":"talking", "/sentiment": -0.5, "/energy": 0.25, "/focus": -0.5 }
##currentState = {"/state":"guarded", "/action":"talking", "/sentiment": -0.5, "/energy": 0.25, "/focus": -0.5 }

def send_state_to_ai(current_focus, current_energy, current_sentiment, current_unit, current_words, current_parts):
    """
    sents the state / new talking  as JSON to the AI
    focus, energy, and sentiment are floats; unit is a string; words and parts are arrays of strings where the indexes correspond, so words[0] goes with parts[0]
    """
    
    print("AI State is: {0} focus, {1} energy, and {2} sentiment".format(current_focus, current_energy, current_sentiment))
    
    ## TODO: Implement read 
    ## TODO: Implement sent to AI 
    pass

def get_sentiment_from_ai():
    ## TODO implement get methods
    ## TODO turn sentiments into state
    """
    Gets state from AI, transforms into sentiment
    """
    print("Getting State from AI")
    return {currentState} 


def setup():
    """
    sets AI in waiting state
    """
    requests.get("./reset")
    print("AI Init State Waiting")
    currentState = get_sentiment_from_ai()
    return None
"""
class SimpleOSCClientRedux(udp_client.UDPClient):

    def send_message(self, address, value):
        builder = osc_message_builder.OscMessageBuilder(address=address)
        if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            values = [value]
        else:
            values = value
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.send(msg)
"""

def osc_dispatch(addr, msg, ip=ip_osc, port=port_client):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    client = udp_client.UDPClient(ip, port,1)
    ## SimpleOSCClientRedux(client)
    ## client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Sent {0} with {1}".format(addr, msg))
    
    builder = osc_message_builder.OscMessageBuilder(address=addr)
    builder.add_arg(msg)
    client.send(builder.build())
    
    ## print(client(addr, msg))
    return None

def check_state():
    """
    gets state from AI
    """
    
    state=get_sentiment_from_ai()
    return 

def broadcast_state(state=currentState):  
    """
    Broadcasts state
    """
    print("Called Broadcast State Function")
    ## TODO: Run in infinite loop version 
    for k,v in state.items():
        print("Dispatching {0} with value {1}".format(k,v))
        osc_dispatch(k,v)
    return

def broadcast_text(AItext):
    """
    send a fixed piece of text from the AI
    """
    
    osc_dispatch('/textnoquest', AItext, port=port_client_editor)
    print("Updating State")
    broadcast_state()
    return

def broadcast_questions():
    """
    broadcast the questions ## verified with web app
    """
    questions = '{"text0": "How are you?", "text1": "Are you well?", "text2": "Who knows?", "text3": "Why not?"}'
    print("Sending questions to editor")
    osc_dispatch('/textques', questions, port=port_client_editor)
    print("Updating State")
    broadcast_state()
    return

def surface_handler(unused_addr, args):
    """
    Handles the surface messages, alts sentiment
    Surface argument to be OSC String Formatted as followed
    "sentiment: value; focus: value; energy: value"
    """
    print("Got Surface Message")
    try: 
        vals = json.loads(args)
        ## surfaces need to be directed to pi, look in js/machineConfiguration.json
    except ValueError:
        print("Unable to decode JSON from Surface")
        exit()
    current_sentiment = vals['sentiment']
    current_focus = vals['focus']
    current_energy = vals['energy']
    current_unit = vals['unit']
    print("From Surface Unit {0}".format(current_unit))
    current_words = vals['words']
    current_parts = vals['parts']
    send_state_to_ai(current_focus, current_energy, current_sentiment, current_unit, current_words, current_parts)
    print("Surface updated AI State at: ", datetime.datetime.now().time())
 
def reset_handler(unused_addr, args):
    """
    Handles the reset from Editor
    """
    ## TODO: Implement
    print("reset handler")
    currentState.update({'/action': 'start'})
    broadcast_state()
    currentState.update({'/action': 'expectant'})

    return

def answer_handler(unused_addr, args):
    """
    Starts answering
    """
    print("send answer to ai")
    
    currentState.update({'/action': 'thinking'})
    broadcast_state()

    ## TODO 

    return

def refresh_handler(unused_addr, args):
    """
    Refresh text
    """
    print("Refreshing text")
    broadcast_questions() 
    ## TODO 

    return

def thinking_handler(unused_addr, args):
    """
    Starts thinking
    """
    print("thinking handler")
            
    currentState.update({'/action': 'thinking'})
    broadcast_state()

    ## TODO 

    return

def talking_handler(unused_addr, args):
    """
    Starts talking
    """
    print("talking handler")
            
    currentState.update({'/action': 'talking'})
    broadcast_state()

    ## TODO 

    return

def silent_handler(unused_addr, args):
    """
    silences the system after TTS
    """
    print("silence handles")
    currentState.update({'/action': 'expectant'})
    broadcast_state()
    ## TODO 

    return

def question_handler(unused_addr, args):
    """
    sends the final questions
    """

    print("Question Handler")
    currentState.update({'/action': 'question'})
    broadcast_state()

def end_handler(unused_addr, args):
    """
    ends the show
    """
    print("end of show")
    currentState.update({'/action': 'end'})
    broadcast_state()
    ## TODO 

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
    dispatch.map("/thinking", thinking_handler)
    dispatch.map("/question", question_handler)
    
    ## TODO: Talk State - > triger from AI to get new words/questions etc from teh AI on the server and then broadcast 
    
    server = pythonosc.osc_server.ThreadingOSCUDPServer(
         (ip, port), dispatch)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip_osc,
          help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port_server,
          help="The port the OSC server is listening on")
    parser.add_argument('--server', action='store_true', default=False,
                        help="Run in server mode")
    parser.add_argument('--state', action='store_true',default=False,
                        help="Broadcast the state")
    parser.add_argument('--text', action='store_true', default=False,
                        help="broadcast the text questions")
    parser.add_argument('--silent', action='store_true', default=False, help="end talking cue")
    parser.add_argument('--talking', action='store_true', default=False, help="get talking cue")
    parser.add_argument('--answer', action='store_true', default=False, help="get answer")
    parser.add_argument('--thinking', action='store_true', default=False, help="sample thinking")
    parser.add_argument('--question', action='store_true', default=False, help="send last statement")
    parser.add_argument('--reset', action='store_true', default=False, help="start over")
    parser.add_argument('--refresh', action='store_true', default=False, help="refresh questions")
    parser.add_argument('--end', action='store_true', default=False, help="end experience")
    parser.add_argument('--surface', action='store_true', default=False, help="send dummy surface data")
    parser.add_argument('--startsurface', action='store_true', default=False, help="test surface start")
    parser.add_argument('--resetsurface', action='store_true', default=False, help="test surface reset")
    args = parser.parse_args()
    print("Got argument: {}".format(args))
    
    if args.server:
        print("Sending Server")
        osc_server()
    elif args.state:
        print("Sending state")
        ##check_state()
        broadcast_state()
    elif args.text:
        print("Sending Text")
        broadcast_questions()
    elif args.silent:
        print("Sending OSC Test Message")
        osc_dispatch('/silent', 1)
    elif args.talking:
        print("Sending Talking")
        osc_dispatch('/talking', "answer")
    elif args.answer:
        print("Sending Answer") ## verified with web app
        osc_dispatch('/answer', "answer")
    elif args.thinking:
        print("Thinking Answer")
        osc_dispatch('/thinking', "thinking")
    elif args.question:
        print("Sending Question")
        osc_dispatch('/question', "question")
    elif args.reset:
        print("Reseting") ## verified with web app
        osc_dispatch('/reset', 1)    
    elif args.refresh:
        print("Refreshing questions")
        osc_dispatch('/refresh', 1)
    elif args.end:
        print("End experience")
        osc_dispatch('/end', 1)
    elif args.startsurface:
        print("Telling surfaces to turn on")
        osc_dispatch('/start-surface', 1)
    elif args.resetsurface:
        print("Telling surfaces to start over")
        osc_dispatch('/reset-surface', 1)
    elif args.surface:
        print("Sending Surface Message")
        ## foo = json.loads('{"number": 1.0, "other": 4.3}')
        osc_dispatch('/surface-sentiments', '{"sentiment": 0.15, "focus": 0.65, "energy": -0.3, "unit": "test", "words": ["inspired", "anxious", "understanding"], "parts": ["hand", "eye", "head"]}')

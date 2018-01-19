import json
import pythonosc
import argparse
import math
import datetime
from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder
import requests
from collections import OrderedDict
from statistics import mean

## added variables to change the ip and port easily
## testing if Git works with  ST

ip_osc = '192.168.1.255'
##ip_osc = '192.168.0.255'
ip_osc_server='0.0.0.0'
ip_osc_editor='196.168.1.255'
## ip_osc = '10.253.0.255'
port_server = 7007
port_client = 7007
port_client_editor = 7007
api_url = "http://frankenstein.hunterowens.net/"
## Some comments

    
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
    print("New State Set to {0}".format(current_state))
    return current_state

def send_surface_state_to_ai(sentiment, energy, focus):
    """
    sents the state / new talking  as JSON to the AI
    focus, energy, and sentiment are floats; unit is a string; words and parts are arrays of strings where the indexes correspond, so words[0] goes with parts[0]
    """
    
    print("AI State is: {0} focus, {1} energy, and {2} sentiment".format(current_focus, current_energy, current_sentiment))
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
    print("Answer sending ", answer)

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
    print("Getting Data from AI")
    r = requests.get(api_url + 'interact')
    if r.status_code == 200:
        data = r.json()
    else: 
        data = pickle.load(open('./default-api-response.p','rb'))
        print("Using Default Data: {}".format(data))
        
    current_state['/state'] = data['state']
    current_state['/sentiment'] = data['sentiment']
    current_state['/focus'] = data['focus']
    current_state['/energy'] = data['energy']
    print('state updated')
    return data
    

def setup():
    """
    sets AI in waiting state
    """
    r = requests.get(api_url + "reset")
    print("AI Init State Waiting")
    current_state = get_api_interact_data()
    ##pull text from AI 
    return None


def osc_dispatch(addr, msg, ip=ip_osc, port=port_client):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    client = udp_client.UDPClient(ip, port,1)
    ## SimpleOSCClientRedux(client)
    ## client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Sent {0} with {1} to {2} at {3}".format(addr, msg, ip, port))
    
    builder = osc_message_builder.OscMessageBuilder(address=addr)
    builder.add_arg(msg)
    client.send(builder.build())
    
    ## print(client(addr, msg))
    return None

def broadcast_state(state=current_state, ip=ip_osc, port=port_client):  
    """
    Broadcasts state
    """
    print("Called Broadcast State Function")
    client = udp_client.UDPClient(ip, port,1)
    builder = osc_message_builder.OscMessageBuilder(address='/status')
    for k,v in state.items():
        builder.add_arg(v)

    client.send(builder.build()) 
    print("sent {0} to {1}:{2}".format(builder.args, ip, port))
    return None

def broadcast_text(AItext):
    """
    send a fixed piece of text from the AI
    add delay into this OSC as second args
    get text somehow 
    """
    
    osc_dispatch('/textnoquest', AItext, port=port_client_editor)
    print("Updating State")
    broadcast_state()
    return None

def send_questions_to_line_editor():
    """
    Sends data for display to Line Editor
    """
    data = get_api_interact_data()['questions']
    print("Called send question to the line editor")
    #client = udp_client.UDPClient(ip_osc_editor, port_client_editor,1)
    #builder = osc_message_builder.OscMessageBuilder(address='/textques')
    #for k,v in data.items():
    #    builder.add_arg(v)
    #builder.add_arg(.75)
    #print('builder ', builder.address)
    #client.send(builder.build()) 
    #osc_dispatch('/textquest', .75, ip=ip_osc_server, port=port_client_editor)
    # print("sent {0} to {1}:{2}".format(builder.args, ip_osc_editor, port_client_editor))
    ip=ip_osc
    port=port_client_editor
    client = udp_client.UDPClient(ip, port,1)
    print("Send Data to Line Editor {}:{}", ip, port)
    builder = osc_message_builder.OscMessageBuilder(address='/textques')
    for k,v in data.items():
        print(k,v)
        builder.add_arg(v)
    client.send(builder.build()) 
    print("sent {0} to {1}:{2}".format(builder.args, ip, port))
    broadcast_state()
    return None

surface_data = []

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
    surface_data.append(vals)
    return None
 
def reset_handler(unused_addr, args):
    """
    Handles the reset from Editor
    """
    ## TODO: Implement
    print("reset handler")
    setup()
    surface_data = []
    current_state.update({'/action': 'start'})
    broadcast_state()
    current_state.update({'/action': 'expectant'})

    return None

def answer_handler(unused_addr, args):
    """
    Starts answering
    """
    print("send answer to ai")
    send_answer_to_ai(args)
    current_state.update({'/action': 'thinking'})
    broadcast_state()

    ## Call line editor
    send_questions_to_line_editor()
    return None

def refresh_handler(unused_addr, args):
    """
    Refresh text
    """
    print("Refreshing text")
    send_questions_to_line_editor()

    return None


def talking_handler(unused_addr, args):
    """
    Starts talking
    """
    print("talking handler")
            
    current_state.update({'/action': 'talking'})
    broadcast_state()

    send_questions_to_line_editor() 
    
    return None

def question_handler(unused_addr, args):
    """
    shuts the machine up
    """
    print('question handler')
    current_state.update({'/action': 'question'})
    broadcast_state()
    
    return None

def thinking_handler(unsused_addr, args):
    """
    shuts the machine up
    """
    print('thinking handler')
    current_state.update({'/action': 'thinking'})
    broadcast_state()
    
    return None   

def silent_handler(unused_addr, args):
    """
    silences the system after TTS
    """
    print("silence handles")
    current_state.update({'/action': 'expectant'})
    broadcast_state()

    return None

def surfacestart_handler(unused_addr, args):
    """
    blasts start to the surfaces
    """
    print("Blasting Start to the Surfaces")
    osc_dispatch('/start-surface', 1)

def surfacereset_handler(unused_addr, args):
    """
    blasts reset to surface
    """

    print("Blasting Reset to the Surface")
    osc_dispatch('/reset-surface', 1)

def surfacestop_handler(unused_addr, args):
    """
    blasts stop to surface
    """

    print("Blasting Stop to the Surface")
    sentiment = mean([d['sentiment'] for d in surface_data])
    energy = mean([d['energy'] for d in surface_data])
    focus = mean([d['focus'] for d in surface_data])
    send_surface_state_to_ai(sentiment, energy, focus) 
    osc_dispatch('/close-surface', 1)

def end_handler(unused_addr, args):
    """
    ends the show
    """
    print("end of show")
    current_state.update({'/action': 'end'})
    broadcast_state()

    return

print("some stupid stuff")

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
    parser.add_argument('--text', action='store_true', default=False,
                        help="broadcast the text questions")
    parser.add_argument('--silent', action='store_true', default=False, help="end talking cue")
    parser.add_argument('--talking', action='store_true', default=False, help="get talking cue")
    parser.add_argument('--answer', action='store_true', default=False, help="get answer")
    parser.add_argument('--reset', action='store_true', default=False, help="start over")
    parser.add_argument('--refresh', action='store_true', default=False, help="refresh questions")
    parser.add_argument('--end', action='store_true', default=False, help="end experience")
    parser.add_argument('--question', action='store_true', default=False, help='test question handler')
    parser.add_argument('--thinking', action='store_true', default=False, help='test thinking handler')
    parser.add_argument('--surface', action='store_true', default=False, help="send dummy surface data")
    parser.add_argument( "--set-state", dest="new-state", default='guarded',
                        help="set teh new state", metavar="STATE")
    parser.add_argument('--startsurface', action='store_true', default=False, help="test surface start")
    parser.add_argument('--resetsurface', action='store_true', default=False, help="test surface reset")
    parser.add_argument('--stopsurface', action='store_true', default=False, help="test surface stop")
    args = parser.parse_args()
    print("Got argument: {}".format(args))
    
    if args.server:
        print("Sending Server")
        osc_server()
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
    elif args.reset:
        print("Reseting") ## verified with web app
        osc_dispatch('/reset', 1)    
    elif args.refresh:
        print("Refreshing questions")
        osc_dispatch('/refresh', 1)
    elif args.end:
        print("End experience")
        osc_dispatch('/end', 1)
    elif args.question:
        print("Sending a question")
        osc_dispatch('/question', 1)
    elif args.thinking:
        print("Setting thinking")
        osc_dispatch('/thinking', 1)
    elif args.startsurface:
        print("Telling surfaces to turn on")
        osc_dispatch('/startsurface', 1)
    elif args.resetsurface:
        print("Telling surfaces to start over")
        osc_dispatch('/resetsurface', 1)
    elif args.surface:
        print("Sending Surface Message")
        ## foo = json.loads('{"number": 1.0, "other": 4.3}')
        osc_dispatch('/surface-sentiments', '{"sentiment": 0.15, "focus": 0.65, "energy": -0.3, "unit": "test", "words": ["inspired", "anxious", "understanding"], "parts": ["hand", "eye", "head"]}')
    elif vars(args)['new-state']:
        print('changing state')
        change_state(current_state, vars(args)['new-state'])

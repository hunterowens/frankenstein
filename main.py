import json
import pythonosc
import chatbot
import argparse
from pythonosc import dispatcher, osc_server, udp_client
import math
import threading

def osc_dispatch(addr, msg, ip='127.0.0.1', port=5050):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    client = udp_client.SimpleUDPClient(ip, int(port))
    return client.sent_message(addr, msg)

def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass

def osc_server(ip='127.0.0.1', port=5050):
    """
    sets up and runs the OSC server. 
    """
    dispatch = dispatcher.Dispatcher()
    dispatch.map("/volume", print_volume_handler, "Volume")
    dispatch.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = pythonosc.osc_server.ThreadingOSCUDPServer(
         (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

def act_1():
    pass

def act_2():
    pass

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
    osc_dispatch('/volume', "test")
    if args.act == 1:
        act_1()
    else: 
        act_2()

    

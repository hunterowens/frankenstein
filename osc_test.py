from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder

from osc_server import  broadcast_state 
from util import osc_dispatch
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( "--state", dest="new-state", default='guarded',
                        help="set teh new state", metavar="STATE")
    parser.add_argument( "--action", dest="action", default='expectant',
                        help="set teh new action", metavar="ACTION")
    parser.add_argument('--surface', action='store_true', default=False, help="send dummy surface data")
    parser.add_argument('--startsurface', action='store_true', default=False, help="test surface start")
    parser.add_argument('--resetsurface', action='store_true', default=False, help="test surface reset")
    parser.add_argument('--stopsurface', action='store_true', default=False, help="test surface stop")
    # Parse Args
    args = parser.parse_args()
    print("Arguments: ", args)
    args = parser.parse_args()
    if vars(args)['new-state']:
        state = vars(args)['new-state']
        action = vars(args)['action']
        print('changing state and action to {},{}'.format(state, action))
        osc_dispatch('/newstate',state)
        if action == 'talking':
            osc_dispatch('/talking', 1, ip="0.0.0.0", num_tries=4)
        elif action == 'thinking':
            osc_dispatch('/thinking', 1)
        elif action == 'expectant':
            osc_dispatch("/silent", 1)
        elif action == 'start':
            osc_dispatch("/reset", 1)
        elif action == 'stop':
            osc_dispatch("/end", 1)
        else:
            print("No Action Recognized")
    elif args.startsurface:
        print("Telling surfaces to turn on")
        osc_dispatch('/start-surface', 1)
    elif args.closesurface:
        print("Telling surfaces to close")
        osc_dispatch('/close-surface', 1)
    elif args.resetsurface:
        print("Telling surfaces to start over")
        osc_dispatch('/reset-surface', 1)
    elif args.surface:
        print("Sending Surface Message")
        ## foo = json.loads('{"number": 1.0, "other": 4.3}')
        osc_dispatch('/surface-sentiments', '{"sentiment": 0.15, "focus": 0.65, "energy": -0.3, "unit": "test", "words": ["inspired", "anxious", "understanding"], "parts": ["hand", "eye", "head"]}')


import json
import pythonosc
import chatbot

def setup():
    """
    Create the initial state for the performance"
    """
    init_state = "neutral"
    current_act = 1 
    ## TODO: Setup Python OSC

def osc_dispatch(msg):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    ## TODO: Pass Init 
    ## TODO: Send msg
    pass

if __name__ == '__main__':
    setup()
    if current_act == 1: 
        pass
    elif current_act == 2: 
        ## Act 2
        chatbot.chat()
        surface.listen()
        change_sentiment()
        osc_dispatch(sentiment)
        ## TODO: Determine when to change to act_# 
    elif current_act == 3:
        ## Act 3
        osc_dispatch()
        ## TODO: Send to Dancer

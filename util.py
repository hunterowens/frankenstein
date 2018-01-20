from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder
import logging 
# const
ip_osc = '192.168.1.255'
##ip_osc = '192.168.0.255'
##ip_osc = '0.0.0.0'
ip_osc_server='196.168,1.255'
ip_osc_editor='196.168.1.255'
## ip_osc = '10.253.0.255'
port_server = 7007
port_client = 7007
port_client_editor = 7007
api_url = "http://frankenstein.hunterowens.net/"

logger = logging.getLogger('util.module')
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
def osc_dispatch(addr, msg, ip=ip_osc_server, port=port_client, num_tries=1):
    """
    Dispatches a message in state change over OSC to all listeners
    """
    client = udp_client.UDPClient(ip, port,1)
    ## SimpleOSCClientRedux(client)
    ## client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    builder = osc_message_builder.OscMessageBuilder(address=addr)
    builder.add_arg(msg)
    for _ in range(num_tries):
        client.send(builder.build())
        logger.info("Sending {0} with {1} to {2} at {3}, Attempt {4}".format(addr, msg, ip, port, _))
    return None

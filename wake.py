import configparser
import os
import sys
import time

from multiping import MultiPing
from wakeonlan import send_magic_packet

import Checks

project_dir = os.path.dirname(os.path.abspath(__file__))
config_location = os.path.join(project_dir, 'config.ini')

# Import config file
config = configparser.RawConfigParser(allow_no_value=True)
config.read(config_location)


def check_server_online():
    mp = MultiPing(['192.168.1.201'])
    mp.send()
    responses, no_responses = mp.receive(1)
    if not no_responses:
        print("Server is online")
        return 1
    return 0

def wake():
    mac = config.get('WAKE', 'Mac')
    send_magic_packet(mac)
    Checks.pushover("Waking up server")


if __name__ == "__main__":
    solarthres = int(config.get('WAKE', 'Solarthres'))
    while True:
        # Skip everything if server is online already
        if not check_server_online():
            solarwatt = Checks.getSolar()
            if solarwatt > solarthres:
                print("enough energy is generated, waking up server")
                wake()
            else:
                print("not enough energy is generated: " + str(solarwatt) + " watt")
            # else:
            #     print("no hosts are online")
        print("Sleeping for 15 minutes")
        sys.stdout.flush()
        time.sleep(900)

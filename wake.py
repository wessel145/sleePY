import configparser
import time

from wakeonlan import send_magic_packet

import Checks

config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

def wake():
    mac = config.get('WAKE', 'Mac')
    send_magic_packet(mac)

if __name__ == "__main__":
    solarthres = int(config.get('WAKE', 'Solarthres'))
    while True:
        onlinehosts = Checks.pings()
        solarwatt = Checks.getSolar()
        if onlinehosts == 0:
            print("some hosts online")
            if solarwatt > solarthres:
                print("enough energy is generated")
                wake()
            else:
                print("not enough energy is generated: " + str(solarwatt) + " watt")

        else:
            print("no hosts are online")
        print("Sleeping for 15 minutes")
        time.sleep(900)

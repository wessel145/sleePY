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
    solarthres = config.get('WAKE', 'Solarthres')
    while True:
        onlinehosts = Checks.pings()
        solarwatt = Checks.getSolar()
        if onlinehosts() == 0:
            print("some hosts online")
        if solarwatt > solarthres:
            print("enough energy is generated")
        time.sleep(900)

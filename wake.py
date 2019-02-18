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
        solarwatt = Checks.getSolar()
        if Checks.pings() == 0:
            print("some hosts online")
        if (solarwatt) > int(solarthres):
            print("enough energy is generated")
        else:
            print(solarwatt, solarthres)
        time.sleep(900)

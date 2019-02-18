import configparser
import time

import Checks

# Import config file
config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")


def hibernate():
    print("going to sleep! bye")
    # Actual shutdown command (make sure command is in visudo)
    # subprocess.call(["sudo", "systemctl", "hibernate"])


if __name__ == "__main__":
    solarthres = int(config.get('SOLAR', 'Threshold'))
    while True:
        hddidle = Checks.check_drive_status()
        cpuidle = Checks.check_cpu_status()
        netidle = Checks.check_network_status()
        hostsoffline = Checks.pings()
        solarvalue = Checks.getSolar()
        # Checks for debug
        # print(hddidle, cpuidle, netidle, hostsoffline)
        # If current generated Watts is lower than thres:
        if solarthres > solarvalue:
            # If CPU/HDD/NETWORK is idle & All hosts are offline
            if hddidle == cpuidle == netidle == hostsoffline == 1:
                # Execute Sleep
                hibernate()
                break
        else:
            print("Current solar generation: " + str(solarvalue) + " watts, threshold: " + str(solarthres))
        print("Sleeping for 15 minutes...")
        time.sleep(900)

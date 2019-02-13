import configparser
import subprocess
import time

import psutil
from multiping import MultiPing

# Import config file
config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

# Read config file
network_interface = config.get('Network', 'Interface')
drives = config.get('HDD', 'Monitored').split(',')
hosts = config.get('PING', 'Hosts').split(',')
cpu_Threshold = int(config.get('CPU', 'Threshold'))


def check_drive_status():
    for drive in drives:
        result = str(subprocess.check_output(['hdparm', '-C', drive]))
        if "active" in result:
            print(drive, " \tactive")
            return 0
        else:
            print(drive, " \tstandby")
    return 1



def check_cpu_status():
    load = psutil.cpu_percent(interval=0.3)
    print("cpu: \t", load, "\t%")
    if load > cpu_Threshold:
        print("CPU usage above Threshold, Load: ", load, " Threshold: ", cpu_Threshold)
        return 0
    else:
        return 1


def check_network_status():
    tx1 = psutil.net_io_counters(pernic=True)[network_interface][0]
    rx1 = psutil.net_io_counters(pernic=True)[network_interface][1]
    time.sleep(1)
    tx2 = psutil.net_io_counters(pernic=True)[network_interface][0]
    rx2 = psutil.net_io_counters(pernic=True)[network_interface][1]

    tx_speed = int((tx2 - tx1) / 1000.0)
    rx_speed = int((rx2 - rx1) / 1000.0)

    print("tx: \t", tx_speed, "\tkbps")
    print("rx: \t", rx_speed, "\tkbps")


def pings():
    mp = MultiPing(hosts)
    mp.send()
    responses, no_responses = mp.receive(1)
    for host in responses:
        print("Host: ", host, " is online")
    for host in no_responses:
        print("Host: ", host, " is offline")


value = check_drive_status()
check_cpu_status()
check_network_status()
pings()

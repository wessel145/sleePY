import configparser
import subprocess
import time

import psutil

# Import config file
config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

# Read config file
network_interface = config.get('Network', 'Interface')
drives = config.get('HDD', 'Monitored').split(',')
cpu_Threshold = config.get('CPU', 'Threshold')


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
    print("cpu: \t", psutil.cpu_percent(interval=0.3), "\t%")


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


value = check_drive_status()
check_cpu_status()
check_network_status()

import configparser
import subprocess
import time

import psutil
# Import config file
import pymysql
from multiping import MultiPing

config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

# Read config file
network_interface = config.get('Network', 'Interface')
drives = config.get('HDD', 'Monitored').split(',')
hosts = config.get('PING', 'Hosts').split(',')
cpu_Threshold = int(config.get('CPU', 'Threshold'))
tx_Threshold = int(config.get('NETWORK', 'Upload_thres'))
rx_Threshold = int(config.get('NETWORK', 'Download_thres'))


def check_drive_status():
    for drive in drives:
        result = str(subprocess.check_output(['hdparm', '-C', drive]))
        if "active" in result:
            print(drive, " \tis active, aborting..")
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

    if tx_speed > tx_Threshold:
        return 0
    elif rx_speed > rx_Threshold:
        return 0
    return 1


def pings():
    mp = MultiPing(hosts)
    mp.send()
    responses, no_responses = mp.receive(1)
    # Debugging
    for host in responses:
        print("Host: ", host, " is online")
    for host in no_responses:
        print("Host: ", host, " is offline")
    if not no_responses:
        print("All hosts online")
        return 0
    if not responses:
        print("All hosts offline")
        return 1
    # If some hosts are online and some are offline
    return 0


def getSolar():
    ip = config.get('SOLAR', 'serverip')
    db = config.get('SOLAR', 'database')
    table = config.get('SOLAR', 'table')
    username = config.get('SOLAR', 'username')
    password = config.get('SOLAR', 'password')
    threshold = config.get('SOLAR', 'Threshold')
    query = "SELECT ACWATT FROM " + table + " ORDER BY log_id desc limit 1"
    mariadb_connection = pymysql.connect(host=ip, user=username, password=password, database=db)
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute(query)
        solarwatt = cursor.fetchone()[0]
        print("Current solar generation: \t" + str(solarwatt) + "\t watts")
    except pymysql.Error as error:
        print("Error: {}".format(error))
        return 0
    if int(solarwatt) < int(threshold):
        return 1
    else:
        return 0

import subprocess
import time

import psutil

network_interface = 'eno1'

drives = {'/dev/sdb',
          '/dev/sdc',
          '/dev/sdd',
          '/dev/sde',
          }


def check_drive_status():
    for drive in drives:
        result = str(subprocess.check_output(['hdparm', '-C', drive]))
        if "standby" in result:
            print(drive, " \tstandby")
        else:
            print(drive, " \tactive")


def check_cpu_status():
    print("cpu: \t", psutil.cpu_percent(interval=0.3), "\t%")


def check_network_status():
    send1 = psutil.net_io_counters(pernic=True)[network_interface][0]
    recv1 = psutil.net_io_counters(pernic=True)[network_interface][1]
    time.sleep(1)
    send2 = psutil.net_io_counters(pernic=True)[network_interface][0]
    recv2 = psutil.net_io_counters(pernic=True)[network_interface][1]

    tx_speed = int((send2 - send1) / 1000.0)
    rx_speed = int((recv2 - recv1) / 1000.0)

    print("tx: \t", tx_speed, "\tkbps")
    print("rx: \t", rx_speed, "\tkbps")

check_drive_status()
check_cpu_status()
check_network_status()

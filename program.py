import psutil
import GPUtil
import platform
import keyboard
import requests

import time
from datetime import datetime

AVG_CPU_LOAD = {
    "1": 0,
    "5": 0,
    "15": 0,
    "30": 0,
    "60": 0
}

# CPU LOAD ARCHIVE
CPU_LOADS_ARCH = {
    "1": [],
    "5": [],
    "15": [],
    "30": [],
    "60": []
}

PROGRAM_START_TIME = time.time()
LAST_PERIOD_1 = PROGRAM_START_TIME + 60
LAST_PERIOD_5 = PROGRAM_START_TIME + 5*60
LAST_PERIOD_15 = PROGRAM_START_TIME + 15*60
LAST_PERIOD_30 = PROGRAM_START_TIME + 30*60
LAST_PERIOD_60 = PROGRAM_START_TIME + 60*60

MAX_CPU_LOAD_PERC = 0
MAX_CPU_LOAD_TIME = ""

DISK_USAGE_PATH = "C:\\"

API_ENDPOINT = ""
API_TOKEN_NAME = ""
API_TOKEN_VALUE = ""
REPORT_FREQUENCY = 99

LAST_REPORT_SEND = 0

RUN_CHECK_EVERY_SECONDS = 30

def load_config():
    global API_ENDPOINT, API_TOKEN_NAME, API_TOKEN_VALUE, REPORT_FREQUENCY, DISK_USAGE_PATH, RUN_CHECK_EVERY_SECONDS
    import json

    # Read the JSON file
    with open("config.json", "r") as file:
        config = json.load(file)
        API_ENDPOINT = config['api_endpoint']
        API_TOKEN_NAME = config['api_token_name']
        API_TOKEN_VALUE = config['api_token_value']
        REPORT_FREQUENCY = config['send_report_every_mins']
        DISK_USAGE_PATH = config['disk_usage_path']
        RUN_CHECK_EVERY_SECONDS = config['run_check_every_seconds']
def get_system_metrics():
    global DISK_USAGE_PATH
    # CPU load
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()

    # Memory load
    memory_info = psutil.virtual_memory()
    memory_load = memory_info.percent

    # CPU temperature (Linux, needs 'sensors' module; may not work on all systems)
    if hasattr(psutil, "sensors_temperatures"):
        cpu_temp_info = psutil.sensors_temperatures().get("coretemp", [])
        cpu_temp = cpu_temp_info[0].current if cpu_temp_info else None
    else:
        cpu_temp = None

    # GPU load (using GPUtil)
    gpu_info = GPUtil.getGPUs()
    gpu_load = gpu_info[0].load * 100 if gpu_info else None

    # disk load
    disk_usage = psutil.disk_usage(DISK_USAGE_PATH)

    return {
        "cpu_count": cpu_count,
        "cpu_load": cpu_load,
        "memory_load": memory_load,
        "cpu_temperature": cpu_temp,
        "gpu_load": gpu_load,
        "disk_usage_free_gb": round(disk_usage.free/1024**3),
        "disk_usage_perc": round(disk_usage.percent)
    }

def getHardwareInfo():
    cpu = platform.processor()
    system = platform.system()

    return {
        "cpu": cpu,
        "system": system
    }

def printStatistic():
    global AVG_CPU_LOAD

    metrics = get_system_metrics()
    print("System Metrics:")
    print(f"CPU Count: {metrics['cpu_count']} threads")
    print(f"CPU Load: {metrics['cpu_load']}%")
    print(f"Memory Load: {metrics['memory_load']}%")
    print("\n")
    print(f"Disk usage free [GB]: {metrics['disk_usage_free_gb']}")
    print(f"Disk usage [%]: {metrics['disk_usage_perc']}")
    print("\n")
    print(f"CPU Temperature: {metrics['cpu_temperature']}°C" if metrics['cpu_temperature'] else "N/A")
    print(f"GPU Load: {metrics['gpu_load']}%" if metrics['gpu_load'] else "N/A")
    print("\n")
    print("Last Max CPU LOAD [%]: ", MAX_CPU_LOAD_PERC)
    print("Last Max CPU LOAD @: ", MAX_CPU_LOAD_TIME)
    print("\n")
    print("Average CPU Load: ")
    for m, l in AVG_CPU_LOAD.items():
        print("\t Average CPU load in last {} minutes: {}%" . format(m, l))


def getCpuAvg(cpuloads, cpu_count):
    if len(cpuloads) == 0:
        return 0
    avg = sum(cpuloads)/len(cpuloads)
    return avg
    #print("CPU LOADS: ", cpuloads)
    #return ( (avg /  cpu_count) * 100 )
def analyze():
    global LAST_PERIOD_1, LAST_PERIOD_5, LAST_PERIOD_15, LAST_PERIOD_30, LAST_PERIOD_60
    global CPU_LOADS_ARCH, MAX_CPU_LOAD_PERC, MAX_CPU_LOAD_TIME

    time_now = time.time()
    metrics = get_system_metrics()

    cpu_count = metrics['cpu_count']
    cpu_load = metrics['cpu_load']

    if cpu_load >= MAX_CPU_LOAD_PERC:
        current_datetime = datetime.now()
        MAX_CPU_LOAD_PERC = cpu_load
        MAX_CPU_LOAD_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if time_now > LAST_PERIOD_1:
        LAST_PERIOD_1 = time_now + 60
        AVG_CPU_LOAD["1"] = getCpuAvg(CPU_LOADS_ARCH["1"], cpu_count)
        CPU_LOADS_ARCH["1"] = []

    if time_now > LAST_PERIOD_5:
        LAST_PERIOD_5 = time_now + 5*60
        AVG_CPU_LOAD["5"] = getCpuAvg(CPU_LOADS_ARCH["5"], cpu_count)
        CPU_LOADS_ARCH["5"] = []

    if time_now > LAST_PERIOD_15:
        LAST_PERIOD_15 = time_now + 15*60
        AVG_CPU_LOAD["15"] = getCpuAvg(CPU_LOADS_ARCH["15"], cpu_count)
        CPU_LOADS_ARCH["15"] = []

    if time_now > LAST_PERIOD_30:
        LAST_PERIOD_30 = time_now + 30*60
        AVG_CPU_LOAD["30"] = getCpuAvg(CPU_LOADS_ARCH["30"], cpu_count)
        CPU_LOADS_ARCH["30"] = []

    if time_now > LAST_PERIOD_60:
        LAST_PERIOD_60 = time_now + 60*60
        AVG_CPU_LOAD["60"] = getCpuAvg(CPU_LOADS_ARCH["60"], cpu_count)
        CPU_LOADS_ARCH["60"] = []

    CPU_LOADS_ARCH["1"].append(cpu_load)
    CPU_LOADS_ARCH["5"].append(cpu_load)
    CPU_LOADS_ARCH["15"].append(cpu_load)
    CPU_LOADS_ARCH["30"].append(cpu_load)
    CPU_LOADS_ARCH["60"].append(cpu_load)

def reportStatistic():
    global LAST_REPORT_SEND, API_ENDPOINT, REPORT_FREQUENCY
    time_now = time.time()

    if time_now < LAST_REPORT_SEND:
        return

    LAST_REPORT_SEND = time_now +REPORT_FREQUENCY * 60

    metrics = get_system_metrics()
    hwinfo = getHardwareInfo()

    report = {
        API_TOKEN_NAME: API_TOKEN_VALUE,
        "system": {
            "cpu_count": metrics['cpu_count'],
            "system_info": hwinfo['system'],
            "cpu": hwinfo['cpu']
        },
        "current": {
            "cpu_load": metrics['cpu_load'],
            "gpu_load": metrics['gpu_load'],
            "memory_load": metrics['memory_load'],
            "cpu_temp": metrics['cpu_temperature'],
            "disk": {
                "usage_gb": metrics['disk_usage_free_gb'],
                "usage_perc": metrics['disk_usage_perc']
            }
        },
        "history": {
            "cpu_load_avg": AVG_CPU_LOAD,
            "last_max_cpu_load": {
                "load": MAX_CPU_LOAD_PERC,
                "time": MAX_CPU_LOAD_TIME
            }
        }
    }

    response = requests.post(API_ENDPOINT, json=report)
    if response.status_code != 200:
        print("Response code not OK")

if __name__ == "__main__":
    print("\n\n")
    print("\t Hardware monitoring and reporting system by Sandi")
    print("\t Version: 1.0")
    print("\n\n")
    print("\t To exit the program, hold 'Q', or you know... the good old CTRL+C")
    print("\n")

    print("\t Loading config....")
    load_config()
    print("\t Config is loaded...")
    print("\n")
    print("Run analyze every {} second(s)" . format(RUN_CHECK_EVERY_SECONDS))
    print("\n")
    hwinfo = getHardwareInfo()
    print("CPU: ", hwinfo['cpu'])
    print("System: ", hwinfo['system'])

    last_check = 0
    while True:
        time_now = time.time()

        # run analyze every RUN_CHECK_EVERY_SECONDS seconds
        if time_now > last_check:
            printStatistic()
            analyze()
            last_check = time_now + RUN_CHECK_EVERY_SECONDS
            reportStatistic()

        time.sleep(2)
        # Check if 'Q' has been pressed to exit
        if keyboard.is_pressed("q"):
            print("Exiting monitoring...")
            break


import platform
import time
from datetime import datetime

import GPUtil
import WinTmp
import psutil
import requests
import keyboard

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

DISK_USAGE_PATHS = ["C:\\"]

API_ENDPOINT = ""
API_TOKEN_NAME = ""
API_TOKEN_VALUE = ""
REPORT_FREQUENCY = 99

LAST_REPORT_SEND = 0

RUN_CHECK_EVERY_SECONDS = 30

NET_IO_START = dict()
NET_IO_END = dict()
TOTAL_NETWORK_TRANSFER = {
    "download": 0,
    "upload": 0,
    "download_unit": "B",
    "upload_unit": "B"
}

PRINT_TO_CONSOLE = True

def load_config():
    global API_ENDPOINT, API_TOKEN_NAME, API_TOKEN_VALUE, REPORT_FREQUENCY, DISK_USAGE_PATHS, RUN_CHECK_EVERY_SECONDS
    global PRINT_TO_CONSOLE
    import json

    # Read the JSON file
    with open("config.json", "r") as file:
        config = json.load(file)
        API_ENDPOINT = config['api_endpoint']
        API_TOKEN_NAME = config['api_token_name']
        API_TOKEN_VALUE = config['api_token_value']
        REPORT_FREQUENCY = config['send_report_every_mins']
        DISK_USAGE_PATHS = config['disk_usage_paths']
        RUN_CHECK_EVERY_SECONDS = config['run_check_every_seconds']
        PRINT_TO_CONSOLE = config['print_to_console']

def get_system_metrics():
    global DISK_USAGE_PATHS
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
    disk_usages = {path: psutil.disk_usage(path) for path in DISK_USAGE_PATHS}
    disk_usages = {path: {"free_gb": round(du.free/1024**3), "free_perc": round(du.percent)} for path, du in disk_usages.items()}

    network = get_network_speed()

    return {
        "cpu_count": cpu_count,
        "cpu_load": cpu_load,
        "memory_load": memory_load,
        "cpu_temperature": cpu_temp,
        "cpu_temp_alt": WinTmp.CPU_Temp(),
        "gpu_temp": WinTmp.GPU_Temp(),
        "gpu_load": gpu_load,
        "disk_usages": disk_usages,
        "network": network
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
    _print("System Metrics:")
    _print(f"CPU Count: {metrics['cpu_count']} threads")
    _print(f"CPU Load: {metrics['cpu_load']}%")
    _print(f"Memory Load: {metrics['memory_load']}%")
    _print("\n")
    _print("Disks info:")
    for path, du in metrics['disk_usages'].items():
        _print("{}: {}" . format(path, du))
    _print("\n")
    _print("Network speed: ")
    _print("\t Total download: ", metrics['network']['total_download_kBps'])
    _print("\t Total upload: ", metrics['network']['total_upload_kBps'])
    _print("\n")
    _print(f"CPU Temperature: {metrics['cpu_temperature']}°C" if metrics['cpu_temperature'] else "N/A")
    _print(f"GPU Load: {metrics['gpu_load']}%" if metrics['gpu_load'] else "N/A")
    _print("\n")
    _print("Last Max CPU LOAD [%]: ", MAX_CPU_LOAD_PERC)
    _print("Last Max CPU LOAD @: ", MAX_CPU_LOAD_TIME)
    _print("\n")
    _print("Average CPU Load: ")
    for m, l in AVG_CPU_LOAD.items():
        _print("\t Average CPU load in last {} minutes: {}%" . format(m, l))

    _print("-----" * 20)

def get_network_speed():
    global NET_IO_START, NET_IO_END, RUN_CHECK_EVERY_SECONDS, TOTAL_NETWORK_TRANSFER


    nics = [nic for nic in NET_IO_START.keys()]

    stats = dict()
    total_upload_kBps = 0
    total_download_kBps = 0

    for nic in nics:
        s, e = NET_IO_START[nic], NET_IO_END[nic]
        upload_speed = abs(e.bytes_sent - s.bytes_sent) / RUN_CHECK_EVERY_SECONDS
        download_speed = abs(e.bytes_recv - s.bytes_recv) / RUN_CHECK_EVERY_SECONDS
        upload_speed_kBps = upload_speed // 1024
        download_speed_kBps = download_speed // 1024
        total_upload_kBps += upload_speed_kBps
        total_download_kBps += download_speed_kBps
        stats[nic] = {
            "upload_speed_kBps": upload_speed_kBps,
            "download_speed_kBps": download_speed_kBps
        }

        TOTAL_NETWORK_TRANSFER['download'] = s.bytes_recv
        TOTAL_NETWORK_TRANSFER['upload'] = s.bytes_sent

    if TOTAL_NETWORK_TRANSFER['download'] > 1024:
        TOTAL_NETWORK_TRANSFER['download'] = TOTAL_NETWORK_TRANSFER['download'] // 1024
        TOTAL_NETWORK_TRANSFER['download_unit'] = 'KB'
    if TOTAL_NETWORK_TRANSFER['download'] > 1024:
        TOTAL_NETWORK_TRANSFER['download'] = TOTAL_NETWORK_TRANSFER['download'] // 1024
        TOTAL_NETWORK_TRANSFER['download_unit'] = 'MB'
    if TOTAL_NETWORK_TRANSFER['download'] > 1024:
        TOTAL_NETWORK_TRANSFER['download'] = TOTAL_NETWORK_TRANSFER['download'] // 1024
        TOTAL_NETWORK_TRANSFER['download_unit'] = 'GB'

    if TOTAL_NETWORK_TRANSFER['upload'] > 1024:
        TOTAL_NETWORK_TRANSFER['upload'] = TOTAL_NETWORK_TRANSFER['upload'] // 1024
        TOTAL_NETWORK_TRANSFER['upload_unit'] = 'KB'
    if TOTAL_NETWORK_TRANSFER['upload'] > 1024:
        TOTAL_NETWORK_TRANSFER['upload'] = TOTAL_NETWORK_TRANSFER['upload'] // 1024
        TOTAL_NETWORK_TRANSFER['upload_unit'] = 'MB'
    if TOTAL_NETWORK_TRANSFER['upload'] > 1024:
        TOTAL_NETWORK_TRANSFER['upload'] = TOTAL_NETWORK_TRANSFER['upload'] // 1024
        TOTAL_NETWORK_TRANSFER['upload_unit'] = 'GB'

    stats = {
        "total_upload_kBps": total_upload_kBps,
        "total_download_kBps": total_download_kBps,
        "per_nic": stats
    }
    return stats

def getCpuAvg(cpuloads, cpu_count):
    if len(cpuloads) == 0:
        return 0
    avg = sum(cpuloads)/len(cpuloads)
    return round(avg)
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
            "cpu_temp_alt": metrics['cpu_temp_alt'],
            "gpu_temp": metrics['gpu_temp'],
            "disks": dict(),
            "network": metrics['network']
        },
        "history": {
            "cpu_load_avg": AVG_CPU_LOAD,
            "last_max_cpu_load": {
                "load": MAX_CPU_LOAD_PERC,
                "time": MAX_CPU_LOAD_TIME
            },
            "network": {
                "total_transfer": TOTAL_NETWORK_TRANSFER
            }
        }
    }

    for path, du in metrics['disk_usages'].items():
        report['current']['disks'][path] = du

    response = requests.post(API_ENDPOINT, json=report)
    if response.status_code != 200:
        print("Response code not OK")

def _print(arg, *args):
    global PRINT_TO_CONSOLE
    if PRINT_TO_CONSOLE:
        print(arg, *args)

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
    print("Output to console is set to: ", PRINT_TO_CONSOLE)
    print("\n")
    hwinfo = getHardwareInfo()
    print("CPU: ", hwinfo['cpu'])
    print("System: ", hwinfo['system'])

    last_check = 0
    while True:
        time_now = time.time()
        NET_IO_END = psutil.net_io_counters(pernic=True)
        # run analyze every RUN_CHECK_EVERY_SECONDS seconds
        if time_now > last_check:
            printStatistic()
            analyze()
            last_check = time_now + RUN_CHECK_EVERY_SECONDS
            reportStatistic()
            NET_IO_START = psutil.net_io_counters(pernic=True)

        time.sleep(2)
        # Check if 'Q' has been pressed to exit
        if keyboard.is_pressed("q"):
            print("Exiting monitoring...")
            break


import platform
import sys
import time
import threading

from datetime import datetime
from json import load as jsload
from json import dump as jsdump
from json import JSONDecodeError

import GPUtil
import WinTmp
import psutil
import requests
import keyboard

from gui import GUI

def writeLog(file_path, text):
    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    text = "[{}] :: {}\n" . format(timestamp, text)
    with open(file_path, 'a') as file:  # 'a' mode opens the file for appending
        file.write(text)

def appendErrorLog(text):
    writeLog('./error_log', text)
class HwInfoReport:
    def about(self):
        print("\n")
        print("\t Hardware monitoring and reporting system by Sandi")
        print("\t Version: {}" . format(self.version))
        print("\n")
        print("\t To exit the program, hold 'Q', or you know... the good old CTRL+C")
        print("\n")

    def _print(self, arg, *args):
        if self.PRINT_TO_CONSOLE:
            print(arg, *args)

    def __init__(self):
        self.version = "3.4.1"

        self.SHOW_GUI = False

        self.AVG_CPU_LOAD = {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0,
            "360": 0,
            "720": 0
        }

        self.MAX_CPU_LOAD = {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0,
            "360": 0,
            "720": 0
        }

        # CPU LOAD ARCHIVE
        self.CPU_LOADS_ARCH = {
            "1": [0],
            "5": [0],
            "15": [0],
            "30": [0],
            "60": [0],
            "360": [0],
            "720": [0]
        }

        # GPU LOAD ARCHIVE
        self.GPU_LOADS_ARCH = {
            "1": [0],
            "5": [0],
            "15": [0],
            "30": [0],
            "60": [0],
            "360": [0],
            "720": [0]
        }

        self.PROGRAM_START_TIME = time.time()

        self.MAX_CPU_LOAD_PERC = 0
        self.MAX_CPU_LOAD_TIME = ""

        self.MAX_NET_DOWNLOAD = 0
        self.MAX_NET_DOWNLOAD_TIME = ""
        self.MAX_NET_UPLOAD = 0
        self.MAX_NET_UPLOAD_TIME = ""

        self.DISK_USAGE_PATHS = ["C:\\"]

        self.API_ENDPOINTS = []
        self.REMOTE_CONTROL_POLLING = []
        self.REMOTE_CONTROL_POLL_FREQUENCY = 60
        self.REMOTE_CONTROL_POLL_COMMANDS = []
        self.LAST_REMOTE_CONTROL_POLL_RUNTIME = 0
        self.LAST_EXECUTED_REMOTE_POLL_COMMAND = ""
        self.LAST_EXECUTED_REMOTE_POLL_COMMAND_TIME = ""
        self.UNIQUE_ID = ""
        self.REPORT_FREQUENCY = 99

        self.LAST_REPORT_SEND = 0

        self.RUN_CHECK_EVERY_SECONDS = 30

        self.NET_IO_START = dict()
        self.NET_IO_END = dict()
        self.MAX_NET_DOWNLINK_KBPS = 0
        self.MAX_NET_UPLINK_KBPS = 0
        self.TOTAL_NETWORK_TRANSFER = {
            "download": 0,
            "upload": 0,
            "download_unit": "B",
            "upload_unit": "B"
        }

        self.PRINT_TO_CONSOLE = True
        self.PRINT_REPORT_TIMESTAMPS = True

        self.INCLUDE_PROCESS_MONITORING = False

        self.LOGS = []
        self.LOG_SIZE = 50

        self.USE_MODULES = []
        self.CUSTOM_FLAGS = dict()

    def appendToLogs(self, type_, content):
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.LOGS.append({
            "timestamp": timestamp,
            "type": type_,
            "content": content
        })

        self.LOGS = self.LOGS[-self.LOG_SIZE:]
    def resetStatistics(self):
        self.AVG_CPU_LOAD = {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0,
            "360": 0,
            "720": 0
        }

        self.MAX_CPU_LOAD = {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0,
            "360": 0,
            "720": 0
        }

        # CPU LOAD ARCHIVE
        self.CPU_LOADS_ARCH = {
            "1": [0],
            "5": [0],
            "15": [0],
            "30": [0],
            "60": [0],
            "360": [0],
            "720": [0]
        }

        # GPU LOAD ARCHIVE
        self.GPU_LOADS_ARCH = {
            "1": [0],
            "5": [0],
            "15": [0],
            "30": [0],
            "60": [0],
            "360": [0],
            "720": [0]
        }

        self.MAX_CPU_LOAD_PERC = 0
        self.MAX_CPU_LOAD_TIME = ""

        self.MAX_NET_DOWNLOAD = 0
        self.MAX_NET_DOWNLOAD_TIME = ""
        self.MAX_NET_UPLOAD = 0
        self.MAX_NET_UPLOAD_TIME = ""

        self.MAX_NET_DOWNLINK_KBPS = 0
        self.MAX_NET_UPLINK_KBPS = 0
        self.TOTAL_NETWORK_TRANSFER = {
            "download": 0,
            "upload": 0,
            "download_unit": "B",
            "upload_unit": "B"
        }
    def load_config(self):
        with open("config.json", "r") as file:
            config = jsload(file)
            self.API_ENDPOINTS = config['api_endpoints']
            self.UNIQUE_ID = config['unique_id']
            self.REPORT_FREQUENCY = config['send_report_every_mins']
            self.DISK_USAGE_PATHS = config['disk_usage_paths']
            self.RUN_CHECK_EVERY_SECONDS = config['run_check_every_seconds']
            self.PRINT_TO_CONSOLE = config['print_to_console']
            self.PRINT_REPORT_TIMESTAMPS = config['print_report_timestamps']
            self.MAX_NET_DOWNLINK_KBPS = config['max_net_downlink_kbps']
            self.MAX_NET_UPLINK_KBPS = config['max_net_uplink_kbps']
            self.INCLUDE_PROCESS_MONITORING = config['include_process_monitoring']
            self.REMOTE_CONTROL_POLLING = config['remote_control_polling']
            self.REMOTE_CONTROL_POLL_FREQUENCY = config['remote_control_poll_every_seconds']
            self.REMOTE_CONTROL_POLL_COMMANDS = config['remote_control_poll_commands']
            self.SHOW_GUI = config['show_gui']
            self.LOG_SIZE = config['log_size']
            self.USE_MODULES = config['use_modules']
            self.CUSTOM_FLAGS = config['customFlags']

        print("\t\t Run analyze every {} second(s)" . format(self.RUN_CHECK_EVERY_SECONDS))
        print("\t\t Output to console is set to: ", self.PRINT_TO_CONSOLE)
        print("\t\t Report to every {} minute(s) " . format(self.REPORT_FREQUENCY))

    def update_json_file(self, key_, value):
        file_path = "config.json"
        # Read the existing JSON data from the file
        try:
            with open(file_path, 'r') as file:
                data = jsload(file)
        except FileNotFoundError:
            #print(f"File not found: {file_path}")
            return
        except JSONDecodeError:
            #print("Error decoding JSON from the file.")
            return

        # Update the JSON data
        data[key_] = value

        # Write the updated JSON data back to the file
        with open(file_path, 'w') as file:
            jsdump(data, file, indent=4)
    def update_config_callback(self, key_, value_):
        key_map = {
            "UNIQUE_ID": "unique_id",
            "LOG_SIZE": "log_size"
        }
        setattr(self, key_, value_)
        self.update_json_file(key_map[key_], value_)
    def getHardwareInfo(self):
        cpu = platform.processor()
        system = platform.system()

        return {
            "cpu": cpu,
            "system": system
        }

    def getCpuAvg(self, cpuloads):
        if len(cpuloads) == 0:
            return 0
        avg = sum(cpuloads) / len(cpuloads)
        return round(avg)

    def get_network_speed(self):
        nics = [nic for nic in self.NET_IO_START.keys()]

        stats = dict()
        total_upload_kBps = 0
        total_download_kBps = 0

        for nic in nics:
            s, e = self.NET_IO_START[nic], self.NET_IO_END[nic]
            upload_speed = abs(e.bytes_sent - s.bytes_sent) / self.RUN_CHECK_EVERY_SECONDS
            download_speed = abs(e.bytes_recv - s.bytes_recv) / self.RUN_CHECK_EVERY_SECONDS
            upload_speed_kBps = upload_speed // 1024
            download_speed_kBps = download_speed // 1024
            total_upload_kBps += upload_speed_kBps
            total_download_kBps += download_speed_kBps
            stats[nic] = {
                "upload_speed_kBps": upload_speed_kBps,
                "download_speed_kBps": download_speed_kBps
            }

            self.TOTAL_NETWORK_TRANSFER['download'] += s.bytes_recv
            self.TOTAL_NETWORK_TRANSFER['upload'] += s.bytes_sent

        if self.TOTAL_NETWORK_TRANSFER['download'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['download'] = self.TOTAL_NETWORK_TRANSFER['download'] // 1024
            self.TOTAL_NETWORK_TRANSFER['download_unit'] = 'KB'
        if self.TOTAL_NETWORK_TRANSFER['download'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['download'] = self.TOTAL_NETWORK_TRANSFER['download'] // 1024
            self.TOTAL_NETWORK_TRANSFER['download_unit'] = 'MB'
        if self.TOTAL_NETWORK_TRANSFER['download'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['download'] = self.TOTAL_NETWORK_TRANSFER['download'] // 1024
            self.TOTAL_NETWORK_TRANSFER['download_unit'] = 'GB'

        if self.TOTAL_NETWORK_TRANSFER['upload'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['upload'] = self.TOTAL_NETWORK_TRANSFER['upload'] // 1024
            self.TOTAL_NETWORK_TRANSFER['upload_unit'] = 'KB'
        if self.TOTAL_NETWORK_TRANSFER['upload'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['upload'] = self.TOTAL_NETWORK_TRANSFER['upload'] // 1024
            self.TOTAL_NETWORK_TRANSFER['upload_unit'] = 'MB'
        if self.TOTAL_NETWORK_TRANSFER['upload'] > 1024:
            self.TOTAL_NETWORK_TRANSFER['upload'] = self.TOTAL_NETWORK_TRANSFER['upload'] // 1024
            self.TOTAL_NETWORK_TRANSFER['upload_unit'] = 'GB'

        current_datetime = datetime.now()
        if total_download_kBps*8 > self.MAX_NET_DOWNLOAD:
            self.MAX_NET_DOWNLOAD = total_download_kBps*8
            self.MAX_NET_DOWNLOAD_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if total_upload_kBps*8 > self.MAX_NET_UPLOAD:
            self.MAX_NET_UPLOAD = total_upload_kBps*8
            self.MAX_NET_UPLOAD_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        download_kbps = total_download_kBps * 8
        upload_kbps = total_upload_kBps * 8
        stats = {
            "total_download_kBps": total_download_kBps,
            "total_upload_kBps": total_upload_kBps,
            "total_download_kbps": download_kbps,
            "total_upload_kbps": upload_kbps,
            "download_usage_perc": round((download_kbps / self.MAX_NET_DOWNLINK_KBPS)*100, 2) if self.MAX_NET_DOWNLINK_KBPS > 0 else 0,
            "upload_usage_perc": round((upload_kbps / self.MAX_NET_UPLINK_KBPS)*100, 2) if self.MAX_NET_UPLINK_KBPS > 0 else 0,
            "per_nic": stats
        }
        return stats

    def get_system_metrics(self):
        # CPU load
        cpu_load = psutil.cpu_percent(interval=1)
        core_count = psutil.cpu_count(logical=False)
        thread_count = psutil.cpu_count()

        # Memory load
        memory_info = psutil.virtual_memory()
        memory_load = memory_info.percent

        # CPU temperature (Linux, needs 'sensors' module; may not work on all systems)
        if hasattr(psutil, "sensors_temperatures"):
            cpu_temp_info = psutil.sensors_temperatures().get("coretemp", [])
            cpu_temp = cpu_temp_info[0].current if cpu_temp_info else None
        else:
            cpu_temp = None

        if hasattr(psutil, "sensors_fans"):
            fans_info = psutil.sensors_fans()
        else:
            fans_info = None

        # GPU load (using GPUtil)
        gpu_info = GPUtil.getGPUs()
        gpu_load = gpu_info[0].load * 100 if gpu_info else None

        # disk load
        disk_usages = {path: psutil.disk_usage(path) for path in self.DISK_USAGE_PATHS}
        disk_usages = {path: {"free_gb": round(du.free/1024**3), "free_perc": round(du.percent)} for path, du in disk_usages.items()}

        disk_total_free_gb = sum(d['free_gb'] for d in disk_usages.values())

        network = self.get_network_speed()

        cpu_temps = WinTmp.CPU_Temps() if WinTmp.CPU_Temps() else []
        all_temps = WinTmp._all_temps() if WinTmp._all_temps() else []

        cpu_clocks = psutil.cpu_freq()

        if cpu_clocks:
            cpu_clock_current = cpu_clocks.current

        vmem = psutil.virtual_memory()
        virtual_memory = {
            "available": vmem.available,
            "percent": vmem.percent
        }

        # find most intense processes
        processes = dict()
        if self.INCLUDE_PROCESS_MONITORING:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                username = proc.info['username']
                name = proc.info['name']
                pid = proc.info['pid']

                if "NT AUTHORITY" in username:
                    continue

                try:
                    p = psutil.Process(pid=pid)
                    with p.oneshot():
                        if name not in processes:
                            processes[name] = {"cpu": 0, "ram": 0, "name": name}
                        processes[name]['cpu'] += p.cpu_percent() * core_count
                        processes[name]['ram'] += p.memory_info().pagefile
                except:
                    pass


        return {
            "core_count": core_count,
            "thread_count": thread_count,
            "cpu_load": round(cpu_load, 2),
            "memory_load": round(memory_load, 2),
            "virtual_memory": virtual_memory,
            "cpu_temperature": cpu_temp,
            "cpu_temp_alt": max(cpu_temps),
            "cpu_temps": cpu_temps,
            "cpu_clocks": { "current": cpu_clock_current },
            "processes": processes,
            "gpu_temp": WinTmp.GPU_Temp(),
            "gpu_load": round(gpu_load, 2),
            "disk_usages": disk_usages,
            "disk_total_free_gb": disk_total_free_gb,
            "network": network,
            "fans_info": fans_info,
            "all_temps": all_temps
        }

    def analyze(self):
        time_now = time.time()
        metrics = self.get_system_metrics()

        core_count = metrics['core_count']
        cpu_load = metrics['cpu_load']
        gpu_load = metrics['gpu_load']

        if cpu_load >= self.MAX_CPU_LOAD_PERC:
            current_datetime = datetime.now()
            self.MAX_CPU_LOAD_PERC = cpu_load
            self.MAX_CPU_LOAD_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


        parts = 60 // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["1"] = self.getCpuAvg(self.CPU_LOADS_ARCH["1"])
        self.MAX_CPU_LOAD["1"] = max(self.CPU_LOADS_ARCH["1"])
        self.CPU_LOADS_ARCH["1"] = self.CPU_LOADS_ARCH["1"][-parts:]

        parts = (5*60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["5"] = self.getCpuAvg(self.CPU_LOADS_ARCH["5"])
        self.MAX_CPU_LOAD["5"] = max(self.CPU_LOADS_ARCH["5"])
        self.CPU_LOADS_ARCH["5"] = self.CPU_LOADS_ARCH["5"][-parts:]

        parts = (15 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["15"] = self.getCpuAvg(self.CPU_LOADS_ARCH["15"])
        self.MAX_CPU_LOAD["15"] = max(self.CPU_LOADS_ARCH["15"])
        self.CPU_LOADS_ARCH["15"] = self.CPU_LOADS_ARCH["15"][-parts:]

        parts = (30 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["30"] = self.getCpuAvg(self.CPU_LOADS_ARCH["30"])
        self.MAX_CPU_LOAD["30"] = max(self.CPU_LOADS_ARCH["30"])
        self.CPU_LOADS_ARCH["30"] = self.CPU_LOADS_ARCH["30"][-parts:]

        parts = (60 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["60"] = self.getCpuAvg(self.CPU_LOADS_ARCH["60"])
        self.MAX_CPU_LOAD["60"] = max(self.CPU_LOADS_ARCH["60"])
        self.CPU_LOADS_ARCH["60"] = self.CPU_LOADS_ARCH["60"][-parts:]

        parts = (360 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["360"] = self.getCpuAvg(self.CPU_LOADS_ARCH["360"])
        self.MAX_CPU_LOAD["360"] = max(self.CPU_LOADS_ARCH["360"])
        self.CPU_LOADS_ARCH["360"] = self.CPU_LOADS_ARCH["360"][-parts:]

        parts = (720 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.AVG_CPU_LOAD["720"] = self.getCpuAvg(self.CPU_LOADS_ARCH["720"])
        self.MAX_CPU_LOAD["720"] = max(self.CPU_LOADS_ARCH["720"])
        self.CPU_LOADS_ARCH["720"] = self.CPU_LOADS_ARCH["720"][-parts:]

        self.CPU_LOADS_ARCH["1"].append(cpu_load)
        self.CPU_LOADS_ARCH["5"].append(cpu_load)
        self.CPU_LOADS_ARCH["15"].append(cpu_load)
        self.CPU_LOADS_ARCH["30"].append(cpu_load)
        self.CPU_LOADS_ARCH["60"].append(cpu_load)
        self.CPU_LOADS_ARCH["360"].append(cpu_load)
        self.CPU_LOADS_ARCH["720"].append(cpu_load)

        parts = 60 // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["1"] = self.GPU_LOADS_ARCH["1"][-parts:]

        parts = (5 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["5"] = self.GPU_LOADS_ARCH["5"][-parts:]

        parts = (15 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["15"] = self.GPU_LOADS_ARCH["15"][-parts:]

        parts = (30 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["30"] = self.GPU_LOADS_ARCH["30"][-parts:]

        parts = (60 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["60"] = self.GPU_LOADS_ARCH["60"][-parts:]

        parts = (360 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["360"] = self.GPU_LOADS_ARCH["360"][-parts:]

        parts = (720 * 60) // self.RUN_CHECK_EVERY_SECONDS
        self.GPU_LOADS_ARCH["720"] = self.GPU_LOADS_ARCH["720"][-parts:]

        self.GPU_LOADS_ARCH["1"].append(gpu_load)
        self.GPU_LOADS_ARCH["5"].append(gpu_load)
        self.GPU_LOADS_ARCH["15"].append(gpu_load)
        self.GPU_LOADS_ARCH["30"].append(gpu_load)
        self.GPU_LOADS_ARCH["60"].append(gpu_load)
        self.GPU_LOADS_ARCH["360"].append(gpu_load)
        self.GPU_LOADS_ARCH["720"].append(gpu_load)

        return metrics

    def module_qbittorrent(self):
        from modules.qbittorrent import qbittorrent
        qb = qbittorrent.QBittorrent()
        qb.connect()
        torrents = qb.get_torrents()
        return {
            "torrents": torrents
        }

    def remote_control_qbittorrent(self, command, torrent_hash):
        from modules.qbittorrent import qbittorrent
        qb = qbittorrent.QBittorrent()
        qb.connect()
        if command == 'resume':
            qb.resume_torrent(torrent_hash)
        elif command == 'pause':
            qb.resume_torrent(torrent_hash)
    def reportStatistic(self):
        metrics = self.get_system_metrics()
        hwinfo = self.getHardwareInfo()

        current_datetime = datetime.now()

        runtime = round(time.time() - self.PROGRAM_START_TIME)
        runtime_unit = "s"
        if runtime > 60:
            runtime = runtime // 60
            runtime_unit = "min"

        if runtime > 60:
            runtime = runtime // 60
            runtime_unit = "h"

        if runtime > 24 and runtime_unit == 'h':
            runtime = runtime // 24
            runtime_unit = "d"

        report = {
            "custom_flags": self.CUSTOM_FLAGS,
            "version": self.version,
            "last_update": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "last_update_seconds": time.time(),
            "start_time": self.PROGRAM_START_TIME,
            "report_runtime": "{} {}" . format(runtime, runtime_unit),
            "system": {
                "core_count": metrics['core_count'],
                "thread_count": metrics['thread_count'],
                "system_info": hwinfo['system'],
                "cpu": hwinfo['cpu'],
                "boot_time": psutil.boot_time(),
                "unique_id": self.UNIQUE_ID,
                "last_executed_poll_command": self.LAST_EXECUTED_REMOTE_POLL_COMMAND,
                "last_executed_poll_command_time": self.LAST_EXECUTED_REMOTE_POLL_COMMAND_TIME
            },
            "current": {
                "cpu_load": metrics['cpu_load'],
                "gpu_load": metrics['gpu_load'],
                "memory_load": metrics['memory_load'],
                "virtual_memory": metrics['virtual_memory'],
                "cpu_temp": metrics['cpu_temperature'],
                "cpu_temp_alt": metrics['cpu_temp_alt'],
                "cpu_temps": metrics['cpu_temps'],
                "cpu_clocks": metrics['cpu_clocks'],
                "gpu_temp": metrics['gpu_temp'],
                "all_temps": metrics['all_temps'],
                "disks": {
                    "total_free_gb": metrics['disk_total_free_gb'],
                    "per_disk": dict()
                },
                "network": metrics['network'],
                "fans_info": metrics['fans_info'],
                "processes": metrics['processes']
            },
            "history": {
                "cpu_load_avg": self.AVG_CPU_LOAD,
                "cpu_load_max": self.MAX_CPU_LOAD,
                "cpu_charts": {
                    "60": self.CPU_LOADS_ARCH["60"],
                    "360": self.CPU_LOADS_ARCH["360"],
                    "720": self.CPU_LOADS_ARCH["720"]
                },
                "gpu_charts": {
                    "60": self.GPU_LOADS_ARCH["60"],
                    "360": self.GPU_LOADS_ARCH["360"],
                    "720": self.GPU_LOADS_ARCH["720"]
                },
                "last_max_cpu_load": {
                    "load": self.MAX_CPU_LOAD_PERC,
                    "time": self.MAX_CPU_LOAD_TIME
                },
                "network": {
                    "total_transfer": self.TOTAL_NETWORK_TRANSFER,
                    "download_peak": {
                        "rate_kbps": self.MAX_NET_DOWNLOAD,
                        "time": self.MAX_NET_DOWNLOAD_TIME
                    },
                    "upload_peak": {
                        "rate_kbps": self.MAX_NET_UPLOAD,
                        "time": self.MAX_NET_UPLOAD_TIME
                    }
                }
            },
            "logs": self.LOGS[::-1]
        }

        # update report with info from other modules
        if len(self.USE_MODULES) > 0:
            report['modules'] = dict()
        for module in self.USE_MODULES:
            if module.lower() == 'qbittorrent':
                ret = self.module_qbittorrent()
                report['modules']['qbittorrent'] = {
                    "torrents": ret['torrents']
                }

        for path, du in metrics['disk_usages'].items():
            report['current']['disks']['per_disk'][path] = du

        for api in self.API_ENDPOINTS:
            url = api['url']
            token_name = api['token_name']
            token_value = api['token_value']
            report[token_name] = token_value
            try:
                response = requests.post(url, json=report)

                if response.status_code != 200:
                    self.appendToLogs("ERROR", "Response code from {} was not OK " . format(url))
                    print("\t\t Response code from {} was not OK " . format(url))
                    print("\t\t Timestamp: ", current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                    appendErrorLog("Response code from {} was not OK " . format(url))
                else:
                    self.appendToLogs("INFO", "Report sent to {}".format(url))
                    if self.PRINT_REPORT_TIMESTAMPS:
                        print("\t\t Report sent at: {}" . format(current_datetime))
            except:
                pass

    def printStatistic(self):
        metrics = self.get_system_metrics()
        print("System Metrics:")
        print(f"CPU Count: {metrics['thread_count']} threads")
        print(f"CPU Load: {metrics['cpu_load']}%")
        print(f"Memory Load: {metrics['memory_load']}%")
        print("\n")
        print("Disks info:")
        print("Total free space [GB] {} " . format(metrics['disk_total_free_gb']))
        for path, du in metrics['disk_usages'].items():
            print("{}: {}" . format(path, du))
        print("\n")
        print("Network speed: ")
        print("\t Total download: ", metrics['network']['total_download_kBps'])
        print("\t Total upload: ", metrics['network']['total_upload_kBps'])
        print("\n")
        print(f"CPU Temperature: {metrics['cpu_temperature']}°C" if metrics['cpu_temperature'] else "N/A")
        print(f"GPU Load: {metrics['gpu_load']}%" if metrics['gpu_load'] else "N/A")
        print("\n")
        print("Last Max CPU LOAD [%]: ", self.MAX_CPU_LOAD_PERC)
        print("Last Max CPU LOAD @: ", self.MAX_CPU_LOAD_TIME)
        print("\n")
        print("Average CPU Load: ")
        for m, l in self.AVG_CPU_LOAD.items():
            print("\t Average CPU load in last {} minutes: {}%" . format(m, l))

        print("\n")
        print("Fans info: ", metrics['fans_info'])
        print("-----" * 20)

    def polling(self):
        if time.time() < self.LAST_REMOTE_CONTROL_POLL_RUNTIME:
            return

        current_datetime = datetime.now()
        whitelisted_commands = [cmd.lower() for cmd in self.REMOTE_CONTROL_POLL_COMMANDS]

        self.LAST_REMOTE_CONTROL_POLL_RUNTIME = time.time() + self.REMOTE_CONTROL_POLL_FREQUENCY

        for api in self.REMOTE_CONTROL_POLLING:
            url = api['url']
            token_name = api['token_name']
            token_value = api['token_value']
            data = {
                "unique_id": self.UNIQUE_ID,
                token_name: token_value
            }
            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    response_data = response.json()
                    if len(response_data.keys()) == 0:
                        continue
                    try:
                        command = response_data['command'] if 'command' in response_data else ''
                        if command.lower() in whitelisted_commands:

                            if command.lower() == 'resetstatistics':
                                self.resetStatistics()
                                self.appendToLogs("INFO", "Remote command {} from {} was successfully executed ".format(command, url))
                                self._print("\t\t Remote command {} from {} was successfully executed ".format(command, url))
                                requests.post(api['clear_queue_url'], json=data)

                            elif command.lower() == 'clearlog':
                                self.LOGS = []
                                self.appendToLogs("INFO", "Remote command {} from {} was successfully executed ".format(command, url))
                                self._print("\t\t Remote command {} from {} was successfully executed ".format(command, url))
                                requests.post(api['clear_queue_url'], json=data)

                            elif command.lower() == "qbittorrent":
                                subcommand = response_data['subcommand'] if 'subcommand' in response_data else ''
                                torrent_hash = response_data['torrentHash'] if 'torrentHash' in response_data else ''
                                self.remote_control_qbittorrent(subcommand, torrent_hash)
                                self.appendToLogs("INFO", "Remote command {} from {} was successfully executed ".format(command, url))
                                self._print("\t\t Remote command {} from {} was successfully executed ".format(command, url))
                                requests.post(api['clear_queue_url'], json=data)

                            self.LAST_EXECUTED_REMOTE_POLL_COMMAND = command
                            self.LAST_EXECUTED_REMOTE_POLL_COMMAND_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            self.appendToLogs("ERROR", "Remote command {} from {} is not whitelisted ".format(command, url))
                            print("\t\t Remote command {} from {} is not whitelisted ".format(command, url))
                            appendErrorLog("Remote command {} from {} is not whitelisted ".format(command, url))
                    except Exception as e:
                        self.appendToLogs("ERROR", "Remote command from {} was not executed " . format(url))
                        appendErrorLog("Remote command from {} was not executed " . format(url))
                        print("\t\t Remote command from {} was not executed " . format(url))
                        print("\t\t Error: ", e)
            except:
                pass
    def run(self):
        sleepTime = 2  # seconds
        self.about()
        print()
        print("\t Loading config....")
        self.load_config()
        print("\t Config is loaded...")
        print()
        print("\t Preparing monitoring and reporting for {} " . format(self.UNIQUE_ID))

        if len(self.USE_MODULES) > 0:
            print()
            print("\t Modules in use: {} " . format(self.USE_MODULES))
            print()

        gui_closed = lambda: False
        if self.SHOW_GUI:
            print()
            print("\t Prepare GUI")
            gui_data = {
                "version": self.version,
                "config": {
                    "unique_id": self.UNIQUE_ID,
                    "log_size": self.LOG_SIZE
                },
                "update_config_callback": self.update_config_callback
            }
            gux = GUI(gui_data)
            gui_closed = gux.get_gui_close_status
            gui_thread = threading.Thread(target=gux.run)
            gui_thread.start()
            print("\t GUI ready")

        print()

        last_check = 0
        metrics = dict()

        while True and not gui_closed():
            time_now = time.time()
            self.NET_IO_END = psutil.net_io_counters(pernic=True)
            # run analyze every RUN_CHECK_EVERY_SECONDS seconds
            if time_now > last_check:
                try:
                    if self.PRINT_TO_CONSOLE:
                        self.printStatistic()
                    metrics = self.analyze()
                except Exception as e:
                    self.appendToLogs("ERROR", "Exception during analyze: {}".format(e))
                    appendErrorLog("Exception during analyze: {} :: {}".format(e, e.args[0]))
                    print("Exception [I]: ", e)
                last_check = time_now + self.RUN_CHECK_EVERY_SECONDS - sleepTime

                if time_now > self.LAST_REPORT_SEND:
                    self.reportStatistic()
                    try:
                        self.reportStatistic()
                    except Exception as e:
                        self.appendToLogs("ERROR", "Exception during reportStatistics: {}" . format(e))
                        appendErrorLog("Exception during reportStatistics: {} :: {}".format(e, e.args[0]))
                        print("Exception [II]: ", e)
                    self.LAST_REPORT_SEND = time_now + self.REPORT_FREQUENCY * 60
                self.NET_IO_START = psutil.net_io_counters(pernic=True)

                if self.SHOW_GUI:
                    try:
                        new_data = {
                            "logs": self.LOGS,
                            "cpu_load": self.CPU_LOADS_ARCH['1'][-1],
                            "gpu_load": self.GPU_LOADS_ARCH['1'][-1],
                            "total_download_kbps": metrics['network']['total_download_kbps'],
                            "total_upload_kbps": metrics['network']['total_upload_kbps'],
                            "downlink_load": metrics['network']['download_usage_perc'],
                            "uplink_load": metrics['network']['upload_usage_perc'],
                            "storage": {
                                "disk_usages": metrics['disk_usages'],
                                "disk_total_free_gb": metrics['disk_total_free_gb']
                            }
                        }
                        gux.update_gui(new_data)
                        print("\t Sent new sensor data to GUI")
                    except Exception as e:
                        self.appendToLogs("ERROR", "Exception during GUI render: {}".format(e))
                        appendErrorLog("Exception during GUI render: {} :: {}".format(e, e.args))
                        print("\t Exception [III]: ", e)

            if len(self.REMOTE_CONTROL_POLLING) > 0:
                self.polling()

            time.sleep(sleepTime)
            # Check if 'Q' has been pressed to exit
            if keyboard.is_pressed("q"):
                print("\t Exiting monitoring...")
                break

            if gui_closed():
                print("\t GUI closed. Program is closing...")
                print("\t GUI window close status: ", gux.gui_closed)
                print("\t Joining GUI Thread")
                gui_thread.join()
                print("\t GUI Thread merged with the main thread")
                break

        print()
        print("\t Exiting...")
        sys.exit()

if __name__ == "__main__":
    hwrp = HwInfoReport()
    hwrp.run()

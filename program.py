import platform
import time
from datetime import datetime
from json import load as jsload

import GPUtil
import WinTmp
import psutil
import requests
import keyboard

class HwInfoReport:
    def about(self):
        print("\n\n")
        print("\t Hardware monitoring and reporting system by Sandi")
        print("\t Version: {}" . format(self.version))
        print("\n\n")
        print("\t To exit the program, hold 'Q', or you know... the good old CTRL+C")
        print("\n")

    def _print(self, arg, *args):
        if self.PRINT_TO_CONSOLE:
            print(arg, *args)

    def __init__(self):
        self.version = "1.1"
        self.AVG_CPU_LOAD = {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        }

        # CPU LOAD ARCHIVE
        self.CPU_LOADS_ARCH = {
            "1": [],
            "5": [],
            "15": [],
            "30": [],
            "60": []
        }

        self.PROGRAM_START_TIME = time.time()

        self.LAST_PERIOD_1 = self.PROGRAM_START_TIME + 60
        self.LAST_PERIOD_5 = self.PROGRAM_START_TIME + 5 * 60
        self.LAST_PERIOD_15 = self.PROGRAM_START_TIME + 15 * 60
        self.LAST_PERIOD_30 = self.PROGRAM_START_TIME + 30 * 60
        self.LAST_PERIOD_60 = self.PROGRAM_START_TIME + 60 * 60

        self.MAX_CPU_LOAD_PERC = 0
        self.MAX_CPU_LOAD_TIME = ""

        self.MAX_NET_DOWNLOAD = 0
        self.MAX_NET_DOWNLOAD_TIME = ""
        self.MAX_NET_UPLOAD = 0
        self.MAX_NET_UPLOAD_TIME = ""

        self.DISK_USAGE_PATHS = ["C:\\"]

        self.API_ENDPOINT = ""
        self.API_TOKEN_NAME = ""
        self.API_TOKEN_VALUE = ""
        self.REPORT_FREQUENCY = 99

        self.LAST_REPORT_SEND = 0

        self.RUN_CHECK_EVERY_SECONDS = 30

        self.NET_IO_START = dict()
        self.NET_IO_END = dict()
        self.TOTAL_NETWORK_TRANSFER = {
            "download": 0,
            "upload": 0,
            "download_unit": "B",
            "upload_unit": "B"
        }

        self.PRINT_TO_CONSOLE = True
        self.PRINT_REPORT_TIMESTAMPS = True

    def load_config(self):
        with open("config.json", "r") as file:
            config = jsload(file)
            self.API_ENDPOINT = config['api_endpoint']
            self.API_TOKEN_NAME = config['api_token_name']
            self.API_TOKEN_VALUE = config['api_token_value']
            self.REPORT_FREQUENCY = config['send_report_every_mins']
            self.DISK_USAGE_PATHS = config['disk_usage_paths']
            self.RUN_CHECK_EVERY_SECONDS = config['run_check_every_seconds']
            self.PRINT_TO_CONSOLE = config['print_to_console']
            self.PRINT_REPORT_TIMESTAMPS = config['print_report_timestamps']

        print("\t\t Run analyze every {} second(s)" . format(self.RUN_CHECK_EVERY_SECONDS))
        print("\t\t Output to console is set to: ", self.PRINT_TO_CONSOLE)
        print("\t\t Report to {} every {} minute(s) " . format(self.API_ENDPOINT, self.REPORT_FREQUENCY))

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

        stats = {
            "total_upload_kBps": total_upload_kBps,
            "total_download_kBps": total_download_kBps,
            "total_upload_kbps": total_upload_kBps * 8,
            "total_download_kbps": total_download_kBps * 8,
            "per_nic": stats
        }
        return stats

    def get_system_metrics(self):
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

        return {
            "cpu_count": cpu_count,
            "cpu_load": cpu_load,
            "memory_load": memory_load,
            "cpu_temperature": cpu_temp,
            "cpu_temp_alt": WinTmp.CPU_Temp(),
            "gpu_temp": WinTmp.GPU_Temp(),
            "gpu_load": gpu_load,
            "disk_usages": disk_usages,
            "disk_total_free_gb": disk_total_free_gb,
            "network": network,
            "fans_info": fans_info
        }

    def analyze(self):
        time_now = time.time()
        metrics = self.get_system_metrics()

        cpu_count = metrics['cpu_count']
        cpu_load = metrics['cpu_load']

        if cpu_load >= self.MAX_CPU_LOAD_PERC:
            current_datetime = datetime.now()
            self.MAX_CPU_LOAD_PERC = cpu_load
            self.MAX_CPU_LOAD_TIME = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if time_now > self.LAST_PERIOD_1:
            self.LAST_PERIOD_1 = time_now + 60
            self.AVG_CPU_LOAD["1"] = self.getCpuAvg(self.CPU_LOADS_ARCH["1"])
            self.CPU_LOADS_ARCH["1"] = []

        if time_now > self.LAST_PERIOD_5:
            self.LAST_PERIOD_5 = time_now + 5*60
            self.AVG_CPU_LOAD["5"] = self.getCpuAvg(self.CPU_LOADS_ARCH["5"])
            self.CPU_LOADS_ARCH["5"] = []

        if time_now > self.LAST_PERIOD_15:
            self.LAST_PERIOD_15 = time_now + 15*60
            self.AVG_CPU_LOAD["15"] = self.getCpuAvg(self.CPU_LOADS_ARCH["15"])
            self.CPU_LOADS_ARCH["15"] = []

        if time_now > self.LAST_PERIOD_30:
            self.LAST_PERIOD_30 = time_now + 30*60
            self.AVG_CPU_LOAD["30"] = self.getCpuAvg(self.CPU_LOADS_ARCH["30"])
            self.CPU_LOADS_ARCH["30"] = []

        if time_now > self.LAST_PERIOD_60:
            self.LAST_PERIOD_60 = time_now + 60*60
            self.AVG_CPU_LOAD["60"] = self.getCpuAvg(self.CPU_LOADS_ARCH["60"])
            self.CPU_LOADS_ARCH["60"] = []

        self.CPU_LOADS_ARCH["1"].append(cpu_load)
        self.CPU_LOADS_ARCH["5"].append(cpu_load)
        self.CPU_LOADS_ARCH["15"].append(cpu_load)
        self.CPU_LOADS_ARCH["30"].append(cpu_load)
        self.CPU_LOADS_ARCH["60"].append(cpu_load)

    def reportStatistic(self):
        time_now = time.time()

        if time_now < self.LAST_REPORT_SEND:
            return

        self.LAST_REPORT_SEND = time_now + self.REPORT_FREQUENCY * 60

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
            self.API_TOKEN_NAME: self.API_TOKEN_VALUE,
            "version": self.version,
            "last_update": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "report_runtime": "{} {}" . format(runtime, runtime_unit),
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
                "disks": {
                    "total_free_gb": metrics['disk_total_free_gb'],
                    "per_disk": dict()
                },
                "network": metrics['network'],
                "fans_info": metrics['fans_info']
            },
            "history": {
                "cpu_load_avg": self.AVG_CPU_LOAD,
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
            }
        }

        for path, du in metrics['disk_usages'].items():
            report['current']['disks']['per_disk'][path] = du


        response = requests.post(self.API_ENDPOINT, json=report)
        if response.status_code != 200:
            print("Response code not OK")
        else:
            if self.PRINT_REPORT_TIMESTAMPS:
                print("Report sent at: {}" . format(current_datetime))

    def printStatistic(self):
        metrics = self.get_system_metrics()
        self._print("System Metrics:")
        self._print(f"CPU Count: {metrics['cpu_count']} threads")
        self._print(f"CPU Load: {metrics['cpu_load']}%")
        self._print(f"Memory Load: {metrics['memory_load']}%")
        self._print("\n")
        self._print("Disks info:")
        self._print("Total free space [GB] {} " . format(metrics['disk_total_free_gb']))
        for path, du in metrics['disk_usages'].items():
            self._print("{}: {}" . format(path, du))
        self._print("\n")
        self._print("Network speed: ")
        self._print("\t Total download: ", metrics['network']['total_download_kBps'])
        self._print("\t Total upload: ", metrics['network']['total_upload_kBps'])
        self._print("\n")
        self._print(f"CPU Temperature: {metrics['cpu_temperature']}°C" if metrics['cpu_temperature'] else "N/A")
        self._print(f"GPU Load: {metrics['gpu_load']}%" if metrics['gpu_load'] else "N/A")
        self._print("\n")
        self._print("Last Max CPU LOAD [%]: ", self.MAX_CPU_LOAD_PERC)
        self._print("Last Max CPU LOAD @: ", self.MAX_CPU_LOAD_TIME)
        self._print("\n")
        self._print("Average CPU Load: ")
        for m, l in self.AVG_CPU_LOAD.items():
            self._print("\t Average CPU load in last {} minutes: {}%" . format(m, l))

        self._print("\n")
        self._print("Fans info: ", metrics['fans_info'])
        self._print("-----" * 20)

    def run(self):
        self.about()
        print()
        print("\t Loading config....")
        self.load_config()
        print("\t Config is loaded...")

        print()
        hwinfo = self.getHardwareInfo()
        print("\t CPU: ", hwinfo['cpu'])
        print("\t System: ", hwinfo['system'])

        last_check = 0
        while True:
            time_now = time.time()
            self.NET_IO_END = psutil.net_io_counters(pernic=True)
            # run analyze every RUN_CHECK_EVERY_SECONDS seconds
            if time_now > last_check:
                self.printStatistic()
                self.analyze()
                last_check = time_now + self.RUN_CHECK_EVERY_SECONDS
                self.reportStatistic()
                self.NET_IO_START = psutil.net_io_counters(pernic=True)

            time.sleep(2)
            # Check if 'Q' has been pressed to exit
            if keyboard.is_pressed("q"):
                print("Exiting monitoring...")
                break

if __name__ == "__main__":
    hwrp = HwInfoReport()
    hwrp.run()
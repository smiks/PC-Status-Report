# PC-Status-Report v1.1

A simple Python program that gathers your system's info and sends it to the endpoint you define in config.json.
It can be used as a remote monitoring of your PC.

It tries to read the CPU temperature in 2 different ways. If it gets the temperature it will report it,
otherwise it will show None.

Network speed is calculated using net_io_counters. 

#

Requirements:
- pythonnet
- GPUtil
- WinTmp
- psutil
- requests
- platform

#

Report sample:
```
{
    "token": "hiddenSomething",
    "version": "1.1",
    "last_update": "2024-10-27 15:26:53",
    "report_runtime": "1min",
    "system": {
        "cpu_count": 16,
        "system_info": "Windows",
        "cpu": "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel"
    },
    "current": {
        "cpu_load": 9.4,
        "gpu_load": 7.000000000000001,
        "memory_load": 48.3,
        "cpu_temp": null,
        "cpu_temp_alt": null,
        "gpu_temp": 51,
        "disks": {
            "total_free_gb": 174,
            "per_disk": {
                "C:\\": {
                    "free_gb": 41,
                    "free_perc": 91
                },
                "R:\\": {
                    "free_gb": 133,
                    "free_perc": 86
                }
            }
        },
        "network": {
            "total_upload_kBps": 2,
            "total_download_kBps": 32,
            "total_upload_kbps": 16,
            "total_download_kbps": 256,
            "per_nic": {
                "Ethernet": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Ethernet 2": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Ethernet 3": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Ethernet 4": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "OpenVPN Data Channel Offload for NordVPN": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection 2": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection* 1": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection* 10": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Wi-Fi": {
                    "upload_speed_kBps": 2,
                    "download_speed_kBps": 32
                },
                "Bluetooth Network Connection": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Loopback Pseudo-Interface 1": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "vEthernet (WSLCore)": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                }
            }
        },
        "fans_info": null
    },
    "history": {
        "cpu_load_avg": {
            "1": 8,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "last_max_cpu_load": {
            "load": 11.1,
            "time": "2024-10-27 15:25:49"
        },
        "network": {
            "total_transfer": {
                "download": 2,
                "upload": 102,
                "download_unit": "GB",
                "upload_unit": "MB"
            },
            "download_peak": {
                "rate_kbps": 360,
                "time": "2024-10-27 15:26:30"
            },
            "upload_peak": {
                "rate_kbps": 88,
                "time": "2024-10-27 15:26:30"
            }
        }
    }
}
```


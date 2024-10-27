# PC-Status-Report v1.2

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
- keyboard

#

Report sample:
```
{
    "token": "hiddenSomething",
    "version": "1.2",
    "last_update": "2024-10-27 22:10:51",
    "report_runtime": "4 min",
    "system": {
        "cpu_count": 16,
        "system_info": "Windows",
        "cpu": "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel"
    },
    "current": {
        "cpu_load": 10,
        "gpu_load": 1,
        "memory_load": 47.1,
        "cpu_temp": null,
        "cpu_temp_alt": null,
        "gpu_temp": 49,
        "disks": {
            "total_free_gb": 172,
            "per_disk": {
                "C:\\": {
                    "free_gb": 39,
                    "free_perc": 92
                },
                "R:\\": {
                    "free_gb": 133,
                    "free_perc": 86
                }
            }
        },
        "network": {
            "total_download_kBps": 104,
            "total_upload_kBps": 6,
            "total_download_kbps": 832,
            "total_upload_kbps": 48,
            "download_usage_perc": 0,
            "upload_usage_perc": 0,
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
                    "upload_speed_kBps": 6,
                    "download_speed_kBps": 104
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
            "1": 9,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "last_max_cpu_load": {
            "load": 20.7,
            "time": "2024-10-27 22:10:50"
        },
        "network": {
            "total_transfer": {
                "download": 10,
                "upload": 284,
                "download_unit": "GB",
                "upload_unit": "MB"
            },
            "download_peak": {
                "rate_kbps": 4872,
                "time": "2024-10-27 22:06:58"
            },
            "upload_peak": {
                "rate_kbps": 168,
                "time": "2024-10-27 22:08:32"
            }
        }
    }
}
```


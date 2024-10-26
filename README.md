# PC-Status-Report v1.0

A simple Python program that gathers your system's info and sends it to the endpoint you define in config.json.
It can be used as a remote monitoring of your PC.

It tries to read the CPU temperature in 2 different ways. If it gets the temperature it will report it,
otherwise it will show None.

Network speed is calculated using net_io_counters.

Report sample:
```
{
    "token": "hiddenSomething",
    "system": {
        "cpu_count": 16,
        "system_info": "Windows",
        "cpu": "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel"
    },
    "current": {
        "cpu_load": 8.7,
        "gpu_load": 0,
        "memory_load": 46.6,
        "cpu_temp": null,
        "cpu_temp_alt": null,
        "gpu_temp": 48,
        "disks": {
            "C:\\": {
                "free_gb": 42,
                "free_perc": 91
            },
            "R:\\": {
                "free_gb": 133,
                "free_perc": 86
            }
        },
        "network": {
            "total_upload_kBps": 7,
            "total_download_kBps": 12,
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
                    "upload_speed_kBps": 7,
                    "download_speed_kBps": 12
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
        }
    },
    "history": {
        "cpu_load_avg": {
            "1": 7,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "last_max_cpu_load": {
            "load": 11.1,
            "time": "2024-10-26 14:49:00"
        },
        "network": {
            "total_transfer": {
                "download": 220,
                "upload": 9,
                "download_unit": "KB",
                "upload_unit": "MB"
            }
        }
    }
}
```

Requirements:
- pythonnet
- GPUtil
- WinTmp
- psutil
- requests
- platform


# PC-Status-Report v1.5

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
    "version": "1.6",
    "last_update": "2024-10-28 17:47:18",
    "last_update_seconds": 1730134038.587204,
    "start_time": 1730134031.564783,
    "report_runtime": "7 s",
    "system": {
        "core_count": 8,
        "thread_count": 16,
        "system_info": "Windows",
        "cpu": "Intel64 Family 6 Model 158 Stepping 13, GenuineIntel",
        "boot_time": 1728224602.587204
    },
    "current": {
        "cpu_load": 3.1,
        "gpu_load": 0,
        "memory_load": 84.6,
        "virtual_memory": {
            "available": 35596468224,
            "percent": 48.1
        },
        "cpu_temp": null,
        "cpu_temp_alt": 79,
        "cpu_temps": [
            55,
            56,
            59,
            59,
            59,
            59,
            60,
            60,
            60,
            60,
            60,
            45,
            44,
            41,
            41,
            41,
            41,
            40,
            40,
            40,
            40,
            60,
            58.70000076293945
        ],
        "cpu_clocks": {
            "current": 3600,
            "max": 3600
        },
        "gpu_temp": 60,
        "all_temps": {
            "Cpu_Temperature": [
                54,
                57,
                59,
                59,
                59,
                59,
                59,
                59,
                59,
                59,
                60,
                46,
                43,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                59,
                58.29999923706055
            ],
            "GpuNvidia_Temperature": [
                60,
                66.1875,
                64
            ],
            "Storage_Temperature": [
                38,
                33,
                41
            ]
        },
        "disks": {
            "total_free_gb": 753,
            "per_disk": {
                "C:\\": {
                    "free_gb": 753,
                    "free_perc": 21
                }
            }
        },
        "network": {
            "total_download_kBps": 1,
            "total_upload_kBps": 1,
            "total_download_kbps": 8,
            "total_upload_kbps": 8,
            "download_usage_perc": 0,
            "upload_usage_perc": 0,
            "per_nic": {
                "Ethernet 3": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "vEthernet (WSL (Hyper-V firewall))": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection* 1": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Local Area Connection* 2": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "WiFi": {
                    "upload_speed_kBps": 1,
                    "download_speed_kBps": 1
                },
                "Ethernet 2": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Bluetooth Network Connection": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Ethernet": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                },
                "Loopback Pseudo-Interface 1": {
                    "upload_speed_kBps": 0,
                    "download_speed_kBps": 0
                }
            }
        },
        "fans_info": null,
        "processes": [
            "[process name].exe": {
                "cpu": [cpu load] %,
                "ram": [ram load] B,
                "name": [process name]
            }...
        ]
    },
    "history": {
        "cpu_load_avg": {
            "1": 4,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "cpu_load_max": {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },        
        "last_max_cpu_load": {
            "load": 5.6,
            "time": "2024-10-28 14:11:19"
        },
        "network": {
            "total_transfer": {
                "download": 24,
                "upload": 4,
                "download_unit": "GB",
                "upload_unit": "GB"
            },
            "download_peak": {
                "rate_kbps": 16,
                "time": "2024-10-28 14:11:23"
            },
            "upload_peak": {
                "rate_kbps": 8,
                "time": "2024-10-28 14:11:23"
            }
        }
    }
}
```


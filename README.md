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
        "cpu_load": 6.6,
        "gpu_load": 0,
        "memory_load": 48.7,
        "cpu_temp": null,
        "cpu_temp_alt": null,
        "gpu_temp": 51,
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
            "upload_kbps": 4,
            "download_kbps": 51
        }
    },
    "history": {
        "cpu_load_avg": {
            "1": 13.345454545454544,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "last_max_cpu_load": {
            "load": 25.5,
            "time": "2024-10-26 13:59:00"
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


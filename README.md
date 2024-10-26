# PC-Status-Report v1.0

A simple Python program that gathers your system's info and sends it to the endpoint you define in config.json.
It can be used as a remote monitoring of your PC.

It tries to read the CPU temperature in 2 different ways. If it gets the temperature it will report it,
otherwise it will show None.

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
        "cpu_load": 12.3,
        "gpu_load": 7.000000000000001,
        "memory_load": 47,
        "cpu_temp": null,
        "cpu_temp_alt": null,
        "gpu_temp": 49,
        "disk": {
            "usage_free_gb": 42,
            "usage_perc": 91
        }
    },
    "history": {
        "cpu_load_avg": {
            "1": 0,
            "5": 0,
            "15": 0,
            "30": 0,
            "60": 0
        },
        "last_max_cpu_load": {
            "load": 22.6,
            "time": "2024-10-26 13:25:54"
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


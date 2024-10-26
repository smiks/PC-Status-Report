# PC-Status-Report

A simple Python program that gathers your system's info and sends it to the endpoint you define in config.json.
It can be used as a remote monitoring of your PC.

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
        "gpu_load": 1,
        "memory_load": 47.7,
        "cpu_temp": null,
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
            "load": 5.2,
            "time": "2024-10-26 12:57:27"
        }
    }
}
```

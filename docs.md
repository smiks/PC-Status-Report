### program configuration

```commandline
{
    // LIST OF ENDPOINT APIs
    "api_endpoints": [
        {
            "url": URL TO YOUR ENDPOINT THAT ACCEPTS REPORT JSON,
            
            // TOKEN NAME AND VALUE (send with every request to the URL)
            "token_name": "token",
            "token_value": "hiddenSomething"
        }
    ],
    
    // LIST OF URLs FROM WHICH THIS PROGRAM PULLS COMMANDS AND EXECUTES THEM
    "remote_control_polling": [
        {
            // URL TO GET THE COMMAND FROM
            // URL MUST RETURN JSON IN FORMAT {"command": "some command"}
            "url": "",
            "clear_queue_url": URL TO CALL AFTER COMMAND IS EXECUTED,
            "token_name": "token",
            "token_value": "hiddenSomething"
        }
    ],
    
    // POLLING INTERVAL (every X seconds)
    "remote_control_poll_every_seconds": X,
    
    // WHITELISTED POLLING COMMANDS - only those can be executed
    // AVAILABLE COMMANDS: "resetStatistics", "clearLog"
    "remote_control_poll_commands":  []
    
    "unique_id": ID OF YOUR COMPUTER,
    "send_report_every_mins": 1,
    "run_check_every_seconds": 5,
    
    // LIST OF DIRECTORIES YOU WANT TO TRACK
    "disk_usage_paths": [
        "C:\\",
        "R:\\"
    ],
    
    // IF YOU WANT TO PRINT STATISTICS TO  THE CONSOLE
    "print_to_console": false,
    
    // IF YOU WANT TO PRINT TIMESTAMPS WHEN REPORT IS SENT
    "print_report_timestamps": true,
    
    // WHAT IS YOUR ISP BANDWIDTH
    "max_net_downlink_kbps": 1000000,
    "max_net_uplink_kbps": 200000,
    
    // IF YOU WANT TO TRACK PROCESSES AND REPORT THEM
    "include_process_monitoring": false,
    
    // IF YOU WANT TO SHOW GUI
    "show_gui": true,
    
    // MAX LOG SIZE
    "log_size": 50,
    
    // LIST OF WHAT ADDITIONAL MODULES YOU WANT TO USE
    // AVAILABLE: "qbittorent"
    "use_modules": [],
    
    // CUSTOM FLAGS YOU WANT TO SET, SENT WITH EVERY REQUEST TO THE ENDPOINT
    // WHEN SENDING REPORT
    "customFlags": {
        "showServices": false
    }
}
```
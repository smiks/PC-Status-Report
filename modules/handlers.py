from datetime import datetime
def writeLog(file_path, text):
    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    text = "[{}] :: {}\n" . format(timestamp, text)
    with open(file_path, 'a') as file:  # 'a' mode opens the file for appending
        file.write(text)

def appendErrorLog(text):
    writeLog('./error_log', text)
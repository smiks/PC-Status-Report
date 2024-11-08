import sys

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def gb2tb(gb):
    if gb > 1024:
        return "{} TB" . format(gb // 1024)
    return "{} GB" . format(gb)

def freeSpace2Total(free, perc):
    invert = 1 - (perc/100)
    return free//invert
class GUI():

    def __init__(self, data):
        self.program_version = data['version']
        self.config_data = data['config']
        self.update_config_callback = data['update_config_callback']
        self.gui_closed = False
        self.labels = dict()
        self.canvases = dict()
        self.frames = dict()
        self.tabs = []

    def on_button_click(self):
        messagebox.showinfo("Hello", "Welcome to your first GUI window!")

    def get_gui_close_status(self):
        return self.gui_closed
    def on_window_close(self):
        print("GUI:: closing window")
        self.gui_closed = True
        sys.exit()

    def clean_labels(self, where):
        for widget in where.winfo_children():
            widget.destroy()
    def on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def update_gui(self, data):
        new_text = "CPU LOAD: {}%".format(data['cpu_load'])
        self.labels['cpu_load'].config(text=new_text)

        new_text = "GPU LOAD: {}%".format(data['gpu_load'])
        self.labels['gpu_load'].config(text=new_text)

        download_speed = data['total_download_kbps']
        download_unit = "kb/s"
        if download_speed > 1024:
            download_speed //= 1024
            download_unit = "Mb/s"

        new_text = "DOWNLINK LOAD: {}{} ({}%)".format(download_speed, download_unit, data['downlink_load'])
        self.labels['downlink_load'].config(text=new_text)

        upload_speed = data['total_upload_kbps']
        upload_unit = "kb/s"
        if upload_speed > 1024:
            upload_speed //= 1024
            upload_unit = "Mb/s"

        new_text = "UPLINK LOAD: {}{} ({}%)".format(upload_speed, upload_unit, data['uplink_load'])
        self.labels['uplink_load'].config(text=new_text)

        self.clean_labels(self.frames['log'])
        logs = data['logs']
        logs = logs[::-1]
        txt = ""
        for log in logs:
            txt += "[{}] :: {} :: {}\n" . format(log['timestamp'], log['type'], log['content'])

        tk.Label(self.frames['log'], text=txt, anchor="nw").pack(fill="x", padx=5, pady=5)


        storage = data['storage']
        perdisk = dict()
        total_disk = 0
        for path, du in storage['disk_usages'].items():
            perdisk[path] = du
        for path, info in perdisk.items():
            tmp = freeSpace2Total(info['free_gb'], info['free_perc'])
            total_disk += tmp

        total_used = total_disk - storage['disk_total_free_gb']
        txt = "Total disk usage: {} / {} \t \n".format(gb2tb(total_used), gb2tb(total_disk))
        txt += "Total free space: {} \t \t  \n" . format(gb2tb(storage['disk_total_free_gb']))
        txt += "\n"
        for path, info in perdisk.items():
            total = freeSpace2Total(info['free_gb'], info['free_perc'])
            used = total - info['free_gb']
            txt += "{}\t {} / {} ({}%) \n" . format(path, gb2tb(used), gb2tb(total), info['free_perc'])

        self.labels['storage'].config(text=txt)

        #print("GUI:: updating GUI with data: ", data)

    def sensor_tab(self):
        # Create a label widget
        self.labels['title'] = tk.Label(self.tabs[0], text="Sensor Data", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[1], text="Storage", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[2], text="Service Logs", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[3], text="Configuration", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[4], text="About", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['proc_load_header'] = tk.Label(self.tabs[0], text="PROCESSING LOAD ", font=("Arial", 12, "bold"))
        self.labels['proc_load_header'].pack(anchor="w", padx=10, pady=10)

        self.labels['cpu_load'] = tk.Label(self.tabs[0], text="CPU LOAD: ", font=("Arial", 10))
        self.labels['cpu_load'].pack(anchor="w", padx=10, pady=5)

        self.labels['gpu_load'] = tk.Label(self.tabs[0], text="GPU LOAD: ", font=("Arial", 10))
        self.labels['gpu_load'].pack(anchor="w", padx=10, pady=5)

        self.labels['network_load_header'] = tk.Label(self.tabs[0], text="NETWORK LOAD ", font=("Arial", 12, "bold"))
        self.labels['network_load_header'].pack(anchor="w", padx=10, pady=10)

        self.labels['downlink_load'] = tk.Label(self.tabs[0], text="DOWNLINK LOAD: ", font=("Arial", 10))
        self.labels['downlink_load'].pack(anchor="w", padx=10, pady=5)

        self.labels['uplink_load'] = tk.Label(self.tabs[0], text="UPLINK LOAD: ", font=("Arial", 10))
        self.labels['uplink_load'].pack(anchor="w", padx=10, pady=5)

    def storage_tab(self):
        self.labels['storage'] = tk.Label(self.tabs[1], text="", font=("Arial", 10))
        self.labels['storage'].pack(anchor="nw", padx=10, pady=5)

    def log_tab(self):
        self.canvases['log'] = tk.Canvas(self.tabs[2])
        scrollbar = tk.Scrollbar(self.tabs[2], orient="vertical", command=self.canvases['log'].yview)
        self.frames['log'] = tk.Frame(self.canvases['log'])

        # Configure the canvas to use the scrollbar
        self.frames['log'].bind(
            "<Configure>",
            lambda e: self.canvases['log'].configure(scrollregion=self.canvases['log'].bbox("all"))
        )

        self.canvases['log'].create_window((0, 0), window=self.frames['log'], anchor="nw")
        self.canvases['log'].configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar into the window
        self.canvases['log'].pack(side="left", fill="both", expand=True, pady=0, padx=10)
        scrollbar.pack(side="right", fill="y")

        self.canvases['log'].bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, self.canvases['log']))

    def config_tab(self):
        def on_edit(event, entry, config, type_="string"):
            user_input = entry.get()

            if type_ == "int" and len(user_input) > 0:
                user_input = int(user_input)
            elif type_ == "float" and len(user_input) > 0:
                user_input = float(user_input)

            self.update_config_callback(config, user_input)

        def validate_numeric_input(char):
            return char.isdigit()  # Only allow digits

        def validate_alphanumeric_input(char):
            return char.isalnum()  # Allow letters and digits only

        entries = dict()

        self.labels['unique_id'] = tk.Label(self.tabs[3], text="Your PC Name:", anchor="nw")
        self.labels['unique_id'].pack(side="left", padx=10, pady=10)

        # Create and place the input field (Entry widget)
        vcmd = (self.tabs[3].register(validate_alphanumeric_input), '%S')
        entries['unique_id'] = tk.Entry(self.tabs[3], validate='key', validatecommand=vcmd, width=30)
        entries['unique_id'].pack(side="left", padx=10, pady=10)

        if self.config_data and "unique_id" in self.config_data:
            entries['unique_id'].insert(0, self.config_data['unique_id'])
            entries['unique_id'].bind("<KeyRelease>", lambda event: on_edit(event, entries['unique_id'], "UNIQUE_ID"))

        self.labels['log_size'] = tk.Label(self.tabs[3], text="Log size:", anchor="nw")
        self.labels['log_size'].pack(side="left", padx=10, pady=10)

        # Create and place the input field (Entry widget)
        vcmd = (self.tabs[3].register(validate_numeric_input), '%S')
        entries['log_size'] = tk.Entry(self.tabs[3], validate='key', validatecommand=vcmd, width=30)
        entries['log_size'].pack(side="left", padx=10, pady=10)

        if self.config_data and "log_size" in self.config_data:
            entries['log_size'].insert(0, self.config_data['log_size'])
            entries['log_size'].bind("<KeyRelease>", lambda event: on_edit(event, entries['log_size'], "LOG_SIZE", "int"))


    def about_tab(self):
        github_link = "https://github.com/smiks"
        self.labels['about'] = tk.Label(self.tabs[4], text="This service was made by Sandi \n Github: {} \n\n Version: {}" . format(github_link, self.program_version), font=("Arial", 10))
        self.labels['about'].pack(anchor="w", padx=10, pady=5)
    def run(self):
        if self.gui_closed:
            return
        # Create the main window
        window = tk.Tk()
        window.title("Sensor Data v{}" . format(self.program_version))
        window.geometry("960x480")  # Set window size

        # Create a Notebook widget (tab manager)
        tab_control = ttk.Notebook(window)

        # Create the first tab
        tab = ttk.Frame(tab_control)
        self.tabs.append(tab)
        tab_control.add(self.tabs[0], text="Sensors")

        tab = ttk.Frame(tab_control)
        self.tabs.append(tab)
        tab_control.add(self.tabs[1], text="Storage")

        tab = ttk.Frame(tab_control)
        self.tabs.append(tab)
        tab_control.add(self.tabs[2], text="Logs")

        tab = ttk.Frame(tab_control)
        self.tabs.append(tab)
        tab_control.add(self.tabs[3], text="Config")


        tab = ttk.Frame(tab_control)
        self.tabs.append(tab)
        tab_control.add(self.tabs[4], text="About")

        # Pack the Notebook widget to make it visible
        tab_control.pack(expand=1, fill="both")

        self.sensor_tab()
        self.storage_tab()
        self.log_tab()
        self.config_tab()
        self.about_tab()

        # prepare on-close hook
        window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        # Run the application
        window.mainloop()

if __name__ == "__main__":
    data = {
        "version": "demo",
        "config": {
            "unique_id": "#####"
        },
        "update_config_callback": lambda x: x
    }
    gx = GUI(data)
    gx.run()
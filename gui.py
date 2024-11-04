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
        txt = ""
        for log in logs:
            txt += "[{}] :: {} :: {}\n" . format(log['timestamp'], log['type'], log['content'])

        tk.Label(self.frames['log'], text=txt, anchor="w").pack(fill="x", padx=5, pady=5)


        storage = data['storage']
        perdisk = dict()
        totalDisk = 0
        for path, du in storage['disk_usages'].items():
            perdisk[path] = du
        for path, info in perdisk.items():
            tmp = freeSpace2Total(info['free_gb'], info['free_perc'])
            totalDisk += tmp

        txt = "Total free space: {} / {}\n".format(gb2tb(storage['disk_total_free_gb']), gb2tb(totalDisk))
        txt += "\n"
        for path, info in perdisk.items():
            total = freeSpace2Total(info['free_gb'], info['free_perc'])
            used = total - info['free_gb']
            txt += "{} :: {} / {} ({}%) \n" . format(path, gb2tb(used), gb2tb(total), info['free_perc'])

        self.labels['storage'].config(text=txt)

        #print("GUI:: updating GUI with data: ", data)

    def run(self):
        if self.gui_closed:
            return
        # Create the main window
        window = tk.Tk()
        window.title("Sensor Data v{}" . format(self.program_version))
        window.geometry("640x480")  # Set window size

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
        tab_control.add(self.tabs[3], text="About")


        # Pack the Notebook widget to make it visible
        tab_control.pack(expand=1, fill="both")

        # Create a label widget
        self.labels['title'] = tk.Label(self.tabs[0], text="Sensor Data", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[1], text="Storage", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[2], text="Service Logs", font=("Arial", 16, "bold"))
        self.labels['title'].pack(pady=5)

        self.labels['title'] = tk.Label(self.tabs[3], text="About", font=("Arial", 16, "bold"))
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


        self.labels['storage'] = tk.Label(self.tabs[1], text="", font=("Arial", 10))
        self.labels['storage'].pack(anchor="w", padx=10, pady=5)

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

        github_link = "https://github.com/smiks"
        self.labels['about'] = tk.Label(self.tabs[3], text="This service was made by Sandi \n Github: {} \n\n Version: {}" . format(github_link, self.program_version), font=("Arial", 10))
        self.labels['about'].pack(anchor="w", padx=10, pady=5)

        # prepare on-close hook
        window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        # Run the application
        window.mainloop()

if __name__ == "__main__":
    data = {
        "version": "demo"
    }
    gx = GUI(data)
    gx.run()
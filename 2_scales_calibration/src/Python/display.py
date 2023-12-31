import tkinter as tk
from tkinter import ttk
import serial
from scales_handler import ScalesHandler

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
INTERVAL = 20
SCALES_VALUES_SEPARATOR = "  "

class Display:
    def __init__(self, window):
        self.window = window
        self.current_display_tab = ttk.Frame(window)        
        self.interval = INTERVAL

        self.serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE)

        self.scales_handler = ScalesHandler(self.current_display_tab, self, self.serial_port)

        # Bind the cleanup method to the window close event
        window.protocol("WM_DELETE_WINDOW", self.cleanup)


        self.create_widgets()
        self.process_display()
    
    def cleanup(self):
        # This method is called when the window is closed
        if self.serial_port:
            self.serial_port.close()
        self.window.destroy()  # Close the GUI window

    def create_widgets(self):
        self.create_current_display_tab()
        self.create_settings_section()

    def create_current_display_tab(self):
        self.current_display_tab.pack(fill="both", expand=True)
        self.scales_handler.handle_scale_frames()  

        print("Children of current_display_tab:")
        for child in self.current_display_tab.winfo_children():
            print(child)
    
    def process_display(self):
        for scale in self.scales_handler.scales:
            if scale.is_displaying.get():
                values = self.read_serial_values()                
                self.scales_handler.handle_display_values(values)

        self.window.after(self.interval, self.process_display)

    def create_settings_section(self):
       
        settings_frame = ttk.Frame(self.current_display_tab)
        settings_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        settings_label = tk.Label(settings_frame, text="Settings", font=("Arial", 12))
        settings_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)


         # FRAME TIME INTERVAL
        time_interval_label = tk.Label(settings_frame, text="Time Interval (ms):")
        time_interval_label.grid(row=1, column=0, padx=5, pady=5)

        self.time_interval_entry = tk.Entry(settings_frame, width=10)
        self.time_interval_entry.insert(tk.END, self.interval)
        self.time_interval_entry.grid(row=1, column=1, padx=5, pady=5)

        update_button = tk.Button(settings_frame, text="Update", command=self.update_time_interval)
        update_button.grid(row=1, column=2, padx=5, pady=5)

        # FRAME CALIBRATE
        # calibrate_label = tk.Label(settings_frame, text="Calibrate (g):")
        # calibrate_label.grid(row=2, column=0, padx=5, pady=5)

        # self.calibrate_entry = tk.Entry(settings_frame, width=10)
        # self.calibrate_entry.insert(tk.END, self.calibrate)
        # self.calibrate_entry.grid(row=2, column=1, padx=5, pady=5)

        # update_button = tk.Button(settings_frame, text="Update", command=self.update_calibrate)
        # update_button.grid(row=2, column=2, padx=5, pady=5)
        


    def get_display_frame_width(self):
        return (self.window.winfo_screenwidth() * 45) // 100

    def read_serial_values(self):
        if self.serial_port.in_waiting > 0:
            line = self.serial_port.readline().decode().strip()
            # values = line.split(SCALES_VALUES_SEPARATOR)
            values = line
            print(values)
            return values
        return None


    # def update_calibrate(self):
    #     new_calibrate = self.calibrate_entry.get()
    #     self.calibrate = float(new_calibrate)

    def update_time_interval(self):
        new_interval = self.time_interval_entry.get()
        if new_interval.isdigit():
            new_interval = int(new_interval)
            if new_interval > 0:
                self.interval = new_interval
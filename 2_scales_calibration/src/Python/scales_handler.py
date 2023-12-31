import tkinter as tk
from tkinter import ttk
from scale import Scale

NUMBER_OF_SCALES = 1
SPACE_BETWEEN_FRAMES = 10
WIDTH = 45

class ScalesHandler:
    def __init__(self, parent, display_instance, serial_port):
        self.parent = parent
        self.display_instance = display_instance
        self.serial_port = serial_port
        self.scales = []   
        self.scale_frames = [] 
    
    def handle_scale_frames(self):
        for scale_num in range(1, NUMBER_OF_SCALES + 1):
            scale_frame = self.create_scale_frame(scale_num)
            print("Created scale frame ", scale_num)            
            scale = self.create_scale(scale_frame, scale_num, self.serial_port) 
            print("Created scale")
            self.create_buttons(scale)          
    
    
    def create_scale_frame(self, scale_num):
        width_ = self.display_instance.get_display_frame_width()
        print("width_ = ", width_)
        scale_frame = ttk.Frame(self.parent, width=width_)       
        scale_frame.grid(row=1, column=scale_num - 1, padx=SPACE_BETWEEN_FRAMES, pady=10)
        self.scale_frames.append(scale_frame)
        return scale_frame
    
    def create_scale(self, scale_frame, scale_num, serial_port):
        scale = Scale(scale_frame, scale_num, serial_port)
        self.scales.append(scale) 
        return scale
    
    def create_buttons(self, scale):
        self.create_start_stop_button(scale)
        self.create_clear_button(scale)
        self.create_calibrate_button(scale)  
    
    def create_start_stop_button(self, scale):
        index = scale.scale_num - 1
        button_text = "Start Measurements"  # Initial text
        start_stop_button = tk.Button(
            self.scale_frames[index], text=button_text, command=lambda: self.toggle_button_action(scale)
        )
        start_stop_button.pack(side="left")
        
        # Store the button and its initial text in the scale object
        scale.start_stop_button = start_stop_button
        scale.button_text = button_text
    
    def toggle_button_action(self, scale):
        if scale.button_text == "Start Measurements":
            scale.is_displaying.set(True)
            scale.button_text = "Stop Measurements"
        else:
            scale.is_displaying.set(False)
            scale.button_text = "Start Measurements"

        # Update the button text
        scale.start_stop_button.config(text=scale.button_text)

    def create_clear_button(self, scale):
        index = scale.scale_num - 1 
        clear_button = tk.Button(self.scale_frames[index], text="Clear", command=self.scales[index].clear_values)
        clear_button.pack(side="left")

    def create_calibrate_button(self, scale):
        index = scale.scale_num - 1
        calibrate_button = tk.Button(
            self.scale_frames[index], text="Calibrate", command=self.scales[index].send_calibration_command
        )
        calibrate_button.pack(side="left")

    def handle_display_values(self, input_string):
        if input_string:
            numbers_as_strings = input_string.split()
            buffer = bytearray([int(num) for num in numbers_as_strings])
            print("Buffer: ", buffer)
            if buffer and self.is_weight_message(buffer):
                floatWeights = self.decode_values(buffer)
                for scale_num, scale in enumerate(self.scales):
                    if scale.is_displaying.get():
                        scale.display_value(floatWeights[scale_num])  
    
    def decode_values(self, buffer):
        floatWeights = []
        number_of_scales = int(buffer[1])
        print("nr scales: ", number_of_scales)
        for i in range(number_of_scales):
            int_weight = (buffer[2 * i + 2] << 8) | buffer[2 * i + 3]
            print("int_weight ", i, ": ", int_weight)
            floatWeights.append(float(int_weight) / 100.0)
            print("float_weight ", i, ": ", floatWeights[i])
        return floatWeights

    def is_weight_message(self, buffer):
        print("Int(buffer[0]): ", int(buffer[0]))
        return int(buffer[0]) == 1
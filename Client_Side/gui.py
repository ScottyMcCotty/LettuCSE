"""This module contains the GUI class"""
import tkinter as tk
import threading


class GUI:

    window = tk.Tk()
    previous_label = None
    proceed = True
    stop_button = None
    main_button = None
    

    def __init__(self):
        self.window.geometry("1000x600")
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green')

        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n"
        "It was designed and implemented by Martin Orosa, Scott Ballinger, Mira Welner, and Liam Carr under "
        "the supervision of Dr. Lieth",
        bg='green')
        instructions_label.pack(pady=10)

    def update_status(self, update):
        if self.previous_label:
            self.previous_label.destroy()
        update_message = tk.Label(text=update, bg='green')
        update_message.pack(pady=5)
        self.previous_label=update_message

    def frame_arduino_label(self, port:str):
        frame_label = tk.Label(self.window,text = "Frame arduino port: " + port, bg="green")
        frame_label.place(relx = 0.0, rely = 1.0, anchor ='sw')

    def toolhead_arduino_label(self, port:str):
        toolhead_label = tk.Label(self.window,text = "Toolhead arduino port: " + port, bg="green")
        toolhead_label.place(relx = 1.0, rely = 1.0, anchor ='se')

    def configure_main_button(self, transplanting_function, source, destination, frame_arduino, toolhead_arduino,stop_button):
        start_and_stop_button = tk.Button(self.window, text="Click Here to Start Transplanting",
            command=lambda:threading.Thread(target=transplanting_function, args=(source, destination, frame_arduino, toolhead_arduino, start_and_stop_button, stop_button, self)).start())
        start_and_stop_button.pack(pady=20)

    def stop_process(self):
        self.proceed = False
        self.stop_button["state"] = tk.DISABLED

    
    def configure_stop_button(self):
        stop_button = tk.Button(self.window, text="Click Here to Stop Transplanting", command=self.stop_process)
        stop_button.pack(pady=20)
        self.stop_button = stop_button
        return stop_button
    

    def loop(self):
        self.window.mainloop()

    

    
"""This module contains the GUI class"""
import tkinter as tk
import threading

class GUI:

    window = tk.Tk()
    previous_label = None

    def __init__(self):
        self.window.geometry("1000x600")
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green')

        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n"
        "It was designed and implemented by Martin Orosa, Scott Ballinger, Mira Welner, and Liam Carr under "
        "the supervision of Dr. Lieth\n"
        "Use a keyboard interrupt (control c) to instantly freeze arm and shut down program\n"
        "Press 'e' when prompted to move arm to origin and end program\n"
        "Press any other key to begin", bg='green')
        instructions_label.pack(pady=5)

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

    def configure_start_button(self, transplanting_function, source, destination, frame_arduino, toolhead_arduino):
        start_and_top_button = tk.Button(self.window, text="Click Here to Start Transplanting",
            command=lambda:threading.Thread(target=transplanting_function, args=(source, destination, frame_arduino, toolhead_arduino)).start())
        start_and_top_button.pack(pady=20)

    def loop(self):
        self.window.mainloop()

    

    
"""This module contains the GUI class"""
import tkinter as tk
import threading
import turtle
from typing import Callable

class GUI:
    """
    A class to handle the graphical user interface

    ...

    Attributes
    ----------
    window:Tkinter object
        The main gui window
    turtle_canvas: Tkinter canvas
        The canvas that the turtle object moves
        around on to show where the head is going
    toolhead_location_label: tk.Label
        The tkinter label object that displays what
        the toolhead arduino is doing at the moment
    stop_button: tk.Button
        The button that stops the transplanting
        thread
    start_button: tk.Buttion
        The button that spawns the transplanting
        thread and continues the transplant after
        the process is paused

    Methods
    -------
    __init__():
        Creates the GUI window, the start and stop buttons, and all the lables
    update_frame_status():
        Updates the location of the frame based on input from the transplanter_robot
    update_toolhead_status():
        Updates the location of the frame based on input from the transplanter_robot
    toolhead_location_label():
        Displays the x and y coords of the frame
    stop_transplanting():
        stop the transplanting procccess and start over afterwards.
        This is NOT the pause that happens when a tray is being replaced
    continue_transplanting():
        continue transplant from where it left off
    set_buttons_to_pre_transplant_stage():
        start button can be clicked, stop button cannot
    set_buttons_to_in_transplant_stage():
        stop button can be clicked, start button cannot
    set_buttons_to_waiting_for_tray_replacement():
        either button can be clicked
    """

    window = tk.Tk()
    turtle_canvas = None
    toolhead_location_label = None
    stop_button = None
    start_button = None
    previous_toolhead_location = None
    turtle = None
    transplanting_thread = None
    continue_transplant = None
    end_transplant = None


    def __init__(self, transplant_function:Callable, end:Callable, continue_transplant:Callable):
        '''
            Initializes the main window, the start and stop
            buttons, the toolhead and frame lables, and the turtle canvas
        '''
        self.transplanting_thread = threading.Thread(target=transplant_function)
        self.continue_transplant = continue_transplant
        self.end_transplant = end
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green', height=800, width=1400)

        self.toolhead_location_label = tk.Label(bg="green")
        self.toolhead_location_label.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

        self.stop_button = tk.Button(self.window,
                                     text="End Transplanting",
                                     command=self.restart_transplanter,
                                     state=tk.DISABLED)
        self.stop_button.place(relx = 0.5, rely = 0.25, anchor=tk.CENTER)
        self.start_button = tk.Button(self.window, text="Start Transplanting", state=tk.NORMAL)
        self.start_button.place(relx = 0.5, rely = 0.2, anchor=tk.CENTER)

        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n\n\n"
                                            "It was designed and implemented by Martin Orosa,"
                                            "Scott Ballinger, Mira Welner, and Liam Carr "
                                            "under the supervision of Dr. Lieth",
                                        bg='green')
        instructions_label.place(relx = 0.5, rely = 0.05, anchor=tk.CENTER)
        self.set_up_turtle()


    def set_up_turtle(self) -> None:
        """Create the canvas and the 'turtle' object
        which will show visually how the toolhead will move"""
        self.turtle_canvas = tk.Canvas(master=None,width=550,height=375)
        self.turtle_canvas.place(relx = 0.5, rely = 0.7, anchor=tk.CENTER)
        self.turtle = turtle.RawTurtle(self.turtle_canvas)
        self.turtle_canvas.create_rectangle(-265, -180, -10, 180, fill='white')
        self.turtle_canvas.create_rectangle(10, -180, 265, 180, fill='white')
        self.turtle.shape("circle")
        self.turtle.turtlesize(0.4)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.setx(-265)
        self.turtle.sety(-180)
        self.restart_transplanter()


    def label_ports(self, toolhead_port:str, frame_port:str):
        """Show what ports the arduinos are connected to, or if they are connected at all"""
        frame_arduino_port_label = tk.Label(self.window,
                                            text = "Frame arduino port: " + frame_port,
                                            bg="green")
        frame_arduino_port_label.place(relx = 0.0, rely = 1.0, anchor ='sw')
        toolhead_arduino_port_label = tk.Label(self.window,
                                               text = "Toolhead arduino port: " + toolhead_port,
                                               bg="green")
        toolhead_arduino_port_label.place(relx = 1.0, rely = 1.0, anchor ='se')


    def move_turtle(self, parameters:tuple) -> None:
        """Move the turtle to given parameters"""
        self.turtle.showturtle()
        location_on_canvas = (round(parameters[0]/16 - 270), round(parameters[1]/20-160))
        self.turtle.goto(location_on_canvas)





    def restart_transplanter(self) -> None:
        """Configures the buttons such that the user can only begin transplanting"""
        if self.transplanting_thread.is_alive():
            self.end_transplant()
            #self.transplanting_thread.join()

        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(text="Start Transplanting",
                                 command=self.begin_transplanting,
                                 state=tk.NORMAL)

    def begin_transplanting(self) -> None:
        """Configures the buttons such that the user can only stop transplanting"""
        self.transplanting_thread.start()

        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="Start Transplanting",
                                 state=tk.DISABLED)

    def pause_transplant(self) -> None:
        """Configures the buttons such that the user can start or stop while replacing the tray"""
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="Trays have been replaced manually - continue transplanting",
                                 command=self.resume_transplant,
                                 state=tk.NORMAL)


    def resume_transplant(self) -> None:
        """Configures the buttons such that the user can start or stop while replacing the tray"""
        self.continue_transplant()
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="Start Transplanting",
                                 state=tk.DISABLED)


    def update_window(self, status:tuple, trays_need_replacing:bool)-> None:
        """Displays the GUI window - while this is running, everything in the thread stops"""
        if trays_need_replacing:
            self.pause_transplant()


        if self.previous_toolhead_location != status and status:
            self.move_turtle(status)
            self.toolhead_location_label.config(text="Toolhead at " + str(status))
            self.previous_toolhead_location = status

        self.window.update_idletasks()
        self.window.update()

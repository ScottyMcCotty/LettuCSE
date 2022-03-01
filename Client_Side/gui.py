"""This module contains the GUI class"""
import tkinter as tk
import threading
import turtle


from transplanter_robot import TransplanterRobot

class GUI:
    """
    A class to handle the graphical user interface

    ...

    Attributes
    ----------
    window:Tkinter object
        The main gui window
    toolhead_label: tk.Label
        The tkinter label object that displays what
        the toolhead arduino is doing at the moment
    frame_label: tk.Label
        The tkinter label object that displays what
        the frame arduino is doing at the moment
    stop_button: tk.Button
        The button that stops the transplanting
        thread
    start_button: tk.Buttion
        The button that spawns the transplanting
        thread and continues the transplant after
        the process is paused
    previous_state: Enum():
        The process state that the transplanter robot
        was in last frame
    transplanter_robot: TransplanterRobot
        An instance of the class representing
        the entire robot
    state: Enum()
        The state that the transplanter robot
        was in previously

    Methods
    -------
    __init__():
        Creates the GUI window, the start and stop buttons, and all the lables
    update_frame_status():
        Updates the location of the frame based on input from the transplanter_robot
    update_toolhead_status():
        Updates the location of the frame based on input from the transplanter_robot
    label_frame_arduino_port():
        Displays in the bottom left corner which port the frame arduino is connected on
    label_toolhead_arduino_port():
        Displays in the bottom read corner which port the toolhead arduino is connected on
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
    toolhead_label = None
    frame_label = None
    stop_button = None
    start_button = None
    previous_state = None
    transplanter = None
    state = None
    previous_toolhead_location = None
    turtle = None

    def __init__(self, transplanter:TransplanterRobot):
        '''
            Initializes the main window, the start and stop
            buttons in the PRE_TRANSPLANT state, the toolhead
            and frame lables, and the toolhead and frame port lables
        '''
        self.transplanter = transplanter
        self.state = transplanter.button_stages
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green', height=800, width=1400)

        self.frame_label = tk.Label(bg="green")
        self.frame_label.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

        self.toolhead_label = tk.Label(bg="green")
        self.toolhead_label.place(relx = 0.5, rely = 0.35, anchor=tk.CENTER)

        self.stop_button = tk.Button(self.window,
                                    text="End Transplanting",
                                    command=self.stop_transplanting,
                                    state=tk.DISABLED)
        self.stop_button.place(relx = 0.5, rely = 0.25, anchor=tk.CENTER)
        self.start_button = tk.Button(self.window,
                                      text="Start Transplanting",
                                      command=lambda:threading.Thread(target=self.transplanter.transplant).start(),
                                      state=tk.NORMAL)
        self.start_button.place(relx = 0.5, rely = 0.2, anchor=tk.CENTER)

        frame_label = tk.Label(self.window,text = "Frame arduino port: " + self.transplanter.frame_arduino.port, bg="green")
        frame_label.place(relx = 0.0, rely = 1.0, anchor ='sw')


        toolhead_label = tk.Label(self.window,text = "Toolhead arduino port: " + self.transplanter.toolhead_arduino.port, bg="green")
        toolhead_label.place(relx = 1.0, rely = 1.0, anchor ='se')

        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n\n\n"
                                            "It was designed and implemented by Martin Orosa,"
                                            "Scott Ballinger, Mira Welner, and Liam Carr "
                                            "under the supervision of Dr. Lieth",
                                        bg='green')
        instructions_label.place(relx = 0.5, rely = 0.05, anchor=tk.CENTER)

        self.turtle_canvas = tk.Canvas(master=None,width=550,height=375)

        self.turtle_canvas.place(relx = 0.5, rely = 0.7, anchor=tk.CENTER)
        self.turtle = turtle.RawTurtle(self.turtle_canvas)
        #create sparse board
        self.turtle_canvas.create_rectangle(-265, -180, -10, 180, fill='white')
        self.turtle_canvas.create_rectangle(10, -180, 265, 180, fill='white')

        self.turtle.shape("circle")
        self.turtle.turtlesize(0.4)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.setx(-265)
        self.turtle.sety(-180)


    def stop_transplanting(self) -> None:
        """Signals to the transplant function in main that the transplanting should finish"""
        self.transplanter.current_state = self.state.PRE_TRANSPLANT


    def continue_transplanting(self) -> None:
        """The main button is given this command when it is pressed
        after the first time. This spawns no new threads and simply continues
        the transplanting process"""
        self.transplanter.current_state = self.state.IN_TRANSPLANT

    def move_turtle(self, parameters) -> None:
        self.turtle.showturtle()
        location_on_canvas = (round(parameters[0]/16 - 270), round(parameters[1]/20-160))
        print(location_on_canvas)
        self.turtle.goto(location_on_canvas)

    def set_buttons_to_pre_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only begin transplanting"""
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(text="Start Transplanting",
                                 command=lambda:threading.Thread(target=self.transplanter.transplant).start(),
                                 state=tk.NORMAL)

    def set_buttons_to_in_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only stop transplanting"""
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="Start Transplanting",
                                 command=lambda:threading.Thread(target=self.transplanter.transplant).start(),
                                 state=tk.DISABLED)

    def set_buttons_to_waiting_for_tray_replacement(self) -> None:
        """Configures the buttons such that the user can start or stop while replacing the tray"""
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="Trays have been replaced manually - continue transplanting",
                                 command=self.continue_transplanting,
                                 state=tk.NORMAL)


    def display_window_frame(self)-> None:
        """Displays the GUI window - while this is running, everything in the thread stops"""
        if self.transplanter.current_state is not self.previous_state:
            if self.transplanter.current_state is self.state.PRE_TRANSPLANT:
                self.set_buttons_to_pre_transplant_stage()
            elif self.transplanter.current_state is self.state.IN_TRANSPLANT:
                self.set_buttons_to_in_transplant_stage()
            elif self.transplanter.current_state is self.state.WAIT:
                self.set_buttons_to_waiting_for_tray_replacement()
            self.previous_state = self.transplanter.current_state
        
        if self.previous_toolhead_location != self.transplanter.frame_arduino.status and self.transplanter.frame_arduino.status:
            self.move_turtle(self.transplanter.frame_arduino.status)
            self.previous_toolhead_location = self.transplanter.frame_arduino.status
            self.toolhead_label.config(text = self.transplanter.toolhead_arduino.status)
            self.frame_label.config(text="Frame arduino moving toolhead to " 
                                      + str(self.transplanter.frame_arduino.status))

        self.window.update_idletasks()
        self.window.update()

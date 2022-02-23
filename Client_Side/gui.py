"""This module contains the GUI class"""
import tkinter as tk
import threading

from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino

class GUI:
    """
    A class to handle the graphical user interface

    ...

    Attributes
    ----------
    window : tkinter object (tk.TK)
        the main gui window
    previous_status_label: string
        the center of the gui contains a status update, and
        when a new one is displayed the old one must be deleted.
        this attribute holds the old label so it can be deleted
    continue_transplanting: boolean
        if this value is true, then the transplant function in main
        continues looping. If not, it stops
    start_button: tk.Button
        the button for spawning the thread to run the transplant function
    stop_button: tk.Button
        the button for stopping the transplant

    Methods
    -------
    update_status(status_message):
        Updates the center label that says what the transplanter is doing  with the new message
    frame_arduino_label(status_message):
        Displays in the bottom left corner which port the frame arduino is connected on
    toolhead_arduino_label(status_message):
        Displays in the bottom read corner which port the toolhead arduino is connected on
    make_start_button(self, transplant, source, destination, frame_arduino, toolhead_arduino):
        Uses the transplant function and its args to spawn a thread that runs the 'transplant'
        function after the start button is pressed
    stop_transplanting():
        stop the transplanting procccess and start over afterwards.
        This is NOT the pause that happens when a tray is being replaced
    configure_stop_button():
        creates the button that stops the transplanting and starts over
    set_buttons_to_pre_transplant_stage():
        start button can be clicked, stop button cannot
    set_buttons_to_in_transplant_stage():
        stop button can be clicked, start button cannot
    set_buttons_to_waiting_for_tray_replacement():
        either button can be clicked
    """

    window = tk.Tk()
    previous_toolhead_status = ""
    previous_frame_status = ""
    continue_transplanting = True
    stop_button = None
    start_button = None
    toolhead_arduino = None
    frame_arduino = None

    def __init__(self, frame_arduino:FrameArduino, toolhead_arduino:ToolheadArduino):
        """
            Initializes the main window (self.window),
            the stop button (self.stop_button)
            and creates the instructions label which is not
            an attribute
        """
        self.window.geometry("1000x600")
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green')
        self.toolhead_arduino = toolhead_arduino
        self.frame_arduino = frame_arduino
        self.label_frame_arduino_port()
        self.label_toolhead_arduino_port()
        self.configure_stop_button()
        

        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n"
        "It was designed and implemented by Martin Orosa, Scott Ballinger, Mira Welner, "
        "and Liam Carr under the supervision of Dr. Lieth",
        bg='green')
        instructions_label.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

    def update_frame_status(self) -> None:
        '''
            Gets the frame status from the arduino and displays it in the frame staus section
            Parameters:
                    None
            Returns:
                    None
        '''
        if self.previous_frame_status is not self.frame_arduino.status:
            update_message = tk.Label(text="Frame Arduino Status: " + self.frame_arduino.status, bg='green')
            update_message.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
            self.previous_frame_status = self.frame_arduino.status

    def update_toolhead_status(self) -> None:
        '''
            Gets the frame status from the arduino and displays it in the frame staus section
            Parameters:
                    None
            Returns:
                    None
        '''
        if self.previous_toolhead_status is not self.toolhead_arduino.status:
            update_message = tk.Label(text="Toolhead Arduino Status: " + self.toolhead_arduino.status, bg='green')
            update_message.place(relx = 0.5, rely = 0.6, anchor=tk.CENTER)
            self.previous_toolhead_status = self.toolhead_arduino.status

    def label_frame_arduino_port(self) -> None:
        '''
            Displays in the bottom right corner which port the toolhead arduino is connected on
            Parameters:
                    port (str): the port address to be displayed

            Returns:
                    None
        '''
        frame_label = tk.Label(self.window,text = "Frame arduino port: " + self.frame_arduino.port, bg="green")
        frame_label.place(relx = 0.0, rely = 1.0, anchor ='sw')

    def label_toolhead_arduino_port(self) -> None:
        '''
            Displays in the bottom right corner which port the toolhead arduino is connected on
            Parameters:
                    port (str): the port address to be displayed

            Returns:
                    None
        '''
        toolhead_label = tk.Label(self.window,text = "Toolhead arduino port: " + self.toolhead_arduino.port, bg="green")
        toolhead_label.place(relx = 1.0, rely = 1.0, anchor ='se')

    def make_start_button(self, transplant_robot) -> None:
        '''
            The main button must spawn another thread so it can run simultaniously to the gui.
            It also must have the transplanting function from the main file fed into it, the
            args seperately from the target. The lambda before the threading.Thread is so that
            it only runs the function once it is clicked and a new thread is spawned.

            Parameters:
                    transplanting_function (function): the function from main which transplants
                    source (Tray): the tray that the lettuce is being moved from
                    destination (Tray): the tray that the lettuce is being moved to
                    frame_arduino (FrameArduino) the arduino controling the frame
                    toolhead_arduino (ToolheadArduino) the arduino controling the toolhead

            Returns:
                    None
        '''
        start_button = tk.Button(self.window,  text="Start Transplanting",
            command=lambda:threading.Thread(target=transplant_robot.transplant).start())
        start_button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)
        self.start_button = start_button

    def stop_transplanting(self) -> None:
        """Signals to the transplant function in main that the transplanting should finish"""
        self.continue_transplanting = False
        self.stop_button["state"] = tk.DISABLED

    def stop_waiting(self) -> None:
        self.stop_waiting = 1

    def configure_stop_button(self) -> None:
        """Create the second button that stops the transplanting"""
        stop_button = tk.Button(self.window,
                                text="End Transplanting",
                                command=self.stop_transplanting)
        stop_button.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
        stop_button["state"] = tk.DISABLED
        self.stop_button = stop_button


    def set_buttons_to_pre_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only begin transplanting"""
        self.continue_transplanting = True
        self.stop_button["text"] = "End Transplanting"
        self.stop_button["state"] = tk.DISABLED
        self.start_button["text"] = "Start Transplanting"
        self.start_button["state"] = tk.NORMAL
        

    def set_buttons_to_in_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only stop transplanting"""
        self.start_button["state"] = tk.DISABLED
        self.start_button["text"] = "Transplanting In Process"
        self.stop_button["state"] = tk.NORMAL
        self.stop_button["text"] = "End Transplanting"

    def set_buttons_to_waiting_for_tray_replacement(self) -> None:
        """Configures the buttons such that the user can start or stop while replacing the tray"""
        self.start_button["state"] = tk.NORMAL
        self.start_button["text"] = "Trays Have Been Replaced, Continue Transplanting"
        self.stop_button["state"] = tk.NORMAL
        self.stop_button["text"] = "End Transplanting"


    def display_window_frame(self)-> None:
        """Displays the GUI window - while this is running, everything in the thread stops"""
        self.update_frame_status()
        self.update_toolhead_status()
        self.window.update_idletasks()
        self.window.update()
        

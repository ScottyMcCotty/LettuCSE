"""This module contains the GUI class"""
import tkinter as tk
import threading

from transplanter_robot import TransplanterRobot

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
    start_button: tk.Button
        the button for spawning the thread to run the transplant function
    stop_button: tk.Button
        the button for stopping the transplant

    Methods
    -------
    update_frame_status():
        Updates the location of the frame based on input from the transplanter_robot
    update_toolhead_status():
        Updates the location of the frame based on input from the transplanter_robot
    label_frame_arduino_port():
        Displays in the bottom left corner which port the frame arduino is connected on
    label_toolhead_arduino_port():
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
    previous_toolhead_status_label = None
    previous_frame_status_label = None
    previous_start_button = None
    previous_stop_button = None
    stop_button = None
    start_button = None
    transplanter_robot = None
    state = None

    def __init__(self, transplanter_robot:TransplanterRobot):
        """
            Initializes the main window (self.window),
            the stop button (self.stop_button)
            and creates the instructions label which is not
            an attribute
        """
        self.window.geometry("1000x600")
        self.window.title("Lettuce Transplanter")
        self.window.configure(bg= 'green')
        self.toolhead_arduino = transplanter_robot.toolhead_arduino
        self.state = transplanter_robot.button_stages
        self.previous_state = None
        self.previous_start_button = None
        self.previous_stop_button = None
        self.transplanter_robot = transplanter_robot
        self.label_frame_arduino_port()
        self.label_toolhead_arduino_port()
        instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n"
                                            "It was designed and implemented by Martin Orosa,"
                                            "Scott Ballinger, Mira Welner, and Liam Carr "
                                            "under the supervision of Dr. Lieth",
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
        if self.previous_frame_status is not self.transplanter_robot.frame_arduino.status:
            frame_status = tk.Label(text="Frame Arduino Status: " + self.transplanter_robot.frame_arduino.status, bg='green')
            frame_status.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
            self.previous_frame_status = self.transplanter_robot.frame_arduino.status
            #if self.previous_frame_status_label:
                #self.previous_frame_status_label.destroy()
            self.previous_frame_status_label = frame_status

    def update_toolhead_status(self) -> None:
        '''
            Gets the frame status from the arduino and displays it in the frame staus section
            Parameters:
                    None
            Returns:
                    None
        '''
        if self.previous_toolhead_status is not self.toolhead_arduino.status:
            toolhead_status = tk.Label(text="Toolhead Arduino Status: " + self.toolhead_arduino.status, bg='green')
            toolhead_status.place(relx = 0.5, rely = 0.6, anchor=tk.CENTER)
            self.previous_toolhead_status = self.toolhead_arduino.status
            #if self.previous_toolhead_status_label:
                #self.previous_toolhead_status_label.destroy()
            self.previous_toolhead_status_label = toolhead_status

    def label_frame_arduino_port(self) -> None:
        '''
            Displays in the bottom right corner which port the toolhead arduino is connected on
            Parameters:
                    port (str): the port address to be displayed

            Returns:
                    None
        '''
        frame_label = tk.Label(self.window,text = "Frame arduino port: " + self.transplanter_robot.frame_arduino.port, bg="green")
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

    def stop_transplanting(self) -> None:
        """Signals to the transplant function in main that the transplanting should finish"""
        self.transplanter_robot.current_state = self.state.PRE_TRANSPLANT


    def continue_transplanting(self) -> None:
        """The main button is given this command when it is pressed
        after the first time. This spawns no new threads and simply continues
        the transplanting process"""
        self.transplanter_robot.current_state = self.state.IN_TRANSPLANT

    def eliminate_previous_buttons(self) -> None:
        """Removes any previous buttons so that you don't have buttons behind
        the new buttons"""
        if self.previous_stop_button:
            self.previous_stop_button.destroy()
        if self.previous_start_button:
            self.previous_start_button.destroy()

    def set_buttons_to_pre_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only begin transplanting"""
        self.transplanter_robot.continue_transplanting = True
        stop_button = tk.Button(self.window,
                                text="End Transplanting",
                                command=self.stop_transplanting,
                                state=tk.DISABLED)
        stop_button.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
        self.start_button = tk.Button(self.window,
                                      text="Start Transplanting",
                                      command=lambda:threading.Thread(target=self.transplanter_robot.transplant).start(),
                                      state=tk.NORMAL)
        self.start_button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)
        self.eliminate_previous_buttons()




    def set_buttons_to_in_transplant_stage(self) -> None:
        """Configures the buttons such that the user can only stop transplanting"""
        stop_button = tk.Button(self.window,
                                text="End Transplanting",
                                command=self.stop_transplanting,
                                state=tk.NORMAL)
        stop_button.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
        self.start_button = tk.Button(self.window,
                                      text="Start Transplanting",
                                      command=lambda:threading.Thread(target=self.transplanter_robot.transplant).start(),
                                      state=tk.DISABLED)
        self.start_button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)
        self.eliminate_previous_buttons()

    def set_buttons_to_waiting_for_tray_replacement(self) -> None:
        """Configures the buttons such that the user can start or stop while replacing the tray"""
        stop_button = tk.Button(self.window,
                                text="End Transplanting",
                                command=self.stop_transplanting,
                                state=tk.NORMAL)
        stop_button.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
        self.start_button = tk.Button(self.window,
                                      text="Trays have been replaced manually - continue transplanting",
                                      command=self.continue_transplanting,
                                      state=tk.NORMAL)
        self.start_button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)
        self.eliminate_previous_buttons()


    def display_window_frame(self)-> None:
        """Displays the GUI window - while this is running, everything in the thread stops"""
        if self.transplanter_robot.current_state is not self.state.IN_TRANSPLANT:
            print(self.transplanter_robot.current_state)
        if self.transplanter_robot.current_state is not self.previous_state:
            if self.transplanter_robot.current_state is self.state.PRE_TRANSPLANT:
                self.set_buttons_to_pre_transplant_stage()
            elif self.transplanter_robot.current_state is self.state.IN_TRANSPLANT:
                self.set_buttons_to_in_transplant_stage()
            elif self.transplanter_robot.current_state is self.state.WAIT:
                self.set_buttons_to_waiting_for_tray_replacement()
        self.previous_state = self.transplanter_robot.current_state
        self.update_frame_status()
        self.update_toolhead_status()
        self.window.update_idletasks()
        self.window.update()

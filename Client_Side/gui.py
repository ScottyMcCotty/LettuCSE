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
    transplant_thread = None
    transplant_function = None
    continue_transplant = None
    end_transplant = None

    # LIAM
    json_enter_button = None
    json_exit_button = None
    instructions_label = None
    json_intro_label = None
    json_confirm_label = None
    json_confirm_continue_button = None
    json_confirm_exit_button = None
    json_instructions = None
    step1_source_button = None
    step1_destination_button = None
    json_exit_popup = None
    json_exit_yes = None
    json_exit_no = None
    json_picture = None
    json_picture_canvas = None
    # /LIAM

    def __init__(self, transplant_function:Callable, end:Callable, continue_transplant:Callable):
        '''
            Initializes the main window, the start and stop
            buttons, the toolhead and frame lables, and the turtle canvas
        '''
        self.transplant_function = transplant_function
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

        self.instructions_label = tk.Label(text="Welcome to the LettuCSE Lettuce Transplanter\n\n\n"
                                            "It was designed and implemented by Martin Orosa,"
                                            "Scott Ballinger, Mira Welner, and Liam Carr "
                                            "under the supervision of Dr. Lieth",
                                        bg='green')
        self.instructions_label.place(relx = 0.5, rely = 0.05, anchor=tk.CENTER)

        self.set_up_turtle()

        # LIAM
        self.json_enter_button = tk.Button(self.window,
                                     text="Create a JSON config for your tray\n(ends transplanting)",
                                     command=self.set_up_json_config,
                                     state=tk.NORMAL)
        self.json_enter_button.place(relx = .1, rely = .2, anchor=tk.CENTER)
        # Initialize various buttons but do not place
        self.json_exit_button = tk.Button(self.window,
                                     text="Exit config generation",
                                     command=self.confirm_config_exit,
                                     state=tk.NORMAL)
        self.json_exit_yes = tk.Button(self.window,
                                     text="Exit",
                                     command=self.set_down_json_config,
                                     state=tk.NORMAL)
        self.json_exit_no = tk.Button(self.window,
                                     text="Cancel",
                                     command=self.json_cancel_exit,
                                     state=tk.NORMAL)                             
        self.json_confirm_continue_button = tk.Button(self.window,
                                     text="Proceed",
                                     command=self.set_json_step1_config,
                                     state=tk.NORMAL)
        self.json_confirm_exit_button = tk.Button(self.window,
                                     text="Go back",
                                     command=self.set_down_json_config,
                                     state=tk.NORMAL)     
        self.step1_source_button = tk.Button(self.window,
                                     text="Source tray",
                                     #command=self.set_down_json_config,#TEMP, should set the tray type AND call set_json_step2_config
                                     state=tk.NORMAL)
        self.step1_destination_button = tk.Button(self.window,
                                     text="Destination tray",
                                     #command=self.set_down_json_config,#TEMP, should set the tray type AND call set_json_step2_config
                                     state=tk.NORMAL)                          
        # Initialize various labels but do not place
        self.json_intro_label = tk.Label(text="JSON File Creation Tool", bg='green')
        self.json_confirm_label = tk.Label(text="\n\n"
                                              "You have entered the process for creating a "
                                              "JSON config file. This file is used to mark"
                                              " where the toolhead needs to move to interact with "
                                              "plants.\n"
                                              "This process will require precise manual measurements"
                                              " of the physical trays.", bg='green')
        self.json_exit_popup = tk.Label(text="NOTE: Exiting now will discard\n"
                                             "any information already entered.", bg='yellow')
        self.json_confirm_warning = tk.Label(text="NOTE: Completing this process will create a new file:\n"
                                                "custom_sparse_tray.json or custom_dense_tray.json. If this"
                                                " file already exists within the directory, it will"
                                                " be overwritten.\nProceed?", bg='yellow')
        self.json_instructions = tk.Label(text="Indicate whether the information being entered is "
                                               "for the source (dense) tray or the destination (sparse) tray.", bg='green')
        # Initialize picture(s) but do not place
        self.json_picture_canvas = tk.Canvas(master=None,width=550,height=375)
        self.json_picture = tk.PhotoImage(file="images/Thonking.png")
        # /LIAM

    # LIAM
    def set_up_json_config(self):
        # End transplanting, if applicable
        self.restart_transplanter()

        # Temporarily remove objects from transplanter GUI
        self.start_button.place_forget()
        self.stop_button.place_forget()
        self.turtle_canvas.place_forget()
        self.json_enter_button.place_forget()
        self.toolhead_location_label.place_forget()

        # ORIGINAL CODE EDITED: instructions_label now a global variable
        self.instructions_label.place_forget()
        self.json_intro_label.place(relx = 0.5, rely = 0.02, anchor=tk.CENTER)

        self.json_confirm_label.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)
        self.json_confirm_warning.place(relx = 0.5, rely = 0.2, anchor=tk.CENTER)

        self.json_confirm_continue_button.place(relx = 0.45, rely = .26, anchor=tk.CENTER)
        self.json_confirm_exit_button.place(relx = 0.55, rely = .26, anchor=tk.CENTER)

        # 1. Clear other things on the window
        # 2. Display pictures & text boxes to allow user's input
        # 3. Move onto the next picture & question when input is processed
        # 4. Use information to generate JSON file

    def confirm_config_exit(self):
        # Remove relevant objects
        self.json_exit_button.place_forget()

        # Place warning window w/ buttons
        self.json_exit_popup.place(relx = 0.1, rely = .2, anchor=tk.CENTER)
        self.json_exit_yes.place(relx = 0.08, rely = .25, anchor=tk.CENTER)
        self.json_exit_no.place(relx = 0.12, rely = .25, anchor=tk.CENTER)

    def json_cancel_exit(self):
        # Remove warning window w/ buttons
        self.json_exit_popup.place_forget()
        self.json_exit_yes.place_forget()
        self.json_exit_no.place_forget()

        # Replace exit button
        self.json_exit_button.place(relx = .1, rely = .2, anchor=tk.CENTER)

    def set_down_json_config(self):
        # Remove objects from json config GUI
        self.json_intro_label.place_forget()
        self.json_exit_button.place_forget()
        self.json_confirm_label.place_forget()
        self.json_confirm_warning.place_forget()
        self.json_confirm_continue_button.place_forget()
        self.json_confirm_exit_button.place_forget()
        self.json_instructions.place_forget()
        self.step1_source_button.place_forget()
        self.step1_destination_button.place_forget()
        self.json_exit_popup.place_forget()
        self.json_exit_yes.place_forget()
        self.json_exit_no.place_forget()
        self.json_picture_canvas.place_forget()

        # Replace objects from transplanter GUI
        self.start_button.place(relx = 0.5, rely = 0.2, anchor=tk.CENTER)
        self.stop_button.place(relx = 0.5, rely = 0.25, anchor=tk.CENTER)
        self.turtle_canvas.place(relx = 0.5, rely = 0.7, anchor=tk.CENTER)
        self.instructions_label.config(text="Welcome to the LettuCSE Lettuce Transplanter\n\n\n"
                                            "It was designed and implemented by Martin Orosa,"
                                            "Scott Ballinger, Mira Welner, and Liam Carr "
                                            "under the supervision of Dr. Lieth",
                                        bg='green')
        self.instructions_label.place(relx = 0.5, rely = 0.05, anchor=tk.CENTER)
        self.json_enter_button.place(relx = .1, rely = .2, anchor=tk.CENTER)
        self.toolhead_location_label.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

    def set_json_step1_config(self):
        # Remove previous instruction(s)
        self.json_confirm_label.place_forget()
        self.json_confirm_warning.place_forget()
        self.json_confirm_continue_button.place_forget()
        self.json_confirm_exit_button.place_forget()

        # Place new instructions/pictures/buttons
        self.json_exit_button.place(relx = .1, rely = .2, anchor=tk.CENTER)
        self.instructions_label.config(text="Step 1 of X: Specify tray type", bg='green')
        self.instructions_label.place(relx = 0.5, rely = 0.05, anchor=tk.CENTER)
        self.json_instructions.place(relx = 0.5, rely = 0.15, anchor=tk.CENTER)
        self.step1_source_button.place(relx = 0.45, rely = 0.2, anchor = tk.CENTER)
        self.step1_destination_button.place(relx = 0.55, rely = 0.2, anchor = tk.CENTER)

        # TEST FOR PICTURE
        # NOTE TO SELF: (0,0) on the canvas is the upper left corner
        self.json_picture_canvas.place(relx = 0.5, rely = 0.7, anchor=tk.CENTER)
        self.json_picture_canvas.create_image(275, 200, anchor=tk.CENTER, image=self.json_picture)
        

    def set_json_step2_config(self):

        # Place new instructions/pictures/buttons
        self.json_instructions.config(text="Please enter the height & width of the tray", bg='green')
        self.json_instructions.place(relx = 0.5, rely = 0.15, anchor=tk.CENTER)
    # /LIAM


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
        location_on_canvas = (round(parameters[0]/16 - 260), round(parameters[1]/20-160))
        self.turtle.goto(location_on_canvas)





    def restart_transplanter(self) -> None:
        """Configures the buttons such that the user can only begin transplanting"""
        if self.transplant_thread and self.transplant_thread.is_alive():
            self.end_transplant()
            self.transplant_thread.join()
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(text="Start Transplanting",
                                 command=self.begin_transplanting,
                                 state=tk.NORMAL)

    def begin_transplanting(self) -> None:
        """Configures the buttons such that the user can only stop transplanting"""
        self.transplant_thread = threading.Thread(target=self.transplant_function)
        self.transplant_thread.start()

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

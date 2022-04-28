"""Module contains the GUI class"""

from tkinter import N, Tk, Label, PhotoImage, CENTER, NORMAL, Button, DISABLED, Canvas, Entry, END
from tray_info import tray_info

class windowHandler():
    """
    This class bundles all the 'junk' that comes with the tkinter class that doesn't need to
    be exposed to the GUI, such as size, title, etc.
    ...

    Attributes
    ----------
    window : Tkinter Object
        tkinter has an object instance that stores everything involving
        the GUI

    Methods (REDO LATER)
    -------
    set_window_to_paused()
        change the window color to red
    set_window_to_unpaused()
        change the window color to green
    """
    tray_measurements = None

    window = None

    current_step = -1
    current_progress = -2
    
    # The buttons.
    start_measuring_button = None
    skip_measuring_button = None

    
    confirm_continue_button = None
    confirm_exit_button = None

    return_title_button = None
    
    confirm_return_yes = None
    confirm_return_no = None

    continue_button = None
    back_button = None

    step1_source_button = None
    step1_destination_button = None

    accept_input_button = None

    # The labels.
    main_title = None
    start_measuring_warning = None
    confirm_return_warning = None
    step_title = None
    step_instructions = None
    text_entry_warning = None
    text_entryA_label = None
    text_entryB_label = None

    # The pictures & canvases.
    step2_pictureA_canvas = None
    step2_pictureA = None
    step3_pictureA_canvas = None
    step3_pictureA = None
    step4_pictureA_canvas = None
    step4_pictureA = None

    # The text input boxes.
    text_entryA = None
    text_entryB = None


    def __init__(self, tkinter_object:Tk) -> None:
        self.window = tkinter_object
        self.window.title("LettuCSE Config Tool")
        self.window.geometry("1000x800")
        self.window.configure(bg = 'light green')

        self.tray_measurements = tray_info(self.window)

        # Instantiate all buttons and images.
        # TITLE SCREEN
        self.main_title = Label(text = "JSON File Creation Tool\n\n\n"
                                            "This program can walk you through the process for creating a "
                                            "JSON config file.\nThis file is used to mark"
                                            " where the toolhead needs to move to interact with "
                                            "plants.\n"
                                            "If creating a new file, this process will require "
                                            "precise manual measurements of the physical trays.",
                                        font = ("Arial", 15),
                                        bg = 'light green')
        

        self.start_measuring_button = Button(self.window,
                                     text = "Create a new JSON\nconfig from scratch",
                                     font = ("Arial", 10),
                                     command = self.start_measuring_button_handler,
                                     state = NORMAL)
        

        self.skip_measuring_button = Button(self.window,
                                     text = "Use existing measurements\nto create a JSON config",
                                     font = ("Arial", 10),
                                     command = self.title_screen, #TODO: Set up skipping steps directly into designating holes in file
                                     state = NORMAL)
        

        # CONFIRM SELECTION SCREEN (start user measurements)
        self.start_measuring_warning = Label(text = "NOTE: Completing this process will create a new file:\n"
                                                  "custom_sparse_tray_measurements.json or custom_dense_tray_measurements.json.\n"
                                                  "If this file already exists within the directory, it will"
                                                  " be overwritten.\nProceed?",
                                             font = ("Arial", 12),
                                             bg = 'yellow')
        self.confirm_continue_button = Button(self.window,
                                              text = "Proceed",
                                              font = ("Arial", 10),
                                              command = self.step1_screen,
                                              state = NORMAL)
        self.confirm_exit_button = Button(self.window,
                                              text = "Go back",
                                              font = ("Arial", 10),
                                              command = self.title_screen,
                                              state = NORMAL)

        # EXIT BUTTON (present on all steps to return to title screen)
        self.return_title_button = Button(self.window,
                                     text = "Exit config generation",
                                     command = self.confirm_title_return,
                                     state = NORMAL)
        self.confirm_return_warning = Label(text="NOTE: Exiting now will discard\n"
                                            "any information already entered.",
                                            font = ("Arial", 10),
                                            bg='yellow')
        self.confirm_return_yes = Button(self.window,
                                     text = "Exit",
                                     command = self.title_screen,
                                     state = NORMAL)
        self.confirm_return_no = Button(self.window,
                                     text = "Cancel",
                                     command = self.cancel_return,
                                     state = NORMAL)

        # CONTINUE & BACK BUTTONS (present on all steps to move between steps)
        self.continue_button = Button(self.window,
                                      text = "Next step",
                                      command = self.next_step,
                                      state = DISABLED)
        self.back_button = Button(self.window,
                                  text = "Previous step",
                                  command = self.previous_step,
                                  state = DISABLED)

        # STEP 1 SCREEN (source or destination tray?)  
        self.step_title = Label(text = "Step 1 of 7\n\nSpecify tray type",
                                 font = ("Arial", 15),
                                 bg = 'light green')
        self.step_instructions = Label(text = "Indicate whether the information being entered is "
                                               "for the source (dense) tray or the destination (sparse) tray.",
                                        font = ("Arial", 15),
                                        bg = 'light green')
        self.step1_source_button = Button(self.window,
                                          text = "Source tray",
                                          command = self.step1_source,#lambda: self.step2_screen("Source"),
                                          state = NORMAL)
        self.step1_destination_button = Button(self.window,
                                               text = "Destination tray",
                                               command = self.step1_destination,#lambda: self.step2_screen("Destination"),
                                               state = NORMAL)

        # STEP 2 SCREEN (length & width of tray holes?)
        self.step2_pictureA_canvas = Canvas(master = None, width = 542, height = 548)
        self.step2_pictureA = PhotoImage(file = "images/step2Image.png")
        self.text_entry_warning = Label(text = "NOTE: Any invalid/large\ninput will be discarded.",
                                        font = ("Arial", 12),
                                        bg = 'yellow')
        self.text_entryA_label = Label(text = "Length:",
                                        font = ("Arial", 12),
                                        bg = 'light green')
        self.text_entryB_label = Label(text = " Width:",
                                        font = ("Arial", 12),
                                        bg = 'light green')                                
        self.text_entryA = Entry(self.window,
                                 bd = 5)
        self.text_entryB = Entry(self.window,
                                 bd = 5)
        self.accept_input_button = Button(self.window,
                                          text = "Enter input",
                                          command = self.accept_input,
                                          state = NORMAL)

        # STEP 3 SCREEN (long & short axis distance between holes?)
        self.step3_pictureA_canvas = Canvas(master = None, width = 504, height = 378)
        self.step3_pictureA = PhotoImage(file = "images/step3Image.png")

        # STEP 4 SCREEN (long & short axis distance to edge?)
        self.step4_pictureA_canvas = Canvas(master = None, width = 504, height = 378)
        self.step4_pictureA = PhotoImage(file = "images/step4Image.png")
                                              
        # Initialize to title screen.
        self.title_screen()

        #title_photo = PhotoImage(file='images/title.png')
        #title_label = Label(self.window,image = title_photo, borderwidth=0,)
        #self.window.image = title_photo
        #title_label.place(relx = 0.5, rely = 0.1, anchor = N)

    # Function for instantiating the title screen.
    def title_screen(self) -> None:
        """Hides everything else and displays the title screen"""
        # Hide all non-title screen objects.
        # TODO
        self.start_measuring_warning.place_forget()
        self.confirm_continue_button.place_forget()
        self.confirm_exit_button.place_forget()

        # Hide confirmation of return objects.
        self.confirm_return_warning.place_forget()
        self.confirm_return_yes.place_forget()
        self.confirm_return_no.place_forget()

        # Reset and hide tray information.
        self.tray_measurements.tray_name = "Placeholder"
        self.tray_measurements.hole_length = -1.0
        self.tray_measurements.hole_width = -1.0
        self.tray_measurements.short_axis_distance = -1.0
        self.tray_measurements.short_axis_distance_to_edge = -1.0
        self.tray_measurements.long_axis_distance = -1.0
        self.tray_measurements.long_axis_distance_to_edge = -1.0
        self.tray_measurements.extra_gap = -1
        self.tray_measurements.rows = -1
        self.tray_measurements.columns = -1
        self.tray_measurements.rows_between_gap = -1
        #self.tray_measurements.update_info()
        self.tray_measurements.hide_label()

        self.current_step = -1
        self.current_progress = -2
        self.continue_button.config(state = DISABLED)
        self.continue_button.place_forget()
        self.back_button.config(state = DISABLED)
        self.back_button.place_forget()

        # Hide step 1 objects.
        self.step_title.place_forget()
        self.step_instructions.place_forget()
        self.step1_source_button.place_forget()
        self.step1_destination_button.place_forget()

        # Hide step 2 objects.
        self.step2_pictureA_canvas.place_forget()
        self.accept_input_button.place_forget()
        self.text_entry_warning.place_forget()
        self.text_entryA_label.place_forget()
        self.text_entryA.place_forget()
        self.text_entryB_label.place_forget()
        self.text_entryB.place_forget()

        # Hide step 3 objects.
        self.step3_pictureA_canvas.place_forget()

        # Hide step 4 objects.
        self.step4_pictureA_canvas.place_forget()

        # Displays the title screen objects.
        self.main_title.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        self.start_measuring_button.place(relx = .35, rely = .3, anchor = CENTER)
        self.skip_measuring_button.place(relx = .6, rely = .3, anchor = CENTER)


    # Function for start_measuring_button.
    def start_measuring_button_handler(self) -> None:
        """Creates a confirmation & warning message before continuing. Called from title screen only"""
        # Hide start_measuring & skip_measuring button.
        self.start_measuring_button.place_forget()
        self.skip_measuring_button.place_forget()

        # Display message & confirmation buttons.
        self.start_measuring_warning.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        self.confirm_continue_button.place(relx = 0.45, rely = 0.38, anchor = CENTER)
        self.confirm_exit_button.place(relx = 0.55, rely = 0.38, anchor = CENTER)
    
    # Function for the return_title_button.
    def confirm_title_return(self) -> None:
        """Creates a confirmation message before returning to title screen. Called from exit button only"""
        # Hide return button.
        self.return_title_button.place_forget()

        # Display confirmation message & buttons.
        self.confirm_return_warning.place(relx = 0.1, rely = 0.04, anchor = CENTER)
        self.confirm_return_yes.place(relx = 0.08, rely = 0.09, anchor = CENTER)
        self.confirm_return_no.place(relx = 0.12, rely = 0.09, anchor = CENTER)

    # Function for cancelling returning to title.
    def cancel_return(self) -> None:
        """Return the exit button to its original state."""
        # Hide confirmation message & buttons.
        self.confirm_return_warning.place_forget()
        self.confirm_return_yes.place_forget()
        self.confirm_return_no.place_forget()

        # Display return button.
        self.return_title_button.place(relx = 0.1, rely = 0.04, anchor = CENTER)

    # Fucntion for going to the next step in the process.
    def next_step(self) -> None:
        """Checks current step and calls the appropriate step function to move forward"""
        if self.current_step == 1:
            self.step2_screen()
            self.back_button.config(state = NORMAL)
        elif self.current_step == 2:
            self.step3_screen()
        elif self.current_step == 3:
            self.step4_screen()
        # TODO: CONTINUE ADDING ELIFS AS MORE STEPS ARE IMPLEMENTED

        # Only allow the next button to be clicked again if input has completed for the current step.
        if self.current_progress >= self.current_step:
            self.continue_button.config(state = NORMAL)
        else:
            self.continue_button.config(state = DISABLED)


    # Function for going back to the previous step in the process.
    def previous_step(self) -> None:
        """Checks current step and calls the appropriate step function to move back"""
        # If current_step is 2, disable the previous step button on moving into step 1.
        if self.current_step == 2:
            self.step1_screen()
            self.back_button.config(state = DISABLED)
        elif self.current_step == 3:
            self.step2_screen()
        elif self.current_step == 4:
            self.step3_screen()
        # TODO: CONTINUE ADDING ELIFS AS MORE STEPS ARE IMPLEMENTED

        # Allow the next button to be clicked again if input has completed for the current step.
        if self.current_progress >= self.current_step:
            self.continue_button.config(state = NORMAL)
        else:
            self.continue_button.config(state = DISABLED)
    
    # Function for displaying step 1.
    def step1_screen(self) -> None:
        """Displays information for step 1 of creating a JSON config file. Called from confirmation screen or step 2"""
        # Hide confirmation screen and title objects.
        self.start_measuring_warning.place_forget()
        self.confirm_continue_button.place_forget()
        self.confirm_exit_button.place_forget()
        self.main_title.place_forget()

        # Hide step 2 objects.
        self.step2_pictureA_canvas.place_forget()
        self.accept_input_button.place_forget()
        self.text_entry_warning.place_forget()
        self.text_entryA_label.place_forget()
        self.text_entryA.place_forget()
        self.text_entryB_label.place_forget()
        self.text_entryB.place_forget()

        self.current_step = 1

        # Display step 1 information (source tray or destination tray?), the exit button, and the continue/back buttons.
        self.tray_measurements.info_label.place_forget()
        self.tray_measurements.update_info()
        self.return_title_button.place(relx = 0.1, rely = 0.04, anchor = CENTER)
        self.step_title.config(text = "Step 1 of 7\n\nSpecify tray type",
                                 font = ("Arial", 15),
                                 bg = 'light green')
        self.step_title.place(relx = 0.5, rely = 0.05, anchor = CENTER)
        self.step_instructions.config(text = "Indicate whether the information being entered is "
                                             "for the source (dense) tray or the destination (sparse) tray.",
                                      font = ("Arial", 15),
                                      bg = 'light green')
        self.step_instructions.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.step1_source_button.place(relx = 0.45, rely = 0.2, anchor = CENTER)
        self.step1_destination_button.place(relx = 0.55, rely = 0.2, anchor = CENTER)
        self.continue_button.config(state = DISABLED)
        self.continue_button.place(relx = 0.65, rely = 0.02, anchor = CENTER)
        self.back_button.config(state = DISABLED)
        self.back_button.place(relx = 0.35, rely = 0.02, anchor = CENTER)

    # Function for pressing the "Source" button in step 1.
    def step1_source(self) -> None:
        """Sets the tray type stored to 'Source'"""
        self.tray_measurements.tray_name = "Source"
        self.tray_measurements.info_label.place_forget()
        self.tray_measurements.update_info()

        # Update input progress and make the next button available.
        if self.current_progress < 1:
            self.current_progress = 1
            self.continue_button.config(state = NORMAL)

    # Function for pressing the "Destination" button in step 1.
    def step1_destination(self) -> None:
        """Sets the tray type stored to 'Destination'"""
        self.tray_measurements.tray_name = "Destination"
        self.tray_measurements.info_label.place_forget()
        self.tray_measurements.update_info()

        # Update input progress and make the next button available.
        if self.current_progress < 1:
            self.current_progress = 1
            self.continue_button.config(state = NORMAL)

    # Function for displaying step 2.
    def step2_screen(self) -> None:
        """Displays information for step 2. Called from step 1 & 3 screens"""

        self.tray_measurements.hide_label()
        self.tray_measurements.update_info()

        self.current_step = 2

        # Hide/modify step 1 and step 3 objects.
        self.step_title.config(text = "Step 2 of 7\n\nTray hole dimensions",
                            font = ("Arial", 15),
                            bg = 'light green')
        self.step_instructions.config(text = "Enter (in mm) the length and width of one of the tray holes.\n"
                                             "Note that the length side is defined as the side parallel "
                                             "to the long side of the tray.",
                                      font = ("Arial", 15),
                                      bg = 'light green')
        self.step1_source_button.place_forget()
        self.step1_destination_button.place_forget()
        # TODO: Step 3 objects need to be hidden
        self.step3_pictureA_canvas.place_forget()

        # NOTE TO SELF: (0,0) on the canvas is the upper left corner
        self.step2_pictureA_canvas.place(relx = 0.3, rely = 0.6, anchor=CENTER)
        self.step2_pictureA_canvas.create_image(275, 275, anchor=CENTER, image=self.step2_pictureA)
        # Add related step 2 objects
        self.text_entry_warning.place(relx = 0.9, rely = 0.55, anchor = CENTER)
        self.text_entryA.place(relx = 0.9, rely = 0.6, anchor = CENTER)
        self.text_entryB.place(relx = 0.9, rely = 0.65, anchor = CENTER)
        self.text_entryA_label.config(text = "Length:",
                                        font = ("Arial", 12),
                                        bg = 'light green')
        self.text_entryB_label.config(text = " Width:",
                                        font = ("Arial", 12),
                                        bg = 'light green')
        self.text_entryA_label.place(relx = 0.8, rely = 0.6, anchor = CENTER)
        self.text_entryB_label.place(relx = 0.8, rely = 0.65, anchor = CENTER)
        self.accept_input_button.place(relx = 0.9, rely = 0.7, anchor = CENTER)

    # Function for accepting input from the two text boxes present in step 2 beyond.
    def accept_input(self) -> None:
        """Confirms the input in each text box is a number before storing it in the tray_info class object based on current step"""
        # TODO potato.replace(".","",1).isdigit()
        # Get input from each box, then clear it.
        inputA = ""
        inputB = ""
        inputA += self.text_entryA.get()
        inputB += self.text_entryB.get()
        self.text_entryA.delete(0, END)
        self.text_entryB.delete(0, END)

        # Is the entry valid? This depends on the step.
        # Steps 2-4 can have decimal input
        # Step 5 can only have whole numbers
        # Step 6 can have decimals for input B, but not input A
        # If invalid input is detected, return without updating any information.
        if self.current_step <= 4 and self.current_step >= 2:
            if not inputA.replace(".","",1).isdigit() or not inputB.replace(".","",1).isdigit():
                return
        elif self.current_step == 5:
            if not inputA.isdigit() or not inputB.isdigit():
                return
        elif self.current_step == 6:
            if not inputA.isdigit() or not inputB.replace(".","",1).isdigit():
                return

        # If input is unreasonably large, also discard.
        if float(inputA) > 1000 or float(inputB) > 1000:
            return
        
        # If code reached here, input is valid. Enter info into relevant tray_info object.
        if self.current_step == 2:
            self.tray_measurements.hole_length = float(inputA)
            self.tray_measurements.hole_width = float(inputB)
        elif self.current_step == 3:
            self.tray_measurements.short_axis_distance = float(inputA)
            self.tray_measurements.long_axis_distance = float(inputB)
        elif self.current_step == 4:
            self.tray_measurements.short_axis_distance_to_edge = float(inputA)
            self.tray_measurements.long_axis_distance_to_edge = float(inputB)
        elif self.current_step == 5:
            self.tray_measurements.rows = int(inputA)
            self.tray_measurements.columns = int(inputB)
        elif self.current_step == 6:
            self.tray_measurements.rows_between_gap = int(inputA)
            self.tray_measurements.extra_gap = float(inputB)

        # Update the tray info displayed.
        self.tray_measurements.update_info()

        # Update input progress and make the next button available, if applicable.
        if self.current_progress < self.current_step:
            self.current_progress = self.current_step
            self.continue_button.config(state = NORMAL)

    # Function for displaying step 3.
    def step3_screen(self):
        """Displays information for step 3. Called from step 2 & 4 screens"""

        self.tray_measurements.hide_label()
        self.tray_measurements.update_info()

        self.current_step = 3

        # Hide/modify step 2 and 4 objects.
        self.step2_pictureA_canvas.place_forget()

        # Hide step 4 objects.
        self.step4_pictureA_canvas.place_forget()

        # Modify/add objects for step 3.
        self.step_title.config(text = "Step 3 of 7\n\nTray hole spaces",
                            font = ("Arial", 15),
                            bg = 'light green')
        self.step_instructions.config(text = "Enter (in mm) the distance between each of the tray holes.\n"
                                             "Identify each axis based on which side of the tray it is parallel to.",
                                      font = ("Arial", 15),
                                      bg = 'light green')
        self.text_entryA_label.config(text = "Short axis distance:")
        self.text_entryA_label.place_forget()
        self.text_entryA_label.place(relx = 0.75, rely = 0.6, anchor = CENTER)
        self.text_entryB_label.config(text = " Long axis distance:")
        self.text_entryB_label.place_forget()
        self.text_entryB_label.place(relx = 0.75, rely = 0.65, anchor = CENTER)

        self.step3_pictureA_canvas.place(relx = 0.3, rely = 0.6, anchor=CENTER)
        self.step3_pictureA_canvas.create_image(252, 189, anchor=CENTER, image=self.step3_pictureA)

    # Function for display step 4.
    def step4_screen(self):
        """Displays information for step 4. Called from step 3 & 5 screens"""

        self.tray_measurements.hide_label()
        self.tray_measurements.update_info()

        self.current_step = 4

        # Hide/modify step 3 and 5 objects.
        self.step3_pictureA_canvas.place_forget()

        # Hide step 5 objects.
        # TODO

        # Modify/add objects for step 4.
        self.step_title.config(text = "Step 4 of 7\n\nDistance to tray edge",
                            font = ("Arial", 15),
                            bg = 'light green')
        self.step_instructions.config(text = "Enter (in mm) the distance from the outer tray holes to the tray edges.\n"
                                             "Identify each axis based on which side of the tray it is parallel to.",
                                      font = ("Arial", 15),
                                      bg = 'light green')
        self.text_entryA_label.config(text = "Short axis distance to edge:")
        self.text_entryA_label.place_forget()
        self.text_entryA_label.place(relx = 0.73, rely = 0.6, anchor = CENTER)
        self.text_entryB_label.config(text = " Long axis distance to edge:")
        self.text_entryB_label.place_forget()
        self.text_entryB_label.place(relx = 0.73, rely = 0.65, anchor = CENTER)

        self.step4_pictureA_canvas.place(relx = 0.3, rely = 0.6, anchor=CENTER)
        self.step4_pictureA_canvas.create_image(252, 189, anchor=CENTER, image=self.step4_pictureA)
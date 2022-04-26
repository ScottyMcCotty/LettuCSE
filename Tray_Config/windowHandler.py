"""Module contains the GUI class"""

from tkinter import N, Tk, Label, PhotoImage, CENTER, NORMAL, Button
from trayInfo import trayInfo

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
    trayMeasurements = trayInfo()

    window = None
    
    # The buttons.
    start_measuring_button = None
    skip_measuring_button = None

    start_measuring_warning = None
    confirm_continue_button = None
    confirm_exit_button = None

    return_title_button = None
    confirm_return_warning = None
    confirm_return_yes = None
    confirm_return_no = None

    step1_source_button = None
    step1_destination_button = None

    # The labels.
    main_title = None
    step1_title = None
    step1_instructions = None


    def __init__(self, tkinter_object:Tk) -> None:
        self.window = tkinter_object
        self.window.title("LettuCSE Transplanter")
        self.window.geometry("1000x800")
        self.window.configure(bg = 'light green')

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
                                              state=NORMAL)
        self.confirm_exit_button = Button(self.window,
                                              text = "Go back",
                                              font = ("Arial", 10),
                                              command = self.title_screen,
                                              state=NORMAL)

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

        # STEP 1 SCREEN (source or destination tray?)  
        self.step1_title = Label(text = "Step 1 of X\n\nSpecify tray type",
                                 font = ("Arial", 15),
                                 bg = 'light green')
        self.step1_instructions = Label(text = "Indicate whether the information being entered is "
                                               "for the source (dense) tray or the destination (sparse) tray.",
                                        font = ("Arial", 15),
                                        bg = 'light green')
        self.step1_source_button = Button(self.window,
                                          text = "Source tray",
                                          command = self.step2_screen("Source"),
                                          state = NORMAL)
        self.step1_destination_button = Button(self.window,
                                               text = "Destination tray",
                                               command = self.step2_screen("Destination"),
                                               state = NORMAL)                          
                                              
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
        # INPROGRESS
        self.start_measuring_warning.place_forget()
        self.confirm_continue_button.place_forget()
        self.confirm_exit_button.place_forget()

        # Hide confirmation of return objects.
        self.confirm_return_warning.place_forget()
        self.confirm_return_yes.place_forget()
        self.confirm_return_no.place_forget()

        # Hide step 1 objects.
        self.step1_title.place_forget()
        self.step1_instructions.place_forget()
        self.step1_source_button.place_forget()
        self.step1_destination_button.place_forget()

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
    
    # Function for confirm_continue_button.
    def step1_screen(self) -> None:
        """Displays information for step 1 of creating a JSON config file. Called from confirmation screen only"""
        # Hide confirmation screen and title objects.
        self.start_measuring_warning.place_forget()
        self.confirm_continue_button.place_forget()
        self.confirm_exit_button.place_forget()
        self.main_title.place_forget()

        # Display step 1 information (source tray or destination tray?) and the exit button.
        self.return_title_button.place(relx = 0.1, rely = 0.04, anchor = CENTER)
        self.step1_title.place(relx = 0.5, rely = 0.05, anchor = CENTER)
        self.step1_instructions.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.step1_source_button.place(relx = 0.45, rely = 0.2, anchor = CENTER)
        self.step1_destination_button.place(relx = 0.55, rely = 0.2, anchor = CENTER)

    def step2_screen(self, trayType) -> None:
        """Stores answer from step 1 and displays information for step 2. Called from step 1 screen only"""
        # Handle logic from previous step before continuing.
        if trayType == "Source":
            self.trayMeasurements.tray_name = "custom_dense_tray_measurements.json"
        elif trayType == "Destination":
            self.trayMeasurements.tray_name = "custom_sparse_tray_measurements.json"

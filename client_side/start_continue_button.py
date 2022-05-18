"""Module contains the Transplanter class"""

import threading
from tkinter import N, Button, PhotoImage

class StartContinueButton():
    """
    This class creates a tkinter button object that swaps between a start button and a
    continue button
    ...

    Attributes
    ----------
    tkinter_instance : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    tkinter_button : Tkinter.Button
        The button object that is placed in a location on the window and changed
    transplanter_function : function
        This runs the transplanting proccess and must be called in another thread
    is_transplanting : bool
        Records whether the transplanting is in progress or not

    Methods
    ----------

    start_transplanting_thread()
        Firstly, set the button so that it is disabled so it can't be repressed.
        Secondly, run the transplanting function in another thread.
    set_to_pause_mode()
        Make it so that the button continues transplanting from where it left off
        rather than restart it. Also changes the button's image to show the user that
        this is true.
    set_to_stopped_mode()
        Reset the button so it's like it is after the button
        is initialized
    __continue_transplanting()
        a private function that is called
        when the user presses the continue button.
        this is called when the button is set to
        paused, and then pressed.
    """
    tkinter_instance = None
    tkinter_button = None
    transplanter_function = None
    continue_transplant = None
    is_transplanting = False

    def __init__(self, tkinter_instance, transplanter_function, continue_transplant) -> None:
        self.transplanter_function = transplanter_function
        self.continue_transplant = continue_transplant

        start_button_photo = PhotoImage(file='images/start_button.png')
        self.tkinter_button = Button(tkinter_instance,
                                     command=self.start_transplanting_thread,
                                     borderwidth=0,
                                     state='normal',
                                     image = start_button_photo)
        self.tkinter_button.image = start_button_photo
        self.tkinter_button.place(relx = 0.5, rely = 0.3, anchor = N)



    def start_transplanting_thread(self):
        """Make the button disabled, so you can't re-press it when it's transplanting already"""
        self.is_transplanting = True
        self.tkinter_button["state"] = "disabled"
        threading.Thread(target=self.transplanter_function).start()

    def set_to_pause_mode(self):
        """Set the button to it's 'continue' mode,
         so that the user can press it after they have replaced the trays"""
        paused_photo = PhotoImage(file='images/pause_button.png')
        self.tkinter_button.config(image=paused_photo,
                                   state="normal",
                                   command=self.__continue_transplanting)
        self.tkinter_button.image = paused_photo
        self.tkinter_button.place(relx = 0.5, rely = 0.3, anchor = N)

    def set_to_stopped_mode(self):
        """Reset the button so it can start again"""
        if self.is_transplanting:
            self.is_transplanting = False
            start_button = PhotoImage(file='images/start_button.png')
            self.tkinter_button.config(image=start_button,
                                       state="normal",
                                       command = self.start_transplanting_thread)
            self.tkinter_button.image = start_button


    def __continue_transplanting(self):
        """Make the button disabled, so you can't re-press it when it's transplanting already,
        and continue the transplanting process"""
        in_progress = PhotoImage(file='images/in_progress.png')
        self.tkinter_button.config(image=in_progress,
                                   state="disabled",
                                   command = lambda:self.start_transplanting_thread)
        self.tkinter_button.image = in_progress
        self.continue_transplant()

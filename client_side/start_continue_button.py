"""Module contains the Transplanter class"""

import threading
from tkinter import DISABLED, N, NORMAL, Button

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

    set_to_transplanting()
        Firstly, set the button so that it is disabled so it can't be repressed.
        Secondly, run the transplanting function in another thread.
    set_to_paused()
        Make it so that the button continues transplanting from where it left off
        rather than restart it. Also changes the button's image to show the user that
        this is true.
    set_to_stopped()
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

        self.tkinter_button = Button(tkinter_instance,
                                     text ="Start Transplant",
                                     command=self.set_to_transplanting,
                                     bd=0,
                                     state=NORMAL)
        self.tkinter_button.place(relx = 0.5, rely = 0.4, anchor = N)



    def set_to_transplanting(self):
        """Make the button disabled, so you can't re-press it when it's transplanting already"""
        self.tkinter_button["state"] = "disabled"
        self.is_transplanting = True
        threading.Thread(target=self.transplanter_function).start()

    def set_to_paused(self):
        """Set the button to it's 'continue' mode,
         so that the user can press it after they have replaced the trays"""
        self.tkinter_button = Button(self.tkinter_instance,
                                     text ="Press to Continue after Trays have been Replaced",
                                     command=self.__continue_transplanting,
                                     bd=0,
                                     state=NORMAL)

    def set_to_stopped(self):
        """Reset the button so it can start again"""
        self.tkinter_button = Button(self.tkinter_instance,
                                     text ="Start Transplant",
                                     command=self.set_to_transplanting,
                                     bd=0,
                                     state=NORMAL)

    def __continue_transplanting(self):
        """Make the button disabled, so you can't re-press it when it's transplanting already,
        and continue the transplanting process"""
        self.tkinter_button = Button(self.tkinter_instance,
                                     text ="Transplanting in Progress",
                                     bd=0,
                                     state=DISABLED)
        self.continue_transplant()

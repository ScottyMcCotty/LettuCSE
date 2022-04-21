"""Module contains the Transplanter class"""

import threading
from tkinter import DISABLED, NORMAL, Button

class StartContinueButton():
    """
    This class creates a tkinter button object that swaps between a start button and a
    continue button
    ...

    Attributes
    ----------
    tkinter_object : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    tkinter_button : Tkinter.Button
        The button object that is placed in a location on the window and changed
    transplanter_function : function
        This runs the transplanting proccess and must be called in another thread

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
    
    

    """
    tkinter_instance = None
    tkinter_button = None
    transplanter_function = None
    continue_transplant = None

    def __init__(self, tkinter_instance, transplanter_function, continue_transplant) -> None:
        self.transplanter_function = transplanter_function
        self.continue_transplant = continue_transplant

        self.tkinter_button = Button(tkinter_instance,
                                     text ="Start Transplant",
                                     command=lambda:self.set_to_transplanting,
                                     bd=0,
                                     state=NORMAL)


    def set_to_transplanting(self):
        """Make the button disabled, so you can't re-press it when it's transplanting already"""
        self.tkinter_button = Button(self.tkinter_instance,
                                     text ="Transplanting in Progress",
                                     bd=0,
                                     state=DISABLED)
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
                                     command=lambda:self.set_to_transplanting,
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

"""Module contains the Transplanter class"""

from tkinter import DISABLED, N, NORMAL, Button, PhotoImage

class StopButton():
    """
    This class creates a tkinter button object that stops the whole process
    ...

    Attributes
    ----------
    tkinter_instance : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    tkinter_button : Tkinter.Button
        The button object that is placed in a location on the window and changed
    stop_function : function
        This runs the stops the transplanting procecss
    is_enabled : boolean
        whether the stop button is pressable
        at the moment

    Methods
    ----------

    enable_button()
        enable the stop button because the transplanting has started
    disable_button()
        disable the stop button because the transplanting is over
        and you don't want to allow the user to press the stop button
        twice
    """
    tkinter_instance = None
    tkinter_button = None
    stop_function = None
    is_enabled = False
    stopped_flag = False

    def __init__(self, tkinter_instance, stop_function) -> None:
        self.stop_function = stop_function
        stop_button_photo = PhotoImage(file='images/stop_button.png')
        self.tkinter_button = Button(tkinter_instance,
                                     image =stop_button_photo,
                                     command=self.stop,
                                     bd=0,
                                     state=DISABLED)
        self.tkinter_button.image=stop_button_photo
        self.tkinter_button.place(relx = 0.5, rely = 0.4, anchor = N)

    def stop(self):
        """reset everything"""
        self.stopped_flag = True
        self.stop_function()
        self.tkinter_button["state"] = "disabled"
        self.is_enabled = False

    def enable_button(self):
        """Enable button, this is called when the transplanting has started"""
        self.tkinter_button["state"] = "normal"
        self.stopped_flag = False
        self.is_enabled = True

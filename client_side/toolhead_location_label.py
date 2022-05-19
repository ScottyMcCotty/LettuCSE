"""Module contains the toolhead location label class"""

from tkinter import N, Label
from tkinter import font

class ToolheadLocationLabel():
    """
    This class creates a tkinter label object which diplays the motor coordinates
    (coordinates in terms of motor steps) and is updated in real time
    ...

    Attributes
    ----------
    tkinter_instance : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    label_instance : Tkinter.Label
        The button object that is placed in a location on the window and changed

    Methods
    ----------

    update_location()
        when the toolhead is somewhere else, change the label
    """
    tkinter_instance = None
    label_instance = None

    def __init__(self, tkinter_instance) -> None:
        self.tkinter_instance = tkinter_instance
        my_font = font.Font(family='Helvetica', size = 10, weight = 'bold', slant = 'roman', underline = 0, overstrike = 0)
        font.families()
        self.label_instance = Label(tkinter_instance,
                                    text = "(0,0)",
                                    bg = "#AFD275",
                                    bd = 0,
                                    fg = "black",
                                    font = my_font)
        self.label_instance.place(relx = 0.5, rely = 0.765, anchor = N)

    def update_location(self, coords:tuple):
        """change the text on the label to reflect new location"""
        self.label_instance['text'] = "Destination of Toolhead in motor coordinates " + str(coords)

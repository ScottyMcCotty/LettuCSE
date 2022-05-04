"""Module contains the toolhead location label class"""

from tkinter import N, Label

class ToolheadLocationLabel():
    """
    This class creates a tkinter button object that swaps between a start button and a
    continue button
    ...

    Attributes
    ----------
    tkinter_instance : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    label_instance : Tkinter.Label
        The button object that is placed in a location on the window and changed
    toolhead_location : tuple
        The location coords to be displayed

    Methods
    ----------

    update_location()
        when the toolhead is somewhere else, change the label
    """
    tkinter_instance = None
    label_instance = None

    def __init__(self, tkinter_instance) -> None:
        self.tkinter_instance = tkinter_instance
        self.label_instance = Label(tkinter_instance,
                                    text = "(0,0)",
                                    bg = "green",
                                    bd = 0,
                                    fg = "white")
        self.label_instance.place(relx = 0.5, rely = 0.5, anchor = N)

    def update_location(self, coords:tuple):
        """change the text on the label to reflect new location"""
        self.label_instance['text'] = coords

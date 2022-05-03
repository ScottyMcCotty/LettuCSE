"""Module contains the Transplanter class"""

import tkinter as tk
import turtle as t

class ToolheadIllustrator():
    """
    This class creates a tkinter button object that swaps between a start button and a
    continue button
    ...

    Attributes
    ----------
    tkinter_object : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    toolhead_image
    canvas
    source_tray_rectangle_image
    destination_tray_rectangle_image
 
    Methods
    ----------

    update_location()
        when the toolhead is somewhere else, change the label
    """
    tkinter_instance = None
    label_instance = None
    turtle = None
    source_tray_box = None
    destination_tray_box = None

    def __init__(self, tkinter_instance) -> None:
        canvas = tk.Canvas(master = tkinter_instance, width = 315, height = 215)
        canvas.place(relx = 0.5, rely = 0.55, anchor = tk.N)
        self.turtle = t.RawTurtle(canvas)
        canvas.create_rectangle(150, 100, 10, -100, fill='white')
        canvas.create_rectangle(-10, 100, -150, -100, fill='white')
        self.turtle.shape("circle")
        self.turtle.pencolor("#000000")
        self.turtle.shapesize(0.5, 0.5, 1)
        self.turtle.penup()



    def update_location(self, coords:tuple):
        """change the text on the label to reflect new location"""
        self.turtle.goto(coords[0]/100-140, coords[1]/100-90)

"""Module contains the Toolhead Illustrator class"""

import tkinter as tk
import turtle as t

class ToolheadIllustrator():
    """
    This class creates a tkinter button object that swaps between a start button and a
    continue button
    ...

    Attributes
    ----------
    tkinter_instance : Tkinter.Tk()
        The tkinter object that is being fed into all objects on the window
    toolhead_image : turtle
        A python 'turtle', which is configured so that it appears as a circle.
        It will move in accordance with how the toolhead moves
        https://docs.python.org/3/library/turtle.html
    canvas : turtle canvas
        A 'canvas' object which comes with the turtle package. It provides a white
        rectangle on which the turtle object is allowed to move
    source_tray_box: turtle rectangle
        A rectangle image drawn by the 'turtle' during initialization (although it's
        too fast to see it be drawn so just think of it as a black rectangle on the canvas).
        It shows roughly where the toolhead is in relation to the source tray
    destination_tray_box: turtle rectangle
        A rectangle image drawn by the 'turtle' during initialization (although
        it's too fast to see it be drawn so just think of it as a black rectangle on the canvas).
        It shows roughly where the toolhead is in relation to the destination tray
 
    Methods
    ----------

    update_location()
        when the toolhead is somewhere else, move the turtle object to that location on the canvas
    """
    tkinter_instance = None
    label_instance = None
    turtle = None
    source_tray_box = None
    destination_tray_box = None

    def __init__(self, tkinter_instance) -> None:
        canvas = tk.Canvas(master = tkinter_instance, width = 340, height = 230)
        canvas.place(relx = 0.5, rely = 0.55, anchor = tk.N)
        self.turtle = t.RawTurtle(canvas)
        canvas.create_rectangle(160, 100, 5, -100, fill='white')
        canvas.create_rectangle(-5, 100, -160, -100, fill='white')
        self.turtle.shape("circle")
        self.turtle.pencolor("#000000")
        self.turtle.shapesize(0.5, 0.5, 1)
        self.turtle.penup()



    def update_location(self, coords:tuple):
        """
        When the toolhead is somewhere else, move the turtle object to that location on the canvas
        The coordinates are modified to fit on the canvas
        """
        self.turtle.goto(coords[0]/32-150, coords[1]/40-90)

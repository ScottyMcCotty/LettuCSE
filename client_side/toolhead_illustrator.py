"""Module contains the Toolhead Illustrator class"""

import tkinter as tk
import turtle as t

class ToolheadIllustrator():
    """
    This class creates a canvas that shows in which hole the toolhead is supposed to be at a given time
    this is partually for debugging purposes and also because it might increase our grade
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
        """First, create canvas object because this can be placed on the
            tkinter object. Then, create a screen object from the canvas
            object because it can be edited in greater detail than the
            canvas object (ie: it can change color). Then, make two rectangles
            to represent the trays and give them both grids"""
        canvas = tk.Canvas(master = tkinter_instance, width = 750, height = 425)
        canvas.place(relx = 0.5, rely = 0.22, anchor = tk.N)

        screen = t.TurtleScreen(canvas)
        screen.bgcolor("#C2CAD0")

        self.turtle = t.RawTurtle(screen, shape='circle')
        canvas.create_rectangle(360, 200, 5, -200, fill='#C2CAD0')

        for source_tray_width_line in range(0, 11):
            x_location = source_tray_width_line*30+30
            canvas.create_line(x_location, 200, x_location, -200)

        canvas.create_rectangle(-5, 200, -360, -200, fill='#C2CAD0')

        for destination_tray_width_line in range(0, 5):
            x_location = destination_tray_width_line*60-305
            canvas.create_line(x_location, 200, x_location, -200)

        self.turtle.shapesize(0.5, 0.5, 1)
        self.turtle.penup()



    def update_location(self, coords:tuple):
        """
        When the toolhead is somewhere else, move the turtle object to that location on the canvas
        The coordinates are modified to fit on the canvas, and the x axis is flipped to reflect the 
        appearance of the transplanter when you are looking at it
        """
        self.turtle.goto(347-(coords[0]/11.95), coords[1]/20-180)

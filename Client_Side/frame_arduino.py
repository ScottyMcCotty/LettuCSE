"""This module contains the Frame Arduino class which is a child of the Arduino class"""
import time
from arduino import Arduino
from gui import GUI

class FrameArduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm to a certain
    (x,y) location

    ...

    Attributes
    ----------
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    __init__(mm_per_motor_step, gui):
        calls the parent init, and then lists the connected port in
        the frame arduino section of the GUI
    move_toolhead(coords):
        moves the arm to the given coordinates, where a tray hole should be found
    """


    serial_number = 42069

    def __init__(self, mm_per_motor_step:int, gui:GUI):
        '''
            Initialize the arduino and then list the name of the port connected to the
            arduino in the toolhead port label on the gui

            Parameters:
                    mm_per_motor_step : int
                        the number of milimeters the arm will move during each motor step
                    gui (GUI): the tkinter window object that everything is displayed on
            Returns:
                    None
        '''
        super().__init__(mm_per_motor_step, gui)
        if self.arduino_connection is None:
            gui.frame_arduino_label("Arduino not connected")
        else:
            gui.frame_arduino_label(self.arduino_port)
            super().wake_up()

    def move_toolhead(self, coords):

        '''
            Moves the arm to the given coordinates

            Parameters:
                    coords : tuple(int)
                        the x and y location that the arm is
                        intending to move to, in milimeters
            Returns:
                    None
        '''
        x_coord = round(coords[0]/self.mm_per_motor_step)
        y_coord = round(coords[1]/self.mm_per_motor_step)

        self.gui.update_status("Toolhead moving to (" + str(x_coord) + ", " + str(y_coord) + ")")

        if self.arduino_connection:
            self.arduino_connection.write(bytes(str(x_coord) + " " + str(y_coord), 'utf-8'))
            while (True):
                value = self.arduino_connection.readline().decode("utf-8")
                #TODO: Should there be the possibility of sending something back other than 
                if "Done" in value:
                    break
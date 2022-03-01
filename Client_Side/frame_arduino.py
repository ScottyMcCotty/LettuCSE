"""This module contains the Frame Arduino class which is a child of the Arduino class"""
import time
from arduino import Arduino

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
    __init__(mm_per_motor_step):
        calls the parent init, and then lists the connected port in
        the frame arduino section of the GUI
    move_toolhead(coords):
        moves the arm to the given coordinates, where a tray hole should be found
    """


    serial_number = 55838343733351510170
    port = "Arduino not connected"
    status = ""

    def __init__(self, mm_per_motor_step:int):
        '''
            Initialize the arduino and then list the name of the port connected to the
            arduino in the toolhead port label on the gui

            Parameters:
                    mm_per_motor_step : int
                        the number of milimeters the arm will move during each motor step
            Returns:
                    None
        '''
        super().__init__(mm_per_motor_step)
        if self.arduino_connection is not None:
            self.port_label = self.port
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

        if self.arduino_connection:
            self.arduino_connection.write(bytes(str(x_coord) + " " + str(y_coord), 'utf-8'))
            self.arduino_connection.readline()

        self.status = (x_coord, y_coord)

        #make it so that rather than sleep you wait for a response
        time.sleep(0.5)

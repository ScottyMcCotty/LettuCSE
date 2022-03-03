"""This module contains the Frame Arduino class which is a child of the Arduino class"""
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
    port_name = "Arduino not connected"
    status = ""

    def __init__(self):
        '''
            Initialize the arduino and then list the name of the port connected to the
            arduino in the toolhead port label on the gui

            Parameters:
                    None
            Returns:
                    None
        '''
        super().__init__()
        if self.arduino_connection is not None:
            super().wake_up()

    def move_toolhead(self, coords):

        '''
            Moves the arm to the given coordinates

            Parameters:
                    coords : tuple(int)
                        the 2D coords that the arm is
                        intending to move to, in milimeters
            Returns:
                    None
        '''
        x_coord = round(coords[0]/self.mm_per_motor_step)
        y_coord = round(coords[1]/self.mm_per_motor_step)
        super().send_string_to_arduino(str(x_coord) + " " +str(y_coord))
        self.status = (x_coord, y_coord)

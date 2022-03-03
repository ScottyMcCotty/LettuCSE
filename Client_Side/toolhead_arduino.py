"""Module contains vertical arduino class"""
from arduino import Arduino


class ToolheadArduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm up and down,
    as well as open and close the cup device which drops or grabs the plant

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step
    arduinoConnection : serial
        the connection between the program and the Arduino
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    __init__(mm_per_motor_step, gui):
        calls the parent init, and then lists the connected port in
        the toolhead arduino section of the GUI
    raise_toolhead():
        signals the arduino to raise the toolhead
    lower_toolhead():
        signals the arduino to lower the toolhead
    """


    serial_number = 42069
    status = ""

    def raise_toolhead(self):
        """Sends a '0' signal to the toolhead arduino,
        which instructs the toolhead to go up"""
        super().send_string_to_arduino(str(0))


    def lower_toolhead(self):
        """Sends a '1' signal to the toolhead arduino,
        which instructs the toolhead to go down"""
        super().send_string_to_arduino(str(1))

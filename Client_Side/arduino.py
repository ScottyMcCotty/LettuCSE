"""Module contains the arduino class"""
from arduino_error import ArduinoError
import serial
import time

class Arduino:

    """
    A parent class for the two arduinos used in the robot

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step
    arduinoConnection : serial
        the connection between the program and the Arduino

    Methods
    -------
    dummy_command():
        sends a basic fixed command to the Arduino
    __init__(mm_per_motor_step):
        initializes arduino given the ratio of milimeters to motor steps
        as well as the COM port used to communicate
    """


    mm_per_motor_step = 1
    arduinoConnection = None

    def dummy_command(self):
        raise NotImplementedError("Should be overridden by child definition")

    def __init__(self, mm_per_motor_step, comPort):
        """
        Constructs all the necessary attributes for the Arduino object and
        sends a dummy command to deal with the first command being lost.

        Parameters
        ----------
            mm_per_motor_step : int
                the number of milimeters the arm will move during each motor step
            comPort : string
                the COM port used by Arduino to connect to the computer
        """
        self.mm_per_motor_step = mm_per_motor_step

        #TODO   remove this restriction when testing with 2 Arduinos.
        #       This is only present since I can only test 1 arduino
        #       at a time, and the code won't run if it doesn't find
        #       the COM port connected
        if comPort == "COM5":
            print("Attempting to establish a connection on port '" + comPort + "'\n")
            self.arduinoConnection = serial.Serial(port=comPort, baudrate=9600, timeout=.1)
            self.dummy_command()
        

        

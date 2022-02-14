"""Module contains the arduino class"""
from arduino_error import ArduinoError

class Arduino:

    """
    A parent class for the two arduinos used in the robot

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step

    Methods
    -------
    __init__(mm_per_motor_step):
        initializes arduino given the ratio of milimeters to motor steps
    """


    mm_per_motor_step = 1
    def __init__(self, mm_per_motor_step):
        """
        Constructs all the necessary attributes for the Arduiono object.

        Parameters
        ----------
            mm_per_motor_step : int
                the number of milimeters the arm will move during each motor step
        """
        self.mm_per_motor_step = mm_per_motor_step

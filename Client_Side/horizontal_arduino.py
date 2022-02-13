from arduino_error import ArduinoError

class Horizontal_Arduino:

    """
    A class to represent the Arduino being used to move the arm.

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step

    Methods
    -------
    move_toolhead(coords):
        moves the arm to the given coordinates
    lower_toolhead():
        lowers the toolhead arm to the plant
    raise_toolhead():
        raises the toolhead arm to the plant
    release_plant():
        opens the cup-grasp and lets the plant fall
    grab_plant():
        closes the cup-grasp to hold the plant
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

    def move_toolhead(self, coords):
        """moves the arm to the given coordinates"""
        #TODO actually signal arduino    
        x = round(coords[0]*self.mm_per_motor_step)
        y = round(coords[1]*self.mm_per_motor_step)
        print("Toolhead moving to (" + str(x) + ", " + str(y) + ")")

    
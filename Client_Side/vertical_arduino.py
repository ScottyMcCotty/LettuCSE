from arduino_error import ArduinoError
from arduino import Arduino

class Vertical_Arduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm up and down, 
    as well as open and close the cup device which drops or grabs the plant

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step

    Methods
    -------
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

    def lower_toolhead(self):
        """lowers the toolhead arm to the plant"""
        #TODO actually signal arduino
        print("Toolhead lowering")

    def raise_toolhead(self):
        """raises the toolhead arm to the plant"""
        #TODO actually signal arduino
        print("Toolhead raising")

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #TODO actually signal arduino
        print("Toolhead raising")

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #TODO actually signal arduino
        print("Toolhead closing")
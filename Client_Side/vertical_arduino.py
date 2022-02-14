"""Module contains vertical arduino class"""
from arduino_error import ArduinoError
from arduino import Arduino

class VerticalArduino(Arduino):

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

    def lower_toolhead(self):
        """lowers the toolhead arm to the plant"""
        #TODO actually signal arduino
        print("Vertical toolhead lowering")

    def raise_toolhead(self):
        """raises the toolhead arm to the plant"""
        #TODO actually signal arduino
        print("Vertical toolhead raising")

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #TODO actually signal arduino
        print("Vertical toolhead opening")

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #TODO actually signal arduino
        print("Vertical toolhead closing")

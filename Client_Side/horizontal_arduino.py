from arduino_error import ArduinoError
from arduino import Arduino

class Horizontal_Arduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm to a certain
    (x,y) location

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step

    Methods
    -------
    move_toolhead(coords):
        moves the arm to the given coordinates
    """


    mm_per_motor_step = 1 

    def move_toolhead(self, coords):
        """moves the arm to the given coordinates"""
        #TODO actually signal arduino    
        x = round(coords[0]*self.mm_per_motor_step)
        y = round(coords[1]*self.mm_per_motor_step)
        print("Horizontal toolhead moving to (" + str(x) + ", " + str(y) + ")")

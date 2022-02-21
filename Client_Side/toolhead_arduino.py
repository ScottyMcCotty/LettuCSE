"""Module contains vertical arduino class"""
from arduino_error import ArduinoError
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

    Methods
    -------
    dummy_command():
        sends a basic fixed command to the Arduino
    grab_plant():
        lowers the toolhead arm to the plant and grabs it
    release_plant():
        releases the plant and raises the toolhead arm
    """


    mm_per_motor_step = 1
    arduinoConnection = None

    def dummy_command(self):
        """sends a basic fixed command to the Arduino"""
        #TODO actually signal arduino

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #TODO actually signal arduino
        print("Toolhead releasing plant")

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #TODO actually signal arduino
        print("Toolhead grabbing plant")

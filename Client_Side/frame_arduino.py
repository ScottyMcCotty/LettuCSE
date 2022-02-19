from arduino_error import ArduinoError
from arduino import Arduino

import serial
import time

class FrameArduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm to a certain
    (x,y) location

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
    move_toolhead(coords):
        moves the arm to the given coordinates
    """


    mm_per_motor_step = 1 
    arduinoConnection = None

    def dummy_command(self):
        """sends a basic fixed command to the Arduino"""
        dummyInput = "0 0"
        self.arduinoConnection.write(bytes(dummyInput, 'utf-8'))

    def move_toolhead(self, coords):
        """moves the arm to the given coordinates"""
        #TODO actually signal arduino    
        x = round(coords[0]/self.mm_per_motor_step)
        y = round(coords[1]/self.mm_per_motor_step)
        print("Horizontal toolhead moving to (" + str(x) + ", " + str(y) + ")")

        input = str(x) + " " + str(y) + "\n"

        self.arduinoConnection.write(bytes(input, 'utf-8'))

        #TODO time.sleep is needed for testing, but
        #     in an actual running environment the
        #     Arduino shouldn't receive a ton of
        #     commands each second since the arm
        #     has to move
        # time.sleep(0.05)

        # Blocking command
        while(True):
            
            value = self.arduinoConnection.readline().decode("utf-8")
            # print(f"Received from arduino: '{value}'")
            if "Done" in value:
                break


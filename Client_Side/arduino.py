import time
import random
from arduino_error import ArduinoError

class Arduino:
    mm_per_motor_step = 1 
    def __init__(self, mm_per_motor_step):
        self.mm_per_motor_step = mm_per_motor_step

    def move_toolhead(self, coords):
        #TODO actually signal arduino    
        if random.randint(0,100000) == 1:
            raise ArduinoError("Error Moving Toolhead")
        else:
            x = round(coords[0]*self.mm_per_motor_step)
            y = round(coords[1]*self.mm_per_motor_step)
            print("Toolhead moving to (" + str(x) + ", " + str(y) + ")")

    def lower_toolhead(self):
        #TODO actually signal arduino
        if random.randint(0,10) == 1:
            raise ArduinoError("Error Lowering Toolhead")
        else:
            print("Toolhead lowering")

    def raise_toolhead(self):
        #TODO actually signal arduino
        if random.randint(0,10) == 1:
            raise ArduinoError("Error Raising Toolhead")
        else:
            print("Toolhead raising")

    def release_plant(self):
        #TODO actually signal arduino
        if random.randint(0,10) == 1:
            raise ArduinoError("Error Releasing Plant")
        else:
            print("Toolhead releasing")

    def grab_plant(self):
        #TODO actually signal arduino
        if random.randint(0,10) == 1:
            raise ArduinoError("Error Grabbing Plant")
        else:
            print("Toolhead closing")
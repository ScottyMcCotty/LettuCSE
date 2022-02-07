from arduino_error import ArduinoError

class Arduino:
    mm_per_motor_step = 1 
    def __init__(self, mm_per_motor_step):
        self.mm_per_motor_step = mm_per_motor_step

    def move_toolhead(self, coords):
        #TODO actually signal arduino    
        x = round(coords[0]*self.mm_per_motor_step)
        y = round(coords[1]*self.mm_per_motor_step)
        print("Toolhead moving to (" + str(x) + ", " + str(y) + ")")

    def lower_toolhead(self):
        #TODO actually signal arduino
        print("Toolhead lowering")

    def raise_toolhead(self):
        #TODO actually signal arduino
        print("Toolhead raising")

    def release_plant(self):
        #TODO actually signal arduino
        print("Toolhead raising")

    def grab_plant(self):
        #TODO actually signal arduino
        print("Toolhead closing")
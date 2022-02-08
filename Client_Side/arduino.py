from arduino_error import ArduinoError

# Necessary imports for the Arduino to work (Liam)
import serial
import time

class Arduino:
    mm_per_motor_step = 1
    arduinoConnection = None
    def __init__(self, mm_per_motor_step, comPort):
        self.mm_per_motor_step = mm_per_motor_step
        # Attempt to connect to the Arduino using provided COM port (Liam)
        print("Attempting to establish a connection on port '" + comPort + "'\n")
        self.arduinoConnection = serial.Serial(port=comPort, baudrate=9600, timeout=.1)
        # NOTE: Arduino seems to ignore the first pair of coordinates it is sent.
        #       Followup commands work normally. Consider sending a dummy (0, 0)
        #       write here on initialization? (Liam)
        dummyInput = "0 0"
        if dummyInput[-1] != '\n':
            dummyInput += '\n'
        self.arduinoConnection.write(bytes(dummyInput, 'utf-8'))

    def move_toolhead(self, coords):
        x = round(coords[0]*self.mm_per_motor_step)
        y = round(coords[1]*self.mm_per_motor_step)
        print("Toolhead moving to (" + str(x) + ", " + str(y) + ")")

        # Put coordinates into "X Y" format expected by arduino (Liam)
        # NOTE: This is assuming coords[] is in motor steps, not mm
        input = str(coords[0]) + " " + str(coords[1])
        
        # If the final char isn't a newline, add one (Liam)
        if input[-1] != '\n':
            input += '\n'
        self.arduinoConnection.write(bytes(input, 'utf-8'))
        # NOTE: Unsure if this sleep & readline are needed. They may cause problems (Liam)
        # Comment from Scott's example code: "We may need to write and immediately read
        #                                     a response, depending on the application"
        time.sleep(0.05)
        value = self.arduinoConnection.readline()



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
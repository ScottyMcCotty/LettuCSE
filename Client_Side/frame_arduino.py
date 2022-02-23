"""This module contains the Frame Arduino class which is a child of the Arduino class"""
import time
import serial as s
from arduino import Arduino


from gui import GUI

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
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    wake_up():
        sends a basic fixed command to the Arduino to wake it up
    move_toolhead(coords):
        moves the arm to the given coordinates
    """


    mm_per_motor_step = 1
    serial_number = 55838343733351510170
    arduino_connection = None
    gui = None


    def __init__(self, mm_per_motor_step:int, gui:GUI):
        for port in s.tools.list_ports.comports():
            if int(self.serial_number) == int(port.serial_number):
                self.arduino_connection = s.Serial(port.device, baudrate=9600, timeout=.1)
                gui.frame_arduino_label(port.device)
        self.mm_per_motor_step = mm_per_motor_step
        self.gui = gui
        if self.arduino_connection is None:
            gui.frame_arduino_label("Arduino not connected")
        else:
            self.wake_up()


    def wake_up(self):
        """sends a wakes up the arduino by signalling it"""
        self.arduino_connection.write(bytes("0 0", 'utf-8'))

    def move_toolhead(self, coords):
        """moves the arm to the given coordinates"""
        #TODO actually signal arduino    
        x = round(coords[0]/self.mm_per_motor_step)
        y = round(coords[1]/self.mm_per_motor_step)
        print("Horizontal toolhead moving to (" + str(x) + ", " + str(y) + ")")

        input = str(x) + " " + str(y) + "\n"

        self.arduinoConnection.write(bytes(input, 'utf-8'))

        # old code from graphical_user_interface branch, delete?
        #if self.arduino_connection:
        #    self.arduino_connection.write(bytes(str(x_coord) + " " + str(y_coord), 'utf-8'))
        #    self.arduino_connection.readline()

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


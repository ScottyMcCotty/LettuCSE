from distutils import archive_util
from arduino import Arduino
import serial
import time

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
    arduinoConnection = None
    gui = None


    def __init__(self, mm_per_motor_step:int, gui:GUI):
        for arduino_port in serial.tools.list_ports.comports():
            if int(self.serial_number) == int(arduino_port.serial_number):
                self.arduinoConnection = serial.Serial(port=arduino_port.device, baudrate=9600, timeout=.1)
                gui.frame_arduino_label(arduino_port.device)
        self.mm_per_motor_step = mm_per_motor_step
        self.gui = gui
        if self.arduinoConnection == None:
            gui.frame_arduino_label("Arduino not connected")
        else:
            self.wake_up()


    def wake_up(self):
        """sends a basic fixed command to the Arduino"""
        dummyInput = "0 0"
        self.arduinoConnection.write(bytes(dummyInput, 'utf-8'))

    def move_toolhead(self, coords):
        """moves the arm to the given coordinates"""
        x = round(coords[0]/self.mm_per_motor_step)
        y = round(coords[1]/self.mm_per_motor_step)
        self.gui.update_status("Horizontal toolhead moving to (" + str(x) + ", " + str(y) + ")")

        input = str(x) + " " + str(y)

        if self.arduinoConnection:
            self.arduinoConnection.write(bytes(input, 'utf-8'))
            self.arduinoConnection.readline()

        #TODO in the actual robot, the toolhead will wait until getting a response, but fur now we have a sleep
        time.sleep(0.5)

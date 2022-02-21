"""Module contains vertical arduino class"""
from arduino import Arduino
import serial.tools.list_ports
import time
from gui import GUI


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
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    wake_up():
        sends a basic fixed command to the Arduino to wake it up
    grab_plant():
        lowers the toolhead arm to the plant and grabs it
    release_plant():
        releases the plant and raises the toolhead arm
    """


    mm_per_motor_step = 1
    arduinoConnection = None
    serial_number = 11111111111111111
    gui = None


    def __init__(self, mm_per_motor_step:int, gui:GUI):
        for arduino_port in serial.tools.list_ports.comports():
            if int(self.serial_number) == int(arduino_port.serial_number):
                self.arduinoConnection = serial.Serial(port=arduino_port.device, baudrate=9600, timeout=.1)
                gui.toolhead_arduino_label(arduino_port.device)
        self.mm_per_motor_step = mm_per_motor_step
        self.gui = gui
        if self.arduinoConnection == None:
            gui.toolhead_arduino_label("Arduino not connected")
        else:
            self.wake_up()

    def wake_up(self):
        """sends a basic fixed command to the Arduino"""
        #TODO actually signal arduino

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #TODO actually signal arduino
        self.gui.update_status("Toolhead releasing plant")
        #TODO in the actual robot, the toolhead will wait until getting a response, but fur now we have a sleep
        time.sleep(0.5)

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #TODO actually signal arduino
        self.gui.update_status("Toolhead grabbing plant")
        #TODO in the actual robot, the toolhead will wait until getting a response, but fur now we have a sleep
        time.sleep(0.5)

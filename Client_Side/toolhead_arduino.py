"""Module contains vertical arduino class"""
import time
import serial.tools.list_ports
from arduino import Arduino
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
    arduino_connection = None
    serial_number = 42069
    gui = None


    def __init__(self, mm_per_motor_step:int, gui:GUI):
        for port in serial.tools.list_ports.comports():
            if int(self.serial_number) == int(port.serial_number):
                self.arduino_connection = serial.Serial(port.device, baudrate=9600, timeout=.1)
                gui.toolhead_arduino_label(port.device)
        self.mm_per_motor_step = mm_per_motor_step
        self.gui = gui
        if self.arduino_connection is None:
            gui.toolhead_arduino_label("Arduino not connected")
        else:
            self.wake_up()

    def lower_toolhead(self):
        """lowers the toolhead arm to the plant"""
        #TODO actually signal arduino
        # print("Vertical toolhead lowering")
        return

    def wake_up(self):
        """sends a basic fixed command to the Arduino"""
        #TODO actually signal arduino
        # print("Vertical toolhead raising")
        return

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #TODO actually signal arduino
        self.gui.update_status("Toolhead releasing plant")
        #TODO make it so that rather than sleep you wait for a response
        time.sleep(0.2)
        # print("Vertical toolhead opening")

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #TODO actually signal arduino
        self.gui.update_status("Toolhead grabbing plant")
        #TODO make it so that rather than sleep you wait for a response
        time.sleep(0.2)
        # print("Vertical toolhead closing")


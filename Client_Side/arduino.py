"""Module contains the arduino class"""
from time import sleep
from serial import Serial, SerialException
from serial.tools import list_ports

class Arduino:

    """
    A parent class that represents all arduinos in the robot

    ...

    Attributes
    ----------
    arduino_connection : Serial connection object
        connection to one of the arduinos, or a None object
        if there is no connection
    port : int
        the unique port that the arduino can connect with
    gui : Tkinter object
        The main gui window

    Methods
    -------
    __init__(mm_per_motor_step, gui):
        calls the parent init, and then lists the connected port in
        the frame arduino section of the GUI
    wake_up():
        moves the arm to the given coordinates, where a tray hole should be found
    """


    arduino_connection = None
    serial_number = None
    port_name = "Arduino not connected"



    def __init__(self):
        """
            Search through all possible ports to find one with the correct
            serial number, if such an arduino can be found (serial number
            specified in child class). Sets the mm to motor step constant as
            0.14, this must be changed if the motor is changed.
        """
        for port in list_ports.comports():
            if int(self.serial_number) == int(port.serial_number):
                try:
                    self.arduino_connection = Serial(port.device, baudrate=9600, timeout=.1)
                    self.port_name = port.device
                    self.wake_up()
                except SerialException:
                    self.port_name = "ERROR CHANGE PORT PERMISSIONS TO ACCESS PORT"
        self.mm_per_motor_step = 0.14

    def wake_up(self):
        """signals the arduino to wake it up"""
        self.arduino_connection.write(bytes("0 0", 'utf-8'))

    def send_string_to_arduino(self, string_to_send):
        """Convert input to bytes, send it to arduino, wait until
        the command is "Done" before continuing"""
        if self.arduino_connection:
            self.arduino_connection.write(bytes(string_to_send, 'utf-8'))
            self.arduino_connection.readline()
            sleep(1)
            #while(True):
                #value = self.arduino_connection.readline().decode("utf-8")
                #print(f"Received from arduino: '{value}'")
                #if "Done" in value:
                #    break

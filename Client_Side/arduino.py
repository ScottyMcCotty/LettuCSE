"""Module contains the arduino class"""
from serial import Serial
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
    port = None

    def __init__(self, mm_per_motor_step:int):
        for port in list_ports.comports():
            if int(self.serial_number) == int(port.serial_number):
                try:
                    self.arduino_connection = Serial(port.device, baudrate=9600, timeout=.1)
                    self.port = port.device
                except:
                    self.port = "ERROR CHANGE PORT PERMISSIONS TO ACCESS PORTd"
                
        self.mm_per_motor_step = mm_per_motor_step

    def wake_up(self):
        """signals the arduino to wake it up"""
        self.arduino_connection.write(bytes("0 0", 'utf-8'))

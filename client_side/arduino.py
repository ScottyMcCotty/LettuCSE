"""Module contains the arduino class"""
from time import sleep
from serial import Serial, SerialException
from serial.tools import list_ports

class Arduino():
    """
    A class to represent the arduinos, and handle the client computer's connetions to them via port.
    It behaves as an 'abstract class' in the sense that it is never initialized, although since it
    is a python class it is not truly abstract
    ...

    Attributes
    ----------
    arduino_connection : serial connection
        The serial connection between the client's port and the given arduino.
        Library documentation here:
        https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
    port_name : str
        The client computer will likely have many ports, however the names
        will vary depending on the type of computer that the user has.
        After the ports have been querried for connections, the name of the
        port that has the connection will be stored here

    Methods
    -------
    send_to_arduino()
        Called by the child classes to communicate with the the arduino.
        It converts the input string into bytes, encodes it in utf-8, and
        sends it to the arduino connection. If there is no connection it
        passes
    calibrate()
        Sends the string 'calibrate' to the arduino, which is interprited as
        a command to go to the origin and set everything to zero. It is its
        own function because it is likely that it will become more complex
        in future itterations
    """
    arduino_connection = None
    port_name = "arduino not connected"
    mm_to_motor_constant = 0.1403
    name = "Arduino"

    def __init__(self, arduino_id:str, motor_data:list) -> None:
        """
            Set constants, find which port the arduino is connected to using
            list_ports, which is described here:
            https://pyserial.readthedocs.io/en/latest/tools.html,
            wait for arduino to confirm connection, and then calibrate
        """
        self.mm_to_motor_constant = float(motor_data["mm_to_motor_constant"])
        self.distance_traveled_to_lift_cup = float(motor_data["distance_traveled_to_lift_cup"])

        for port in list_ports.comports():
            if arduino_id == str(port.serial_number):
                try:
                    self.arduino_connection = Serial(port.device, baudrate=9600, timeout=.1)
                    self.port_name = port.device
                except SerialException:
                    self.port_name = "ERROR CHANGE PORT PERMISSIONS TO ACCESS PORT"
        if self.arduino_connection:
            response = self.arduino_connection.readline().decode("utf-8")
            while response == "":
                response = self.arduino_connection.readline().decode("utf-8")
        self.calibrate()

    def send_to_arduino(self, string_to_send:str) -> None:
        """Convert input to bytes, send string to arduino, wait until
        the arduino has finished movement which is indicated by it responding "Done"
        or "Calibrated", othewise sleep because if there are no arduinos connected it
        means the software is being tested and nothing needs to be sent """
        if self.arduino_connection:
            self.arduino_connection.write(bytes(string_to_send + "\n", 'utf8'))
            response = self.arduino_connection.readline().decode("utf-8")
            while "Done" not in response and "Calibrated" not in response:
                sleep(0.1)
                response = self.arduino_connection.readline().decode("utf-8")
        else:
            sleep(0.2)

    def calibrate(self) -> None:
        "sends a string saying calibrate to the toolhead"
        self.send_to_arduino("calibrate")

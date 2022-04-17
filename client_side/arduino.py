"""Module contains the arduino class"""
from time import sleep
from serial import Serial, SerialException
from serial.tools import list_ports

class Arduino():
    """
    A class to represent the arduinos, and handle their connections. It is never
    initalized itself, only it's child classes, so it is essentially an abstract
    class only those don't exist in python.
    ...

    Attributes
    ----------
    arduino_connection : serial connection
        the se
    port_name : str
        port that the arduino is connected to the computer on,
        displayed on the gui for debugging purposes

    Methods
    -------
    send_string_to_arduino()
        called by the child classes to connect to the arduino.
        Converts the input string into bytes, encodes it, and
        sends it to the arduino connection. If there is no
        arduino connection it does nothing.
    calibrate()
        sets everything to zero, places toolhead in the 
        right place
    """
    arduino_connection = None
    port_name = "Arduino not connected"
    mm_to_motor_constant = 1

    def __init__(self, arduino_id:str, motor_data:list) -> None:

        for port in list_ports.comports():
            if arduino_id == str(port.serial_number):
                try:
                    self.arduino_connection = Serial(port.device, baudrate=9600, timeout=.1)
                    self.port_name = port.device
                except SerialException:
                    self.port_name = "ERROR CHANGE PORT PERMISSIONS TO ACCESS PORT"
        self.mm_to_motor_constant = motor_data["mm_to_motor_constant"]
        self.corner_to_first_cup_x = motor_data["corner_to_first_cup_x"]
        self.corner_to_first_cup_y = motor_data["corner_to_first_cup_y"]
        self.distance_traveled_to_lift_cup = motor_data["distance_traveled_to_lift_cup"]

    def send_string_to_arduino(self, string_to_send:str) -> None:
        """Convert input to bytes, send it to arduino, wait until
        the command is "Done" before continuing if an arduino is connected,
        othewise sleep because it is on 'test mode'"""
        if self.arduino_connection:
            self.arduino_connection.write(bytes(string_to_send + "\n", 'utf8'))
            while True:
                response = self.arduino_connection.readline().decode("utf-8")
                if response == "":
                    print(f"Waiting for response from {self.port_name}...")
                    sleep(.5)
                else:
                    print(f"Response: '{response}'!")
                    break
        else:
            sleep(0.1)

    def calibrate(self) -> None:
        "sends a string saying calibrate to the toolhead"
        self.send_string_to_arduino("calibrate")

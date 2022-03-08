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
    serial number : int
        The unique serial number on the arduino.
        It is a 'None' here since the serial number
        is different for child classes
    port_name : string
        The port that the arduino is on with,
        or a string indicating that no port
        was found for the arduino's serial number

    Methods
    -------
    __init__(mm_per_motor_step, gui):
        calls the parent init, and then lists the connected port in
        the frame arduino section of the GUI
    wake_up():
        moves the arm to the given coordinates, where a tray hole should be found

    send_string_to_arduino():
        Turns the string into bytes and
        sends it along to the arduino, waits
        until the task is done to continue

    """

    arduino_connection = None
    serial_number = None
    port_name = "Arduino not connected"


    def __init__(self) -> None:
        """
            Search through all possible ports to find one with the correct
            serial number, if such an arduino can be found (serial number
            specified in child class). Sets the mm to motor step constant as
            0.14, this must be changed if the motor is changed.
        """
        for port in list_ports.comports():
            if str(self.serial_number) == str(port.serial_number):
                try:
                    self.arduino_connection = Serial(port.device, baudrate=9600, timeout=.1)
                    self.port_name = port.device
                    self.wake_up()
                except SerialException:
                    self.port_name = "ERROR CHANGE PORT PERMISSIONS TO ACCESS PORT"
        self.mm_per_motor_step = 0.14

    def wake_up(self) -> None:
        """signals the arduino to wake it up"""
        # self.arduino_connection.write(bytes("0 0" + "\n", 'utf8'))

        # wait for the first message from the arduino
        while True:
            msg = self.arduino_connection.readline().decode("utf-8")
            if msg == "":
                print(f"Waiting for {self.serial_number}'s initial message")
            else:
                print(f"{self.serial_number}'s initial message:")
                print(f"'{msg}'")
                break


    def send_string_to_arduino(self, string_to_send:str) -> None:
        """Convert input to bytes, send it to arduino, wait until
        the command is "Done" before continuing if an arduino is connected,
        othewise sleep because it is on 'test mode'"""
        if self.arduino_connection:
            self.arduino_connection.write(bytes(string_to_send + "\n", 'utf8'))

            while True:

                response = self.arduino_connection.readline().decode("utf-8")

                if response == "":
                    print(f"Waiting for response from {self.serial_number}...")
                    sleep(.5)
                else:
                    print(f"Response: '{response}'!")
                    break

        else:
            sleep(0.1)

"""Module contains vertical arduino class"""
from arduino import Arduino


class ToolheadArduino(Arduino):

    """
    A class to represent the Arduino being used to move the toolhead up and down
    The actual 'plant grabbing' is taken care of mechanically so this is not addressed
    by the client code

    ...

    Attributes
    ----------
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    raise_toolhead():
        signals the arduino to raise the toolhead
    lower_toolhead():
        signals the arduino to lower the toolhead
    """


    serial_number = "957363235323515012A2"


    def raise_toolhead(self, transplanting_over:int) -> None:
        """Sends a '0' signal to the toolhead arduino,
        which instructs the toolhead to go up"""
        if not transplanting_over:
            super().send_string_to_arduino(str(0))


    def lower_toolhead(self, transplanting_over:int) -> None:
        """Sends a '1' signal to the toolhead arduino,
        which instructs the toolhead to go down"""
        if not transplanting_over:
            super().send_string_to_arduino(str(1))

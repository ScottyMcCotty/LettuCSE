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
    name : string
         The name, used for debugging purposes

    Methods
    -------
    raise_toolhead():
        signals the arduino to raise the toolhead
    lower_toolhead():
        signals the arduino to lower the toolhead
    """

    name = "Toolhead Arduino :)"

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

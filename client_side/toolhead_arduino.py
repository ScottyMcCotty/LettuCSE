"""Module contains toolhead arduino class"""
from arduino import Arduino


class ToolheadArduino(Arduino):
    """
    A class to represent the frame arduino, which moves the toolhead along
    the horiznontal axis. It is also the class in which absolute coordinates
    are converted to motor coordinates
    ...

    Attributes
    ----------
    name : the name of the arduino to aid debugging

    Methods
    -------
    raise_toolhead()
        instruct the toolhead arduino to raise

    lower_toolhead()
        instruct the toolhead arduino to lower
    """

    name = "Toolhead Arduino"


    def raise_toolhead(self) -> None:
        """Sends a '0' signal to the toolhead arduino,
        which instructs the toolhead to go up"""
        super().send_to_arduino(str(0))


    def lower_toolhead(self) -> None:
        """Sends a '1' signal to the toolhead arduino,
        which instructs the toolhead to go down"""
        super().send_to_arduino(str(1))

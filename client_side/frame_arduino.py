"""This module contains the Frame Arduino class which is a child of the Arduino class"""
from arduino import Arduino

class FrameArduino(Arduino):
    """
    A class to represent the frame arduino, which moves the toolhead along
    the x and y axis. It is also the class in which absolute coordinates
    are converted to motor coordinates. Absolute coordinates are in mm,
    motor coordinates are in motor steps.
    ...

    Attributes
    ----------
    distance_traveled_to_lift_cup : float
        the number of mm behind the cup that the toolhead will first
        land when it is lowered, and the number of mm behind the cup
        that the toolhead will slide after dropping a cup
    name : str
        the name of the arduino (for debugging)
    location : tuple
        The coordinates that the toolhead is moving to in motor
        coordinates. This data is used by the label which shows
        the location of the toolhead in the GUI.

    Methods
    -------
    go_to_origin()
        Go to the center of the first cup. This is used to end the transplanting
        if the user stops everything
    go_behind_cup(coords:tuple)
        Goes to a given value behind the first cup so that
        when the toolhead is lowered, it is beind the cup
        and does not squish the plant on landing. Also useful
        after a cup has been dropped so it can slide behind the 
        cup
    go_to_cup(coords:tuple)
        Goes to the coordinates specified
    """

    distance_traveled_to_lift_cup = 0
    location = (0,0)
    name = "Frame Arduino"

    def go_to_origin(self) -> None:
        """Sends the toolhead to the center of the first cup"""
        super().send_to_arduino('calibrate')
        self.location = (0,0)


    def go_behind_cup(self, coords:tuple) -> bool:
        """Go to a given distance behind the cup so that it will
        be in place to scoop it up when it is lifted"""
        x_coord = round((coords[0] + self.distance_traveled_to_lift_cup)/
            super().mm_to_motor_constant)
        y_coord = round((coords[1])/super().mm_to_motor_constant)
        self.location = (x_coord,y_coord)
        super().send_to_arduino(str(x_coord) + " " +str(y_coord))
        return True

    def go_to_cup(self, coords:tuple) -> bool:
        """Go directly to the cordinate location"""
        x_coord = round(coords[0]/super().mm_to_motor_constant)
        y_coord = round(coords[1]/super().mm_to_motor_constant)
        self.location = (x_coord,y_coord)
        super().send_to_arduino(str(x_coord) + " " +str(y_coord))
        return True

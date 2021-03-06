"""This module contains the Frame Arduino class which is a child of the Arduino class"""
from arduino import Arduino

class FrameArduino(Arduino):
    """
    A class to represent the frame arduino, which moves the toolhead along
    the horiznontal axis. It is also the class in which absolute coordinates
    are converted to motor coordinates
    ...

    Attributes
    ----------
    corner_to_first_cup_x : float
        distance on the x axis of the motor origin from the (0,0) corner
    corner_to_first_cup_y : float
        distance on the y axis of the motor origin from the (0,0) corner
    distance_traveled_to_lift_cup : float
        the number of mm behind the cup that the toolhead will first
        land when it is lowered
    name : str
        the name of the arduino to aid debugging
    location : tuple
        the coordinates that the toolhead is moving to.
        This data is used by the label which shows
        the location of the toolhead

    Methods
    -------
    go_to_origin()
        Go to the center of the first cup
    go_behind_cup(coords:tuple)
        Goes to a given value behind the first cup so that
        when the toolhead is lowered, it is in the right place
    go_to_cup(coords:tuple)
        Goes to the coordinates specified
    """

    corner_to_first_cup_x = 0
    corner_to_first_cup_y = 0
    distance_traveled_to_lift_cup = 0
    location = (0,0)
    name = "Frame Arduino"

    def go_to_origin(self) -> None:
        """Sends the toolhead to the center of the first cup"""
        self.location = (0,0)
        super().send_to_arduino(str(self.corner_to_first_cup_x) +
                                      " " +
                                      str(self.corner_to_first_cup_y))


    def go_behind_cup(self, coords:tuple) -> None:
        """Go to a given distance behind the cup so that it will
        be in place to scoop it up when it is lifted"""
        x_coord = round((coords[0]- self.corner_to_first_cup_x + self.distance_traveled_to_lift_cup)/super().mm_to_motor_constant)
        y_coord = round((coords[1] - self.corner_to_first_cup_y)/super().mm_to_motor_constant)
        self.location = (x_coord,y_coord)
        super().send_to_arduino(str(x_coord) + " " +str(y_coord))

    def go_to_cup(self, coords:tuple) -> None:
        """Go directly to the cordinate location"""
        x_coord = round((coords[0] - self.corner_to_first_cup_x)/super().mm_to_motor_constant)
        y_coord = round((coords[1] - self.corner_to_first_cup_y)/super().mm_to_motor_constant)
        self.location = (x_coord,y_coord)
        super().send_to_arduino(str(x_coord) + " " +str(y_coord))

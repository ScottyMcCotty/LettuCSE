"""This module contains the Frame Arduino class which is a child of the Arduino class"""
from arduino import Arduino

class FrameArduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm to a certain
    (x,y) location

    ...

    Attributes
    ----------
    serial_number : int
        the serial number of the arduino that is being used for the frame
        if you change the toolhead arduino you will have to change this number
    status : tuple(int)
        the location of the toolhead which is reported to the GUI so it can
        be displayed

    Methods
    -------
    move_toolhead(coords):
        moves the arm to the given coordinates, where a tray hole should be found
    """


    serial_number = "957363235323514040C0"
    status = ""
    distance_for_picking_up_cup = 25

    def move_toolhead_to_coords(self, coords:tuple, transplanting_over:int) -> None:
        '''
            Moves the arm to the given coordinates

            Parameters:
                    coords : tuple(int)
                        the 2D coords that the arm is
                        intending to move to, in milimeters
            Returns:
                    None
        '''
        if not transplanting_over:
            print("HERE")
            x_coord = round(coords[0]/self.mm_per_motor_step)
            y_coord = round(coords[1]/self.mm_per_motor_step)
            super().send_string_to_arduino(str(x_coord) + " " +str(y_coord))
            self.status = (x_coord, y_coord)

    def move_toolhead_behind_coords(self, coords:tuple, transplanting_over:int) -> None:
        '''
            Moves the arm to the given coordinates

            Parameters:
                    coords : tuple(int)
                        the 2D coords that the arm is
                        intending to move to, in milimeters
            Returns:
                    None
        '''
        if not transplanting_over:
            print("HERE")
            x_coord = round(coords[0]/self.mm_per_motor_step)
            y_coord = round((coords[1]-self.distance_for_picking_up_cup)/self.mm_per_motor_step)
            super().send_string_to_arduino(str(x_coord) + " " +str(y_coord))
            self.status = (x_coord, y_coord)

    def move_toolhead_forward(self, transplanting_over:int) -> None:
        """Move the toolhead slightly forward so the toolhead
        can pick up the cup"""
        if not transplanting_over:
            print("HERE")
            x_coord = self.status[0]
            y_coord = round(self.status[1] + self.distance_for_picking_up_cup/self.mm_per_motor_step)
            super().send_string_to_arduino(str(x_coord) + " " +str(y_coord))
            self.status = (x_coord, y_coord)

    def move_toolhead_back(self, transplanting_over:int) -> None:
        """Move the toolhead slightly
        backward to drop the cup"""
        if not transplanting_over:
            print("HERE")
            x_coord = self.status[0]
            y_coord = round(self.status[1] - self.distance_for_picking_up_cup/self.mm_per_motor_step)
            super().send_string_to_arduino(str(x_coord) + " " +str(y_coord))
            self.status = (x_coord, y_coord)

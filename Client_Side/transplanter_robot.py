"""Contains the transplanter_robot class"""
import enum
from time import sleep
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from tray import Tray

class TransplanterRobot:
    """
    A class to handle the ways that all the trays and arduinos mesh together
    to transplant a plant from one location to another. The enum variables
    which represent the state are entirely controled by the GUI. If you are wondering
    where the state was changed and are confused, LOOK IN THE GUI CLASS.

    ...

    Attributes
    ----------
    source_tray : tray
        The tray that the plants are being moved from
    destination_tray : tray
        The tray that the plants are being moved to
    frame_arduino: FrameArduino
        the arduino that controls the frame
    toolhead_arduino: ToolheadArduino
        the arduino that controls the toolhead
    trays_need_replacing: boolean
        whether the robot should pause to wait for
        trays replaced

    Methods
    -------
    end():
        Returns arm to origin
    repot_single_plant(source, destination):
        Given the location in mm of the source and destination holes,
        move the plant from one spot to another
    wait_for_tray_replace()
        pause everything and wait for tray to be replaced
    transplant()
        determine when to move a plant, when
        to pause and wait for the replacement, and when to stop

    """
    source_tray = None
    destination_tray = None
    frame_arduino = None
    toolhead_arduino = None
    trays_need_replacing = False
    continue_transplanting = True
    button_stages = enum.Enum("button_stages", "PRE_TRANSPLANT IN_TRANSPLANT WAIT")
    current_state = None


    def __init__(self, source: Tray, destination: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino):
        self.source_tray = source
        self.destination_tray = destination
        self.frame_arduino = frame_arduino
        self.toolhead_arduino = toolhead_arduino
        self.current_state = self.button_stages.PRE_TRANSPLANT


    def end(self) -> None:
        '''Returns arm to the origin' and retracts it in order
            to prepare the robot for shutdown'''
        self.frame_arduino.move_toolhead((0,0))
        self.toolhead_arduino.release_plant()

    def repot_single_plant(self, source:tuple, destination: tuple) -> None:
        '''
        Sends the arduino commands to move the plant from the source tray to the destination tray

                Parameters:
                        source (float tuple): The X and Y values of the plant to be repotted
                        destination (float tuple): The X and Y values that the plant is sent to
                        arduino (Arduino): The arduino object being used for the arm
                Returns:
                        None
        '''
        self.frame_arduino.move_toolhead(source)
        self.toolhead_arduino.grab_plant()
        self.frame_arduino.move_toolhead(destination)
        self.toolhead_arduino.release_plant()


    def wait_for_tray_replace(self) -> None:
        """Pause transplanting while waiting for the human to replace the tray
           The current state variable is altered in the GUI class when one
           of the buttons is pressed"""
        self.current_state = self.button_stages.WAIT
        while self.current_state is self.button_stages.WAIT:
            sleep(0.1)

    def transplant(self) -> None:
        '''
        Compares the sizes of the two trays, warns the user if they are different
        sizes (which may indicate a faulty json file)

                Parameters:
                        source_tray (Tray): the original tray containing lettuce
                        destination_tray (Tray): tray the lettuce is being moved to
                        arduino (Arduino): The arduino object being used for the arm
                Returns:
                        None
        '''
        source_hole_itt = destination_hole_itt = 0
        self.current_state = self.button_stages.PRE_TRANSPLANT
        while self.continue_transplanting:
            if source_hole_itt == self.source_tray.get_number_of_holes():
                self.wait_for_tray_replace()
                source_hole_itt = 0
            elif destination_hole_itt == self.destination_tray.get_number_of_holes():
                self.wait_for_tray_replace()
                destination_hole_itt = 0
            else:
                self.current_state = self.button_stages.IN_TRANSPLANT
                source_hole = self.source_tray.ith_hole_location(source_hole_itt)
                destination_hole = self.destination_tray.ith_hole_location(destination_hole_itt)
                self.repot_single_plant(source_hole,destination_hole)
                source_hole_itt += 1
                destination_hole_itt += 1
        self.current_state = self.button_stages.PRE_TRANSPLANT
        self.end()

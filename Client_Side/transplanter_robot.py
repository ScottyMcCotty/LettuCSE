from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from tray import Tray
from tkinter import IntVar
from gui import GUI

class TransplanterRobot:
    source_tray = None
    destination_tray = None
    frame_arduino = None
    toolhead_arduino = None
    gui = None
    trays_been_replaced = 0

    def __init__(self, source: Tray, destination: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino, gui:GUI):
        self.source_tray = source
        self.destination_tray = destination
        self.frame_arduino = frame_arduino
        self.toolhead_arduino = toolhead_arduino
        self.gui = gui


    def end(self) -> None:
        '''Returns arm to the origin'''
        self.frame_arduino.move_toolhead((0,0))
        self.toolhead_arduino.release_plant()

    def repot_single_plant(self, source: Tray, destination: Tray) -> None:
        '''
        Sends the arduino commands to move the plant from the source tray to the destination tray

                Parameters:
                        source (int tuple): The X and Y values of the plant to be repotted
                        destination (int tuple): The X and Y values that the plant is sent to
                        arduino (Arduino): The arduino object being used for the arm
                Returns:
                        None
        '''
        self.frame_arduino.move_toolhead(source)
        self.toolhead_arduino.grab_plant()
        self.frame_arduino.move_toolhead(destination)
        self.toolhead_arduino.release_plant()


    def wait_for_tray_replace(self) -> None:
        """Pause transplanting while waiting for the human to replace the tray"""
        self.gui.set_buttons_to_waiting_for_tray_replacement()
        self.gui.update_status("Tray is full - replace tray or end program")

        self.gui.start_button.wait_variable(self.gui.continue_transplanting)

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
        source_hole_itterator = destination_hole_itterator = 0
        #self.gui.set_buttons_to_pre_transplant_stage()
        while self.gui.continue_transplanting:
            if source_hole_itterator == self.source_tray.get_number_of_holes():
                self.wait_for_tray_replace(self.trays_been_replaced)
                source_hole_itterator = 0
            elif destination_hole_itterator == self.destination_tray.get_number_of_holes():
                self.wait_for_tray_replace(self.trays_been_replaced)
                destination_hole_itterator = 0
            else:
                #self.gui.set_buttons_to_in_transplant_stage()
                source_hole = self.source_tray.ith_hole_location(source_hole_itterator)
                destination_hole = self.destination_tray.ith_hole_location(destination_hole_itterator)
                self.repot_single_plant(source_hole,destination_hole)
                source_hole_itterator += 1
                destination_hole_itterator += 1
        self.gui.set_buttons_to_pre_transplant_stage()
        self.end()
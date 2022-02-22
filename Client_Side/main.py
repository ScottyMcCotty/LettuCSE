"""When run, this module makes the robot begin transplanting"""
from tkinter import DISABLED, NORMAL, Button, IntVar
from gui import GUI
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino

def end(frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
    '''Returns arm to the origin'''
    frame_arduino.move_toolhead((0,0))
    toolhead_arduino.release_plant()

def repot_single_plant(source: Tray, destination: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
    '''
    Sends the arduino commands to move the plant from the source tray to the destination tray

            Parameters:
                    source (int tuple): The X and Y values of the plant to be repotted
                    destination (int tuple): The X and Y values that the plant is sent to
                    arduino (Arduino): The arduino object being used for the arm
            Returns:
                    None
    '''
    frame_arduino.move_toolhead(source)
    toolhead_arduino.grab_plant()
    frame_arduino.move_toolhead(destination)
    toolhead_arduino.release_plant()


def wait_for_tray_replace(main_button:Button, stop_trigger:IntVar, gui:GUI):
    gui.set_buttons_to_waiting_for_tray_replacement()
    gui.update_status("Tray is full - replace tray or end program")
    main_button.wait_variable(stop_trigger)

def transplant(source: Tray, destination: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino, gui:GUI) -> None:
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
    source_hole = destination_hole = 0
    stop_trigger = IntVar()
    while gui.proceed:
        if source_hole == source.get_number_of_holes():
            wait_for_tray_replace(gui.main_button, stop_trigger, gui)
            source_hole = 0
        elif destination_hole == destination.get_number_of_holes():
            wait_for_tray_replace(gui.main_button, stop_trigger, gui)
            destination_hole = 0
        else:
            gui.set_buttons_to_in_transplant_stage()
            repot_single_plant(source.ith_hole_location(source_hole),destination.ith_hole_location(destination_hole), frame_arduino, toolhead_arduino)
            source_hole += 1
            destination_hole += 1
    gui.set_buttons_to_pre_transplant_stage()
    end(frame_arduino, toolhead_arduino)
     

def main():
    """Run the transplanter"""
    gui = GUI()
    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())
    frame_arduino = FrameArduino(0.14, gui)
    toolhead_arduino = ToolheadArduino(0.14, gui)
    gui.configure_stop_button()
    gui.configure_main_button(transplant, source_tray, destination_tray, frame_arduino, toolhead_arduino)
    gui.loop()


    

if __name__ == "__main__":
    main()

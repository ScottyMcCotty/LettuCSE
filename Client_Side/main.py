"""When run, this module makes the robot begin transplanting"""
from gui import GUI
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino

def end(frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
    '''Returns arm to the origin, exits without error'''
    frame_arduino.move_toolhead((0,0))
    toolhead_arduino.release_plant()
    print("Repotting Completed")
    exit(0)

def shut_down() -> None:
    '''Quits program without returning main arm to the origin, program returns an error'''
    print("EMERGENCY SHUTDOWN")
    exit(1)

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

def ask_to_quit(frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
    """Asks the user if they want to continue repotting, ends program gracefully if they do not"""
    quit_or_continue=input()
    if quit_or_continue.lower() == 'e':
        end(frame_arduino, toolhead_arduino)

def test_trays(tray_1: Tray, tray_2: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
    '''
    Compares the sizes of the two trays, warns the user if the size difference is greater
    than 5% error (which may indicate a faulty json file)

            Parameters:
                    tray_1 (Tray): one of the two trays created from the JSON file
                    tray_2 (Tray): the other of the two trays created from the JSON file
                    arduino (Arduino): The arduino object being used for the arm
            Returns:
                    None
    '''
    width_1, width_2 =  tray_1.get_width(), tray_2.get_width()
    length_1, length_2 =  tray_1.get_length(), tray_2.get_length()
    if (abs(width_1-width_2)/width_1) > 0.05:
        print("Warning: the json files for your trays suggest that they are"
              "different widths, you may have an error in your json file\n"
              "Press e to end and any other key to continue")
        ask_to_quit(frame_arduino, toolhead_arduino)
    if (abs(length_1-length_2)/length_1) > 0.05:
        print("Warning: the json files for your trays suggest that they are "
              "different lengths, you may have an error in your json file\n"
              "Press e to end and any other key to continue")

def transplant(source_tray: Tray, destination_tray: Tray, frame_arduino: FrameArduino, toolhead_arduino: ToolheadArduino) -> None:
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
    try:
        while True:
            if source_hole == source_tray.get_number_of_holes():
                print("Tray is empty - Press 'e' to end repotting or any "
                      "other key to continue after tray is replaced\n")
                ask_to_quit(frame_arduino, toolhead_arduino)
                source_hole = 0
            elif destination_hole == destination_tray.get_number_of_holes():
                print("Tray is full - Press 'e' to end repotting or any "
                      "other key to continue after tray is replaced\n")
                ask_to_quit(frame_arduino, toolhead_arduino)
                destination_hole = 0
            else:
                repot_single_plant(source_tray.ith_hole_location(source_hole),
                                       destination_tray.ith_hole_location(destination_hole), 
                                       frame_arduino, toolhead_arduino)
                source_hole += 1
                destination_hole += 1

    except KeyboardInterrupt:
        shut_down()    

def main():
    """Run the transplanter"""
    gui = GUI()
    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())
    frame_arduino = FrameArduino(0.14, gui)
    toolhead_arduino = ToolheadArduino(0.14, gui)
    test_trays(source_tray, destination_tray, frame_arduino, toolhead_arduino)
    gui.configure_start_button(transplant, source_tray, destination_tray, frame_arduino, toolhead_arduino)
    gui.loop()


    

if __name__ == "__main__":
    main()

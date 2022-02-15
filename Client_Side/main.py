"""When run, this module makes the robot begin transplanting"""
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from arduino_error import ArduinoError

# GLOBAL VARIABLE: COM ports used for the frame & toolhead Arduinos (Liam)
# NOTE: Will need to be updated later, either from user input
#       or the input JSON file (if possible)
COM_PORT_FRAME =    "COM5"
COM_PORT_TOOLHEAD = "COM4"

def end(arduino_for_xy_movement, arduino_for_arm_movement):
    '''Returns arm to the origin, exits without error'''
    arduino_for_xy_movement.move_toolhead((0,0))
    arduino_for_arm_movement.release_plant()
    arduino_for_arm_movement.raise_toolhead()
    print("Repotting Completed")
    exit(0)

def shut_down():
    '''Quits program without returning main arm to the origin, program returns an error'''
    print("EMERGENCY SHUTDOWN")
    exit(1)

def startup(arduino_for_xy_movement, arduino_for_arm_movement):
    '''Greets user and gives instructions for use'''
    print("You have successfully initialized the LettuceCSE Lettuce Repotter, designed and "
          "implemented by Marin Orosa, Scott Ballinger, Mira Welner, and Liam Carr under "
          "the supervision of Professor Lieth\n"
          "Use a keyboard interrupt (control c) to instantly freeze arm and shut down program\n"
          "Press 'e' when prompted to move arm to origin and end program\n"
          "Press any other key to begin")
    ask_to_quit(arduino_for_xy_movement, arduino_for_arm_movement)

def repot_single_plant(source, destination, arduino_for_xy_movement, arduino_for_arm_movement):
    '''
    Sends the arduino commands to move the plant from the source tray to the destination tray

            Parameters:
                    source (int tuple): The X and Y values of the plant to be repotted
                    destination (int tuple): The X and Y values that the plant is sent to
                    arduino (Arduino): The arduino object being used for the arm
            Returns:
                    None
    '''
    arduino_for_xy_movement.move_toolhead(source)
    arduino_for_arm_movement.lower_toolhead()
    arduino_for_arm_movement.grab_plant()
    arduino_for_arm_movement.raise_toolhead()
    arduino_for_xy_movement.move_toolhead(destination)
    arduino_for_arm_movement.lower_toolhead()
    arduino_for_arm_movement.release_plant()
    arduino_for_arm_movement.raise_toolhead()

def ask_to_quit(arduino_for_xy_movement, arduino_for_arm_movement):
    """Asks the user if they want to continue repotting, ends program gracefully if they do not"""
    quit_or_continue=input()
    if quit_or_continue.lower() == 'e':
        end(arduino_for_xy_movement, arduino_for_arm_movement)

def test_trays(tray_1, tray_2, arduino_for_xy_movement, arduino_for_arm_movement):
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
        ask_to_quit(arduino_for_xy_movement, arduino_for_arm_movement)
    if (abs(length_1-length_2)/length_1) > 0.05:
        print("Warning: the json files for your trays suggest that they are "
              "different lengths, you may have an error in your json file\n"
              "Press e to end and any other key to continue")

def transplant(source_tray, destination_tray, arduino_for_xy_movement, arduino_for_arm_movement):
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
                ask_to_quit(arduino_for_xy_movement, arduino_for_arm_movement)
                source_hole = 0
            elif destination_hole == destination_tray.get_number_of_holes():
                print("Tray is full - Press 'e' to end repotting or any "
                      "other key to continue after tray is replaced\n")
                ask_to_quit(arduino_for_xy_movement, arduino_for_arm_movement)
                destination_hole = 0
            else:
                try:
                    repot_single_plant(source_tray.ith_hole_location(source_hole),
                                       destination_tray.ith_hole_location(destination_hole), 
                                       arduino_for_xy_movement, arduino_for_arm_movement)
                except ArduinoError:
                    shut_down()
                source_hole += 1
                destination_hole += 1

    except KeyboardInterrupt:
        shut_down()


def main():
    """Run the transplanter"""
    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())
    arduino_for_xy_movement = FrameArduino(0.14, COM_PORT_FRAME)
    arduino_for_arm_movement = ToolheadArduino(0.14, COM_PORT_TOOLHEAD)
    test_trays(source_tray, destination_tray, arduino_for_xy_movement, arduino_for_arm_movement)
    startup(arduino_for_xy_movement, arduino_for_arm_movement)
    transplant(source_tray, destination_tray, arduino_for_xy_movement, arduino_for_arm_movement)

if __name__ == "__main__":
    main()

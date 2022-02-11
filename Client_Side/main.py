from tray import Tray
from arduino import Arduino
from arduino_error import ArduinoError

def end(arduino):
    '''Returns arm to the origin, exits without error'''
    arduino.move_toolhead((0,0))
    print("Repotting Completed")
    exit(0)

def shut_down():
    '''Quits program without returning main arm to the origin, program returns an error'''
    print("EMERGENCY SHUTDOWN")
    exit(1)

def startup(arduino):
    '''Greets user and gives instructions for use'''
    print("You have successfully initialized the LettuceCSE Lettuce Repotter, designed and implemented by Marin Orosa, Scott Ballinger, Mira Welner, and Liam Carr under the supervision of Professor Lieth\n"
            "Use a keyboard interrupt (control c) to instantly freeze arm and shut down program\n"
            "Press 'e' when prompted to move arm to origin and end program\n"
            "Press any other key to begin")
    ask_to_quit(arduino)

def repot_single_plant(source, destination, arduino):
    '''
    Sends the arduino commands to move the plant from the source tray to the destination tray

            Parameters:
                    source (int tuple): The X and Y values of the plant to be repotted
                    destination (int tuple): The X and Y values that the plant is sent to
                    arduino (Arduino): The arduino object being used for the arm
    '''
    arduino.move_toolhead(source)
    arduino.lower_toolhead()
    arduino.grab_plant()
    arduino.raise_toolhead()
    arduino.move_toolhead(destination)
    arduino.lower_toolhead()
    arduino.release_plant()
    arduino.raise_toolhead()

def ask_to_quit(arduino):
    """Asks the user if they want to continue repotting, ends program gracefully if they do not"""
    quit_or_continue=input()
    if quit_or_continue.lower() == 'e':
        end(arduino)

def test_trays(tray_1, tray_2, arduino):
    '''
    Compares the sizes of the two trays, warns the user if they are different sizes (which may indicate a faulty json file)

            Parameters:
                    tray_1 (Tray): one of the two trays created from the JSON file
                    tray_2 (Tray): the other of the two trays created from the JSON file
                    arduino (Arduino): The arduino object being used for the arm
    '''
    width_1, width_2 =  tray_1.get_width(), tray_2.get_width()
    height_1, height_2 =  tray_1.get_length(), tray_2.get_length()
    if width_1-width_2 < -1 or width_1-width_2 > 1 or height_1-height_2 < -1 or height_1-height_2 > 1:
        print("Warning: the json files for your trays suggest that they are different sizes, you may have an error in your json file\n"
                        "Press e to end and any other key to continue")
        ask_to_quit(arduino)


def main():

    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())

    arduino_in_use = Arduino(0.14)

    source_hole = destination_hole = 0

    test_trays(source_tray, destination_tray, arduino_in_use)

    startup(arduino_in_use)
    

    try:
        while(True):
            if source_hole == source_tray.get_number_of_holes():
                print("Tray is empty - Press 'e' to end repotting or any other key to continue after tray is replaced\n")
                ask_to_quit(arduino_in_use)
                source_hole = 0
            elif destination_hole == destination_tray.get_number_of_holes():
                print("Tray is full - Press 'e' to end repotting or any other key to continue after tray is replaced\n")
                ask_to_quit(arduino_in_use)
                destination_hole = 0
            else:
                try:
                    repot_single_plant(source_tray.ith_hole_location(source_hole), destination_tray.ith_hole_location(destination_hole), arduino_in_use)
                except(ArduinoError):
                    shut_down()
                source_hole+=1
                destination_hole+=1

    except KeyboardInterrupt:
        shut_down()

if __name__ == "__main__":
    main()
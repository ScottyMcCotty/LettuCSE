from tray import Tray
from arduino_signals import *
def main():
    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())
    
    source_hole = 0
    destination_hole = 0

    while(True):
        if source_hole == source_tray.get_number_of_holes():
            print("Tray is Empty - Please Replace")
            source_hole = 0
        elif destination_hole == destination_tray.get_number_of_holes():
            print("Tray is Full - Please Replace")
            destination_hole = 0
        else:
            move_toolhead(source_tray.ith_hole_location(source_hole))
            lower_toolhead()
            grab_plant()
            raise_toolhead()
            move_toolhead(destination_tray.ith_hole_location(destination_hole))
            lower_toolhead()
            release_plant()
            raise_toolhead()
            source_hole+=1
            destination_hole+=1



if __name__ == "__main__":
    main()
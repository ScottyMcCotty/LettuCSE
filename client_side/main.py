"""The main function class - you run it with python3 main.py"""
import configparser
from tkinter import Tk
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from window_maker import WindowMaker
from relocate_plant import RelocatePlant


def main():
    config = configparser.ConfigParser()
    config.read('configfile.ini')

    destination_tray = Tray(config["JSON_FILES"]["destination_tray"])
    next_destination_hole = destination_tray.get_next_hole
    destination_tray_full = destination_tray.is_tray_full

    source_tray = Tray(config["JSON_FILES"]["source_tray"])
    next_source_hole = source_tray.get_next_hole
    source_tray_full = source_tray.is_tray_full
    
    f_arduino = FrameArduino(config["ARDUINO_ID"]["frame_arduino_id"], config["MOTOR"])
    go_to_cup = f_arduino.go_to_cup
    go_behind_cup = f_arduino.go_behind_cup
    go_to_origin = f_arduino.go_to_origin


    t_arduino = ToolheadArduino(config["ARDUINO_ID"]["toolhead_arduino_id"], config["MOTOR"])
    raise_toolhead = t_arduino.raise_toolhead
    lower_toolhead = t_arduino.lower_toolhead

    tkinter_instance = Tk()

    port_name_labels = PortNameLabel(tkinter_instance, t_arduino.port_name, f_arduino.port_name)
    window_maker = WindowMaker(tkinter_instance)

    plant_relocator = RelocatePlant(go_behind_cup, go_to_cup, raise_toolhead, lower_toolhead)

    gui_window = window_maker.window




    gui_window.mainloop()

if __name__ == "__main__":
    main()

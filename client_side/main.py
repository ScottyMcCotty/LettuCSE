"""The main function class - you run it with python3 main.py"""
import configparser
from tkinter import Tk
from toolhead_illustrator import ToolheadIllustrator
from toolhead_location_label import ToolheadLocationLabel
from start_continue_button import StartContinueButton
from port_name_label import PortNameLabel
from transplanter import Transplanter
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from window_maker import WindowMaker
from relocate_plant import RelocatePlant
from stop_button import StopButton


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

    plant_relocator = RelocatePlant(go_behind_cup, go_to_cup, raise_toolhead, lower_toolhead, go_to_origin)
    relocation_function = plant_relocator.transport_plant
    reset = plant_relocator.reset_transplanter

    transplanter = Transplanter(source_tray_full, destination_tray_full,
                                                 next_source_hole,
                                                 next_destination_hole,
                                                 reset,
                                                 relocation_function)

    transplant = transplanter.transplant
    continue_transplant = transplanter.continue_transplant

    start_continue_button = StartContinueButton(tkinter_instance, transplant, continue_transplant)
    stop_transplant = start_continue_button.set_to_stopped_mode
    stop_button = StopButton(tkinter_instance, stop_transplant)
    location_label = ToolheadLocationLabel(tkinter_instance)
    toolhead_illustrator = ToolheadIllustrator(tkinter_instance)



    gui_window = window_maker.window


    while True:
        #stop handler
        if start_continue_button.is_transplanting and not transplanter.stopped:
            transplanter.restart()
            stop_button.enable_button()
        if stop_button.stopped_flag:
            transplanter.stop()
            start_continue_button.set_to_stopped_mode()
        if start_continue_button.is_transplanting and not stop_button.is_enabled:
            stop_button.enable_button()

        #pause handler
        if transplanter.paused:
            start_continue_button.set_to_pause_mode()

        # location display handler
        location_label.update_location(f_arduino.location)
        toolhead_illustrator.update_location(f_arduino.location)

        gui_window.update()



if __name__ == "__main__":
    main()

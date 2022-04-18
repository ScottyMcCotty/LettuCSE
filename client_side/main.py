"""The main function class - you run it with python3 main.py"""
import configparser
from tkinter import Tk
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from window_maker import WindowMaker
from port_name_label import PortNameLabel


def main():
    config = configparser.ConfigParser()
    config.read('configfile.ini')
    destination_tray = Tray(config["JSON_FILES"]["destination_tray"])
    source_tray = Tray(config["JSON_FILES"]["source_tray"])
    
    f_arduino = FrameArduino(config["ARDUINO_ID"]["frame_arduino_id"], config["MOTOR"])
    t_arduino = ToolheadArduino(config["ARDUINO_ID"]["toolhead_arduino_id"], config["MOTOR"])

    tkinter_instance = Tk()

    main_port_name_lables = PortNameLabel(tkinter_instance, t_arduino.port_name, f_arduino.port_name)
    main_window_maker = WindowMaker(tkinter_instance)




    gui_window = main_window_maker.window




    gui_window.mainloop()

if __name__ == "__main__":
    main()

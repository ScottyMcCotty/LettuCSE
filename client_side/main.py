"""The main function class - you run it with python3 main.py"""
import configparser
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino
from serial.tools import list_ports


def main():
    config = configparser.ConfigParser()
    config.read('configfile.ini')
    destination_tray = Tray(config["JSON_FILES"]["destination_tray"])
    source_tray = Tray(config["JSON_FILES"]["source_tray"])
    
    f_arduino = FrameArduino(config["ARDUINO_ID"]["frame_arduino_id"], config["MOTOR"])
    t_arduino = ToolheadArduino(config["ARDUINO_ID"]["toolhead_arduino_id"], config["MOTOR"])

    for port in list_ports.comports():
        print(port.serial_number)

if __name__ == "__main__":
    main()
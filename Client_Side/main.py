"""When run, this module makes the robot begin transplanting"""
import yaml
from transplanter_robot import TransplanterRobot
from gui import GUI
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino


def load_config_file():
    """Load the config file which is stored in yaml"""
    config_file = open("config.yaml")
    return yaml.load(config_file, Loader=yaml.FullLoader)




def main():
    """Run the transplanter based on data from the config file"""
    config_file = load_config_file()

    source_tray = Tray(config_file["LINK_TO_DENSE_TRAY_JSON"], config_file["CALIBRATION"])
    destination_tray = Tray(config_file["LINK_TO_SPARSE_TRAY_JSON"], config_file["CALIBRATION"], source_tray.get_width())

    frame_arduino = FrameArduino(config_file["FRAME_ARDUINO_ID"], config_file["MM_PER_MOTOR_STEP"])
    toolhead_arduino = ToolheadArduino(config_file["TOOLHEAD_ARDUINO_ID"], config_file["MM_PER_MOTOR_STEP"])

    transplanter = TransplanterRobot(source_tray, destination_tray, frame_arduino, toolhead_arduino)
    gui = GUI(transplanter.transplant, transplanter.end, transplanter.continue_transplant)
    gui.label_ports(toolhead_arduino.port_name, frame_arduino.port_name)


    while True:
        gui.update_window(transplanter.frame_arduino.status, transplanter.trays_need_replacing)

if __name__ == "__main__":
    main()

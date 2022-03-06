"""When run, this module makes the robot begin transplanting"""
from transplanter_robot import TransplanterRobot
from gui import GUI
from tray import Tray
from frame_arduino import FrameArduino
from toolhead_arduino import ToolheadArduino

def main():
    """Run the transplanter"""
    source_tray = Tray('dense_tray.json')
    destination_tray = Tray('sparse_tray.json', source_tray.get_width())
    frame_arduino = FrameArduino()
    toolhead_arduino = ToolheadArduino()
    transplanter = TransplanterRobot(source_tray, destination_tray, frame_arduino, toolhead_arduino)
    gui = GUI(transplanter.transplant, transplanter.end, transplanter.continue_transplant)
    gui.label_ports(toolhead_arduino.port_name, frame_arduino.port_name)


    while True:
        gui.update_window(transplanter.frame_arduino.status, transplanter.trays_need_replacing)

if __name__ == "__main__":
    main()

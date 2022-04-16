"""The main function class - you run it with python3 main.py"""
import configparser
from tray import Tray

def main():
    config = configparser.ConfigParser()
    config.read('configfile.ini')
    destination_tray = Tray(config["JSON_FILES"]["destination_tray"])
    source_tray = Tray(config["JSON_FILES"]["source_tray"])
    while not destination_tray.is_tray_full():
        print(destination_tray.get_next_hole())

if __name__ == "__main__":
    main()
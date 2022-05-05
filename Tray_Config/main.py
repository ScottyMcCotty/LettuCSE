"""The main function class - you run it with python3 main.py"""
import configparser
from tkinter import Tk
from windowHandler import windowHandler


def main():
    config = configparser.ConfigParser()
    config.read('configfile.ini')

    tkinter_instance = Tk()

    window_maker = windowHandler(tkinter_instance)

    gui_window = window_maker.window


    while True:
        gui_window.update()

if __name__ == "__main__":
    main()

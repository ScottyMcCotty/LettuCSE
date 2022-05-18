"""This module contains the Tray class"""

import json

class Tray:
    """
    A class to represent the trays that the plants are being moved from,
    and determine whether the tray is full and which is the next hole to
    be moved to

    ...

    Attributes
    ----------
    json_file_link : str
        a relative path the the json file with the data on the
        particular tray
    hole_iterator : int
        which hole to return data on - this is incremented every time
        until the tray is full
    hole_location_map : map
         A python map which maps the nth hole to the nth hole's location,
         lists the number of holes in the tray, and how far the tray is from the motor
         (the destination tray is farther from the motor becuase the source tray
         is in the way)

    Methods
    -------
    get_next_hole()
        gets a tuple with the x and y coordinates of the next tray hole, increment
        the hole_itterator
    is_tray_full()
        determines if the tray is full and needs replacing
    """

    json_file_link = ''
    hole_iterator = 0
    hole_location_map = {}

    def __init__(self, json_link):
        self.json_file_link = json_link
        with open(json_link, encoding='UTF-8') as tray_data:
            self.hole_location_map = json.load(tray_data)
        tray_data.close()

    def get_next_hole(self) -> tuple:
        """get an integer tuple representing the x and y values in mm of the place the
           motor needs to go. Measurement is in absolute coordinates, not motor coordinates.
           Tuple is converted from a string tuple to a float tuple
        """
        hole_x_value =  float(self.hole_location_map.get(str(self.hole_iterator))[0])
        hole_y_value =  float(self.hole_location_map.get(str(self.hole_iterator))[1])
        adjusted_hole_x_value = hole_x_value + float(self.hole_location_map.get("width_of_source_tray")) +float(self.hole_location_map.get("width_offset_distance"))
        adjusted_hole_y_value = hole_y_value + float(self.hole_location_map.get("height_offset_distance"))

        next_hole = (adjusted_hole_x_value, adjusted_hole_y_value)

        if self.hole_iterator+1 == int(self.hole_location_map.get("holes")):
            self.hole_iterator = 0
        else:
            self.hole_iterator += 1
        return next_hole

    def is_tray_full(self) -> bool:
        """return whether all holes have been visited and it is time
           for the tray to be replaced"""
        return self.hole_iterator == int(self.hole_location_map.get("holes")) - 1

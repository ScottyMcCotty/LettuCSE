"""This module contains the Tray class"""

import json

class Tray:

    """
    A class to represent the trays being used to hold the lettuce - all units in milimeters

    ...

    Attributes
    ----------
    json_link : string
        a link to the json file with the infornmations
    hole_side_length: float
        side length of the squares that the plant is in
    short_axis_distance: float
        distance between columns
    short_axis_distance: float
        distance between columns
    short_axis_distance_to_edge: float
        distance between edge of the board and first column of holes
    long_axis_distance_to_edge: float
        distance between edge of the board and first row of holes
    extra_gap: float
        distance length-wise between the clumps of holes   

    Methods
    -------
    ith_hole_x(i):
        Finds the x location of the ith hole of the given tray in mm
    ith_hole_y(i):
        Finds the y location of the ith hole of the given tray in mm
    ith_hole_location():
        Finds the (x,y) location of the ith hole of the given tray in mm
    get_width():
        Finds the width of the tray from the given JSON file
    get_length():
        Finds the length of the tray from the given JSON file
    """
    json_link = ''
    hole_side_length = 0
    short_axis_distance = 0
    long_axis_distance = 0
    short_axis_distance_to_edge = 0
    long_axis_distance_to_edge = 0
    extra_gap = 0
    columns = 0
    shift_right = 0

    def __init__(self, json_link, shift_right=0):
        self.json_link = json_link
        tray_data = open(json_link)
        tray_values = json.load(tray_data)

        self.hole_side_length = tray_values['hole_size']
        self.short_axis_distance = tray_values['short_axis_distance']
        self.long_axis_distance = tray_values['long_axis_distance']
        self.short_axis_distance_to_edge = tray_values['short_axis_distance_to_edge']
        self.long_axis_distance_to_edge = tray_values['long_axis_distance_to_edge']
        self.extra_gap = tray_values['extra_gap']
        self.columns = tray_values['columns']
        self.rows = tray_values['rows']
        self.rows_between_gap = tray_values['rows_between_gap']
        self.shift_right = shift_right


    def ith_hole_x(self, i):
        '''
        Finds the x location of the ith hole of the given tray in mm.
        Holes in the tray are numbered right to left, then top to bottom.
        i = 0 is the top left hole

            Parameters:
                    i (int): an integer representing which hole is being located
            Returns:
                    (int): the distance between the given hole and the right side
                    of the frame, in milimeters
        '''
        column_number = i% self.columns
        total_gap = self.short_axis_distance*column_number
        total_hole_width = self.hole_side_length*column_number + column_number/2
        return total_gap + total_hole_width + self.short_axis_distance_to_edge*2 + self.shift_right

    def ith_hole_y(self, i):
        '''
            Finds the y location of the ith hole of the given tray in mm. Holes in the
            tray are numbered right to left, then top to bottom.
            i = 0 is the top left hole

            Parameters:
                    i (int): an integer representing which hole is being located
            Returns:
                    (int): the distance between the given hole, and the top of the frame,
                    in milimeters
        '''
        row_number = i//self.columns
        thicker_rows = row_number%self.rows_between_gap

        total_gap = self.long_axis_distance*(row_number-thicker_rows)+self.extra_gap*(thicker_rows)
        total_hole_distance = self.hole_side_length*row_number + row_number/2
        return total_gap + total_hole_distance + self.long_axis_distance_to_edge*2

    def ith_hole_location(self, i):
        '''
            Finds the (x,y) location of the ith hole of the given tray in mm.
            Holes in the tray are numbered right to left, then top to bottom.
            i = 0 is the top left hole

            Parameters:
                    i (int): an integer representing which hole is being located
            Returns:
                    (int tuple): the location of the given hole, with location (0,0)
                    being the top left and the units in milimeters
        '''
        return self.ith_hole_x(i), self.ith_hole_y(i)

    def get_width(self):
        '''
            Finds the width of the tray from the given JSON file
            Parameters:
                    None

            Returns:
                    (int): tray width in milimeters
        '''
        edges = self.short_axis_distance_to_edge*2
        holes = self.hole_side_length*self.columns
        distances = self.short_axis_distance*(self.columns-1)
        return edges + holes + distances

    def get_length(self):
        '''
            Finds the length of the tray from the given JSON file

            Parameters:
                    None

            Returns:
                    (int): tray length in milimeters
        '''
        edges = self.long_axis_distance_to_edge*2
        holes = self.hole_side_length*self.rows
        regular_distances = self.long_axis_distance*(self.rows-(self.rows//self.rows_between_gap))
        gaps = self.extra_gap*(self.rows//self.rows_between_gap-1)
        return edges + holes + regular_distances + gaps

    def get_number_of_holes(self):
        """Returns total number of holes in tray"""
        return self.columns*self.rows

import json

class Tray:
    json_link = ''
    hole_size = 0
    horizontal_distance = 0
    vertical_distance = 0
    horizontal_distance_to_edge = 0
    vertical_distance_to_edge = 0
    extra_gap = 0
    columns = 0
    shift_right = 0

    mm_per_motor_step = 0.14 
    def __init__(self, json_link, shift_right=0):
        self.json_link = json_link
        tray_data = open(json_link)
        tray_values = json.load(tray_data)

        self.hole_size = tray_values['hole_size']
        self.horizontal_distance = tray_values['horizontal_distance']
        self.vertical_distance = tray_values['vertical_distance']
        self.horizontal_distance_to_edge = tray_values['horizontal_distance_to_edge']
        self.vertical_distance_to_edge = tray_values['vertical_distance_to_edge']
        self.extra_gap = tray_values['extra_gap']
        self.columns = tray_values['columns']
        self.rows = tray_values['rows']
        self.rows_between_gap = tray_values['rows_between_gap']
        self.shift_right = shift_right


    def ith_hole_x(self, i):
        column_number = i% self.columns
        total_horizontal_distance = self.horizontal_distance*column_number
        total_hole_distance = self.hole_size*column_number + column_number/2
        total_milimeters =  total_horizontal_distance + total_hole_distance + self.horizontal_distance_to_edge*2 + self.shift_right
        return round(total_milimeters/self.mm_per_motor_step)

    def ith_hole_y(self, i):
        row_number = i//self.columns
        thicker_rows = row_number%self.rows_between_gap

        total_vertical_distance = self.vertical_distance*(row_number-thicker_rows) + self.extra_gap*(thicker_rows)
        total_hole_distance = self.hole_size*row_number + row_number/2
        total_milimeters =  total_vertical_distance + total_hole_distance + self.vertical_distance_to_edge*2
        return round(total_milimeters/self.mm_per_motor_step)

    def ith_hole_location(self, i):
        return self.ith_hole_x(i), self.ith_hole_y(i)

    def get_width(self):
        edges = self.horizontal_distance_to_edge*2
        holes = self.hole_size*self.columns
        distances = self.horizontal_distance*(self.columns-1)
        return edges + holes + distances

    def get_number_of_holes(self):
        return self.columns*self.rows
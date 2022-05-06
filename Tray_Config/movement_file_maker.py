import json

class movement_file_maker():

    output_file_name = None
    hole_length = None
    hole_width = None
    short_axis_distance = None
    long_axis_distance = None
    short_axis_distance_to_edge = None
    long_axis_distance_to_edge = None
    rows = None
    columns = None
    rows_between_gap = None
    extra_gap = None

    def __init__(self, fN, hL, hW, sAD, lAD, sADtE, lADtE, row, col, rBG, eG):
        if fN == "Source":
            self.output_file_name = "source_tray.json"
        elif fN == "Destination":
            self.output_file_name = "destination_tray.json"
        else:
            return
        self.hole_length = hL
        self.hole_width = hW
        self.short_axis_distance = sAD
        self.long_axis_distance = lAD
        self.short_axis_distance_to_edge = sADtE
        self.long_axis_distance_to_edge = lADtE
        self.rows = row
        self.columns = col
        self.rows_between_gap = rBG
        self.extra_gap = eG


    def ith_hole_x(self, i) -> float:
        # Instead of i% self.columns, it's columns - i%self.columns to reflect order going from left to right
        # instead of right to left.
        column_number = (self.columns - 1) - (i% self.columns)
        total_gap = self.short_axis_distance*column_number
        # use hole_length or hole_width?
        total_hole_width = self.hole_width*column_number + column_number/2
        return total_gap + total_hole_width + self.short_axis_distance_to_edge*2

    def ith_hole_y(self, i:int) -> float:
        row_number = i//self.columns
        if self.rows_between_gap > 0:
            thicker_rows = row_number%self.rows_between_gap
        else:
            thicker_rows = 0

        total_gap = self.long_axis_distance*(row_number-thicker_rows)+self.extra_gap*(thicker_rows)
        # use hole_length or hole_width?
        total_hole_distance = self.hole_length*row_number + row_number/2
        return total_gap + total_hole_distance + self.long_axis_distance_to_edge*2

    def ith_hole_location(self, i) -> tuple:
        return '["' + str(round(self.ith_hole_x(i), 3)) + '","' + str(round(self.ith_hole_y(i), 3)) + '"]'

    def get_width(self) -> float:
        
        #TODO the +6 is atrocious, put it in a config file or something dear lord
        edges = self.short_axis_distance_to_edge*2
        holes = self.hole_width*self.columns
        distances = self.short_axis_distance*(self.columns-1)
        return edges + holes + distances + 6

    def get_number_of_holes(self) -> int:
        """Returns total number of holes in tray"""
        return self.columns*self.rows

    def create_movement_file(self, end_row, end_col, ignored_holes) -> None:
        """Creates a JSON file with generated coordinates based on the parameters and stored tray information."""
        file_info = {}
        coord = []
        # Only create coordinates up to the end row and end column.
        for m in range (0,(end_row - 1) * self.columns + end_col):
            if m not in ignored_holes:
                coord = [str(round(self.ith_hole_x(m), 3)), str(round(self.ith_hole_y(m), 3))]
                file_info[str(m)] = coord

        holes = str(self.get_number_of_holes())
        file_info["holes"] = holes
        distance = str(self.get_width())
        file_info["distance_from_bottom"] = distance
        
        with open(self.output_file_name, 'w') as output:
            json.dump(file_info, output, indent = 4)

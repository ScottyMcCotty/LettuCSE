from curses import beep


class movement_file_maker():

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

    def __init__(self, hL, hW, sAD, lAD, sADtE, lADtE, row, col, rBG, eG):
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
        column_number = i% self.columns
        total_gap = self.short_axis_distance*column_number
        # use hole_length or hole_width?
        total_hole_width = self.hole_side_length*column_number + column_number/2
        return total_gap + total_hole_width + self.short_axis_distance_to_edge*2

    def ith_hole_y(self, i:int) -> float:
        row_number = i//self.columns
        thicker_rows = row_number%self.rows_between_gap

        total_gap = self.long_axis_distance*(row_number-thicker_rows)+self.extra_gap*(thicker_rows)
        # use hole_length or hole_width?
        total_hole_distance = self.hole_side_length*row_number + row_number/2
        return total_gap + total_hole_distance + self.long_axis_distance_to_edge*2

    def ith_hole_location(self, i) -> tuple:
        return '["' + str(round(self.ith_hole_x(i), 3)) + '","' + str(round(self.ith_hole_y(i), 3)) + '"]'

    def get_width(self) -> float:
        
        #TODO the +6 is atrocious, put it in a config file or something dear lord
        edges = self.short_axis_distance_to_edge*2
        holes = self.hole_side_length*self.columns
        distances = self.short_axis_distance*(self.columns-1)
        return edges + holes + distances + 6

    def get_number_of_holes(self) -> int:
        """Returns total number of holes in tray"""
        return self.columns*self.rows

    def create_movement_file(self) -> None:
        for m in range (0,columns*rows):
            print('"' + str(m) + '":' + str(ith_hole_location(m)) + ',')
        print('holes:' + '"' + str(get_number_of_holes()) + '",')
        print('distance_from_bottom:' + str(get_width()))

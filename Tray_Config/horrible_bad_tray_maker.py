hole_side_length = 32.3
short_axis_distance = 12.6
long_axis_distance = 21.4
short_axis_distance_to_edge = 33.1
long_axis_distance_to_edge = 47.4
extra_gap = 29.3
columns = 12
rows = 15
rows_between_gap = 5


def ith_hole_x(i) -> float:
    column_number = i% columns
    total_gap = short_axis_distance*column_number
    total_hole_width = hole_side_length*column_number + column_number/2
    return total_gap + total_hole_width + short_axis_distance_to_edge*2

def ith_hole_y(i:int) -> float:
    row_number = i//columns
    thicker_rows = row_number%rows_between_gap

    total_gap = long_axis_distance*(row_number-thicker_rows)+extra_gap*(thicker_rows)
    total_hole_distance = hole_side_length*row_number + row_number/2
    return total_gap + total_hole_distance + long_axis_distance_to_edge*2

def ith_hole_location(i) -> tuple:
    return '["' + str(round(ith_hole_x(i), 3)) + '","' + str(round(ith_hole_y(i), 3)) + '"]'

def get_width() -> float:
    
    #TODO the +6 is atrocious, put it in a config file or something dear lord
    edges = short_axis_distance_to_edge*2
    holes = hole_side_length*columns
    distances = short_axis_distance*(columns-1)
    return edges + holes + distances + 6

def get_number_of_holes() -> int:
    """Returns total number of holes in tray"""
    return columns*rows

for m in range (0,columns*rows):
    print('"' + str(m) + '":' + str(ith_hole_location(m)) + ',')
print('holes:' + '"' + str(get_number_of_holes()) + '",')
print('distance_from_bottom:' + str(get_width()))

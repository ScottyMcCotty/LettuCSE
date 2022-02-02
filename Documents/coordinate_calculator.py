source_border_x = 5
source_border_y = 5
source_hole_distance_x = 5
source_hole_distance_y = 5
source_hole_width = 5
source_hole_height = 5
destination_border_x = 5
destination_border_y = 5
destination_hole_distance_x = 5
destination_hole_distance_y = 5
destination_hole_width = 5
destination_hole_height = 5
random_wide_distance_source = 5
random_wide_distance_destination = 5

source_list = []
destination_list = []


def get_x_source(i):
    width_of_holes = source_hole_width*i
    width_of_inbetween = source_hole_distance_x*(i-1)
    return width_of_holes + width_of_inbetween + source_border_x

def get_y_source(i):
    height_of_holes = source_hole_height*i
    height_of_inbetween = source_hole_distance_x*(i-1)
    extra_gap = (i+1)//5*random_wide_distance_source-1

    return height_of_holes + height_of_inbetween + source_border_y + extra_gap

def get_x_destination(i):
    width_of_holes = destination_hole_width*i
    width_of_inbetween = destination_hole_distance_x*(i-1)
    width_of_source_tray = source_border_x*2+source_hole_distance_x*11+source_hole_width*12
    return width_of_holes + width_of_inbetween + destination_border_x + width_of_source_tray

def get_y_destination(i):
    height_of_holes = destination_hole_height*i
    height_of_inbetween = destination_hole_distance_y*(i-1)
    extra_gap = (i+1)//3*random_wide_distance_destination
    return height_of_holes + height_of_inbetween + destination_border_y + extra_gap


for i in range(1,12):
    for j in range(1,15):
        source_list.append((get_x_source(i), get_y_source(j)))


for i in range(4):
    for j in range(1,6):
        for k in range(1,9):
            destination_list.append((get_x_destination(j), get_y_destination(k)))


for i in range(len(source_list)):
    print("Move " + str(source_list[i]) + " to " + str(destination_list[i]))

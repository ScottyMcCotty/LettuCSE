from tkinter import Tk, Label, CENTER, LEFT

class tray_info():
    tray_name = None
    hole_length = None
    hole_width = None
    short_axis_distance = None
    short_axis_distance_to_edge = None
    long_axis_distance = None
    long_axis_distance_to_edge = None
    extra_gap = None
    rows = None
    columns = None
    rows_between_gap = None

    window = None
    tray_name_text = None
    hole_length_text = None
    hole_width_text = None
    short_axis_distance_text = None
    short_axis_distance_to_edge_text = None
    long_axis_distance_text = None
    long_axis_distance_to_edge_text = None
    extra_gap_text = None
    rows_text = None
    columns_text = None
    rows_between_gap_text = None

    info_label = None

    def __init__(self, tkinter_object:Tk):
        self.tray_name = "Placeholder"
        self.hole_length = -1.0
        self.hole_width = -1.0
        self.short_axis_distance = -1.0
        self.short_axis_distance_to_edge = -1.0
        self.long_axis_distance = -1.0
        self.long_axis_distance_to_edge = -1.0
        self.extra_gap = -1.0
        self.rows = -1
        self.columns = -1
        self.rows_between_gap = -1

        self.window = tkinter_object
        self.info_label = Label(self.window, text = "N/A")

    def update_info(self):
        # Go through all held info and instantiate their text lines
        self.tray_name_text = "Tray type:\t\t\t\t"
        if self.tray_name == "Source":
            self.tray_name_text += "Source      "
        elif self.tray_name == "Destination":
            self.tray_name_text += "Destination"
        else:
            self.tray_name_text += "TBD          "
        
        self.hole_length_text = "Hole length:\t\t\t\t"
        if self.hole_length == -1.0:
            self.hole_length_text += "TBD"
        else:
            self.hole_length_text += str(self.hole_length)

        self.hole_width_text = "Hole width:\t\t\t\t"
        if self.hole_width == -1.0:
            self.hole_width_text += "TBD"
        else:
            self.hole_width_text += str(self.hole_width)

        self.short_axis_distance_text = "Short axis distance:\t\t\t"
        if self.short_axis_distance == -1.0:
            self.short_axis_distance_text += "TBD"
        else:
            self.short_axis_distance_text += str(self.short_axis_distance)

        self.short_axis_distance_to_edge_text = "Short axis distance to edge:\t\t\t"
        if self.short_axis_distance_to_edge == -1.0:
            self.short_axis_distance_to_edge_text += "TBD"
        else:
            self.short_axis_distance_to_edge_text += str(self.short_axis_distance_to_edge)

        self.long_axis_distance_text = "Long axis distance:\t\t\t"
        if self.long_axis_distance == -1.0:
            self.long_axis_distance_text += "TBD"
        else:
            self.long_axis_distance_text += str(self.long_axis_distance)

        self.long_axis_distance_to_edge_text = "Long axis distance to edge:\t\t\t"
        if self.long_axis_distance_to_edge == -1.0:
            self.long_axis_distance_to_edge_text += "TBD"
        else:
            self.long_axis_distance_to_edge_text += str(self.long_axis_distance_to_edge)

        self.extra_gap_text = "Additional gap length:\t\t\t"
        if self.extra_gap == -1.0:
            self.extra_gap_text += "TBD"
        elif self.extra_gap < -1:
            self.extra_gap_text += "N/A"
        else:
            self.extra_gap_text += str(self.extra_gap)

        self.rows_text = "Number of rows:\t\t\t\t"
        if self.rows == -1:
            self.rows_text += "TBD"
        else:
            self.rows_text += str(self.rows)
        
        self.columns_text = "Number of columns:\t\t\t"
        if self.columns == -1:
            self.columns_text += "TBD"
        else:
            self.columns_text += str(self.columns)
        
        self.rows_between_gap_text = "Number of rows between additional gaps:\t" # 41 CHARS
        if self.rows_between_gap == -1:
            self.rows_between_gap_text += "TBD"
        elif self.rows_between_gap < -1:
            self.rows_between_gap_text += "N/A"
        else:
            self.rows_between_gap_text += str(self.rows_between_gap)

        # Now that all information is updated, display it on the Tkinter object
        self.info_label.config(text = self.tray_name_text + "\n"
                               + self.hole_length_text + "\n"
                               + self.hole_width_text + "\n"
                               + self.short_axis_distance_text + "\n"
                               + self.long_axis_distance_text + "\n"
                               + self.short_axis_distance_to_edge_text + "\n"
                               + self.long_axis_distance_to_edge_text + "\n"
                               + self.rows_text + "\n"
                               + self.columns_text + "\n"
                               + self.extra_gap_text + "\n"
                               + self.rows_between_gap_text,
                               font = ("Arial", 10),
                               justify = LEFT,
                               bg = 'light green')
        self.info_label.place_forget()
        self.info_label.place(relx = 0.8, rely = 0.86, anchor = CENTER)

    def hide_label(self) -> None:
        self.info_label.place_forget()
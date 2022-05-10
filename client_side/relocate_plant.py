"""Module contains the RelocatePlant class"""


class RelocatePlant():
    """
    Creates a function that moves a plant from the source to the destination
    ...

    Attributes
    ----------
    go_behind_cup : function
        a received function which moves the toolhead a distance behind the cup hole
        so the cup can be slid on or off.
    go_to_cup : function
        go directly to the cup location in the xy plane
    raise_toolhead : function
        signals the toolhead arduino to go up
    lower_toolhead : function
        signals the toolhead arduino to go down

    Methods
    ----------
    transport_plant ()
        calls the attribute functions in the proper order
        to move from one location to another.
    reset_toolhead()
        raise the toolhead and send it to the origin
    """

    go_behind_cup = None
    go_to_cup = None
    raise_toolhead = None
    lower_toolhead = None
    go_to_origin = None
    width_of_source_tray = None

    def __init__(self, go_behind_cup, go_to_cup, raise_toolhead, lower_toolhead, go_to_origin) -> None:
        self.lower_toolhead = lower_toolhead
        self.go_behind_cup = go_behind_cup
        self.go_to_cup = go_to_cup
        self.raise_toolhead = raise_toolhead
        self.go_to_origin = go_to_origin


    def transport_plant(self, source:tuple, destination:tuple):
        """Get the toolhead to go from a raised position, move
            a plant from the source to the destination, and again
            enter a raised position. For all the destinations, an x
            value is added to compensate for the width of the source tray
            so that the toolhead recognizes that it needs to go further back 
            for the destination trays"""
        self.go_to_cup(source)
        
        self.go_behind_cup(source)
        self.lower_toolhead()
        self.go_to_cup(source)
        self.raise_toolhead()
        self.go_to_cup((float(destination[0]), destination[1]))
        self.lower_toolhead()
        self.go_behind_cup((float(destination[0]), destination[1]))
        self.raise_toolhead()
        
    def reset_transplanter(self):
        """Raise the toolhead and go to the origin"""
        self.go_to_origin()
        self.raise_toolhead()

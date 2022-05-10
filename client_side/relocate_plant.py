"""Module contains the RelocatePlant class"""


from time import sleep


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
            enter a raised position. The sleep commands serve the dual
            purpose of ensuring the toolhead does not lower while
            it is moving, which would crush the plants, and making
            the video look a bit cleaner."""
        self.go_behind_cup(source)
        sleep(7.5)
        self.lower_toolhead()
        sleep(1.5)
        self.go_to_cup(source)
        sleep(0.25)
        self.raise_toolhead()
        sleep(1.5)
        self.go_to_cup(destination)
        sleep(10)
        self.lower_toolhead()
        sleep(1.5)
        self.go_behind_cup(destination)
        sleep(0.5)
        self.raise_toolhead()
        sleep(1.5)

    def reset_transplanter(self):
        """Raise the toolhead and go to the origin"""
        self.go_to_origin()
        self.raise_toolhead()

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
    """

    go_behind_cup = None
    go_to_cup = None
    raise_toolhead = None
    lower_toolhead = None

    def __init__(self, go_behind_cup, go_to_cup, raise_toolhead, lower_toolhead) -> None:
        self.lower_toolhead = lower_toolhead
        self.go_behind_cup = go_behind_cup
        self.go_to_cup = go_to_cup
        self.raise_toolhead = raise_toolhead

    def transport_plant(self, source:tuple, destination:tuple):
        """Get the toolhead to go from a raised position, move
            a plant from the source to the destination, and again
            enter a raised position"""
        self.go_behind_cup(source)
        self.lower_toolhead()
        self.go_to_cup(source)
        self.raise_toolhead()
        self.go_to_cup(destination)
        self.lower_toolhead()
        self.go_behind_cup(destination)
        self.raise_toolhead()

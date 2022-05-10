"""Module contains the Transplanter class"""


class Transplanter():
    """
    This class deals with starting, stopping, pausing, and continuing the transplanter.
    Is is also the place that 'discoveres' when it is time for things to pause. 
    ...

    Attributes
    ----------
        paused : boolean
            this pauses the transplanting process while the human
            monitor comes and replaces the tray
        source_is_full : function
            a function which indicates that the source tray is full
        dest_is_full : function
            a function which indicates that the destination tray is full
        next_source_hole : function
            a function which returns a tuple which represents the next location to take a plant from
        next_dest_hole : function
            a function which returns a tuple which represents the next location to take a plant to
        reset : function
            this resets the device and moves the toolhead back to the origin
        transport : function
            moves a plant from hole a to hole b
    Methods
    ----------
    transplant()
        runs the transplanter, pauses and stops when needed
    continue_transplant()
        the transplanter automatically pauses when the trays are full.
        This function makes them continue
    """
    paused = False
    stopped = False

    source_is_full = None
    dest_is_full = None
    next_source_hole = None
    next_dest_hole = None
    reset = None
    transport = None

    def __init__(self, source_is_full, dest_is_full, next_source_hole,
                        next_dest_hole,
                        reset,
                        transport) -> None:
        self.source_is_full = source_is_full
        self.dest_is_full = dest_is_full
        self.next_source_hole = next_source_hole
        self.next_dest_hole = next_dest_hole
        self.reset = reset
        self.transport = transport

    def transplant(self):
        """
            Run the transplanter until things are stopped. Take a break when
            the trays are full
        """
        self.stopped = False
        self.paused = False
        while not self.stopped:
            if not self.paused:
                if self.source_is_full() or self.dest_is_full():
                    self.paused = True
                print(float(self.next_dest_hole()[0]))
                self.transport((float(self.next_source_hole()[0]), float(self.next_source_hole()[1])), (float(self.next_dest_hole()[0]), float(self.next_dest_hole()[1])))

    def continue_transplant(self):
        """permanantly end the whole process"""
        self.paused = False

    def stop(self):
        """Causes the transplant function to stop running, resets everything"""
        self.stopped = True
        self.reset()

    def restart(self):
        """If you want to run the transplanter after stopping it
        you need to reset the stop variable, so this does that
        """
        self.stopped = False

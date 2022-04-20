"""Module contains the GUI class"""

from tkinter import LEFT, RIGHT, Tk, Label

class PortNameLabel():
    """
    This class bundles all the 'junk' that comes with the tkinter class that doesn't need to
    be exposed to the GUI, such as size, title, etc.
    ...

    Attributes
    ----------
    toolhead_arudino_port_label : Tkinter Label
        label displaying the port that the toolhead arduino is connected to
    frame_arudino_port_label : Tkinter Label
        label displaying the port that the frame arduino is connected to
    """

    def __init__(self, tkinter_instance: Tk, toolhead_port: str, frame_port: str) -> None:

        self._toolhead_arudino_port_label = Label(tkinter_instance,
                                                 text = "Toolhead " + toolhead_port,
                                                 borderwidth=0,
                                                 bg="green")
        self._toolhead_arudino_port_label.place(relx = 0.22, rely = 0.975, anchor = 'e')

        self._frame_arudino_port_label = Label(tkinter_instance,
                                                 text = "Frame " + frame_port,
                                                 borderwidth=0,
                                                 bg="green")
        self._frame_arudino_port_label.place(relx = 0.78, rely = 0.975, anchor = 'w')


    @property
    def toolhead_arudino_port_label(self):
        """a label for showing where the toolhead arduino is connected"""
        return self.toolhead_arudino_port_label

    @property
    def frame_arudino_port_label(self):
        """a label for showing where the frame arduino is connected"""
        return self.frame_arudino_port_label

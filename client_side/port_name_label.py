"""Module contains the port name label class"""

from tkinter import Tk, Label

class PortNameLabel():
    """
    The ports are very finniky in the sense that they are computer dependent. Some people
    might have their ports set to private, or have some other odd configuration. However you
    can't really deal with it because if your code affects the permissions of other people's
    folders than you have made malware. So instead of dealing with it we just make it super
    easy to debug by having the names of the ports displayed on the GUI. These are the labels
    that display the ports!
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
                                                 bg="#AFD275")
        self._toolhead_arudino_port_label.place(relx = 0.22, rely = 0.975, anchor = 'e')

        self._frame_arudino_port_label = Label(tkinter_instance,
                                                 text = "Frame " + frame_port,
                                                 borderwidth=0,
                                                 bg="#AFD275")
        self._frame_arudino_port_label.place(relx = 0.78, rely = 0.975, anchor = 'w')


    @property
    def toolhead_arudino_port_label(self):
        """a label for showing where the toolhead arduino is connected"""
        return self.toolhead_arudino_port_label

    @property
    def frame_arudino_port_label(self):
        """a label for showing where the frame arduino is connected"""
        return self.frame_arudino_port_label

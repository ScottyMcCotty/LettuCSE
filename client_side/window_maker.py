"""Module contains the WindowMaker class"""

from tkinter import N, Tk, Label, PhotoImage

class WindowMaker():
    """
    This class bundles all the 'junk' that comes with the tkinter class that doesn't need to
    be exposed to the GUI, such as size, title, etc.
    ...

    Attributes
    ----------
    window : Tkinter Instance
        tkinter has an object instance that stores everything involving
        the GUI

    Methods
    -------
    set_window_to_paused()
        change the window color to red
    set_window_to_unpaused()
        change the window color to green
    """
    window = None


    def __init__(self, tkinter_instance:Tk) -> None:
        self.window = tkinter_instance
        self.window.title("LettuCSE Transplanter")
        self.window.geometry("1000x800")
        self.window.configure(bg='#AFD275')

        title_photo = PhotoImage(file='images/title.png')
        title_label = Label(self.window,image = title_photo, borderwidth=0,)
        self.window.image = title_photo
        title_label.place(relx = 0.5, rely = 0.02, anchor = N)

    def set_window_to_paused(self) -> None:
        """Makes the window red"""
        self.window.configure(bg='red')


    def set_window_to_unpaused(self) -> None:
        """Makes the window green"""
        self.window.configure(bg='green')

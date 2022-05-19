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
    """
    window = None

    def __init__(self, tkinter_instance:Tk) -> None:
        self.window = tkinter_instance
        self.window.title("LettuCSE Transplanter")
        self.window.geometry("1000x900")
        self.window.configure(bg='#AFD275')

        title_photo = PhotoImage(file='images/title.png')
        title_label = Label(self.window,image = title_photo, borderwidth=0,)
        self.window.image = title_photo
        title_label.place(relx = 0.5, rely = 0.02, anchor = N)

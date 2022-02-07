import tkinter as tk

class App():
     def __init__(self):
        super().__init__()
        inactive_message = "Repotter Currently Inactive"
        in_progress_message = "Repotting In Progress"
        dense_tray_replacement_message = "The Tray For Small Plants Is Full, Please Replace"
        sparse_tray_replacement_message = "The Tray For Large Plants Is Full, Please Replace"

        gui_window = tk.Tk()

        start_repotting = tk.Button(text="Begin Repotting",width=35,height=5,bg="gray", fg="black")
        shut_down = tk.Button(text="Stop Repotting",width=35,height=5,bg="gray",fg="black")
        tray_replaced = tk.Button(text="Tray Has Been Replaced, Continue Repotting", width=35, height=5, bg="gray", fg="black")

        start_repotting.pack()
        shut_down.pack()
        tray_replaced.pack()
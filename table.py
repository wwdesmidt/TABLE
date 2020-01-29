import tkinter as tk
import time


#full screen root window
root = tk.Tk()
root.attributes("-fullscreen", True)

#the table top canvas
table_top = tk.Canvas(root)
table_top.pack()






table_top.create_text(100, 100, text=f"mouse: ", tag="mouse_position")
table_top.create_text(100, 120, text=f"press escape to quit")











#function and keybind

def exit(event):
    root.quit()

def update_mouse_pos(event):
    #if theres more than one with this tag it stops working
    table_top.delete(table_top.find_withtag("mouse_position"))
    table_top.create_text(100, 100, text=f"{event}", tag="mouse_position")

root.bind_all("<Escape>", exit)

root.bind_all("<Motion>", update_mouse_pos)

table_top.mainloop()
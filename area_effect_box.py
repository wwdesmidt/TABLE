import tkinter as tk

# a popup window to create an area effect

class MeasureBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)







        #ok button
        ok_button = tk.Button(top, text="OK", command=self.ok)
        ok_button.pack()

        #cancel button
        cancel_button = tk.Button(top, text="Cancel", command=self.cancel)
        cancel_button.pack()



    def cancel(self):
        #if they clicked cancel return null
        self.result=None
        self.top.destroy()

    def ok(self):

        #values to send back
        #this is a fireball
        self.shape = "circle"
        self.radius = 20
        self.color = "red"

        self.top.destroy()
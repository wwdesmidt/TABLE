import tkinter as tk
from tkinter import ttk

# a popup window to create an area effect

class AreaEffectBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)


        self.symetrical = False

        #spinbox to get the number part
        height_label = tk.Label(top, text="Height")
        self.height_selection = tk.IntVar(value=5)
        height_input = tk.Spinbox(top, from_=1, to=100, textvariable=self.height_selection)
        height_label.pack()
        height_input.pack()


        def handle_width_selection():
            if self.symetrical==True:
                self.height_selection.set(self.width_selection.get())

        #spinbox to get the number part
        width_label = tk.Label(top, text="Width")
        self.width_selection = tk.IntVar(value=5)
        width_input = tk.Spinbox(top, from_=1, to=100, textvariable=self.width_selection, command=handle_width_selection)
        width_label.pack()
        width_input.pack()




        #radio buttons to choose shape
        shape_label = tk.Label(top, text="Shape")
        self.shape_selection = tk.StringVar()
        shape_combobox = ttk.Combobox(top, textvariable=self.shape_selection)
        shape_combobox["values"] = ("square", "rectangle", "circle", "oval")
        shape_label.pack()
        shape_combobox.pack()
        self.shape_selection.set("square")
        self.symetrical=True
        width_input.configure(state="disabled")


        def handle_shape_selection(event):
            if self.shape_selection.get() == "square" or self.shape_selection.get() == "circle":
                self.symetrical = True
                width_input.configure(state="disabled")
            elif self.shape_selection.get() == "rectangle" or self.shape_selection.get() == "oval":
                self.symetrical = False
                width_input.configure(state="normal")

        shape_combobox.bind("<<ComboboxSelected>>", handle_shape_selection)


        #option_feet = tk.Radiobutton(top, text="Circle", variable=self.shape_selection, value="circle")
        #option_miles = tk.Radiobutton(top, text="Square", variable=self.shape_selection, value="square")
        #option_feet.pack()
        #option_miles.pack()
    


# def handle_selection(event):
#     print(f"today is {selected_weekday.get()}")
#     print(weekday.current())

# weekday.bind("<<ComboboxSelected>>", handle_selection)





        color_label = tk.Label(top, text="Color")
        self.color_selection = tk.StringVar()
        color_combobox = ttk.Combobox(top, textvariable=self.color_selection)
        color_combobox["values"] = ("red","orange","yellow","green","blue","indigo","violet","black","white","grey")
        color_label.pack()
        color_combobox.pack()
        self.color_selection.set("red")


        #ok button
        ok_button = tk.Button(top, text="OK", command=self.ok)
        ok_button.pack()

        #cancel button
        cancel_button = tk.Button(top, text="Cancel", command=self.cancel)
        cancel_button.pack()



    def cancel(self):
        #if they clicked cancel return null
        self._return = False
        self.top.destroy()

    def ok(self):
        self._return = True
        self.shape = self.shape_selection.get()
        self.height = self.height_selection.get()
        #if the object is symmetrical return the height as the width
        if self.symetrical==True:
            self.width = self.height_selection.get()
        else:
            self.width = self.width_selection.get()
        self.color = self.color_selection.get()

        self.top.destroy()
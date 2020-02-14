import tkinter as tk
from tkinter import ttk

# a popup window to create an area effect

class AreaEffectBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)


        self.symmetrical = False
        self.radius = False

        #spinbox to get the number part
        height_label = tk.Label(top, text="Height")
        self.height_selection = tk.IntVar(value=5)
        height_input = tk.Spinbox(top, from_=1, to=100, textvariable=self.height_selection)
        height_label.pack()
        height_input.pack()



        #spinbox to get the number part
        width_label = tk.Label(top, text="Width")
        self.width_selection = tk.IntVar(value=5)
        width_input = tk.Spinbox(top, from_=1, to=100, textvariable=self.width_selection)
        width_label.pack()
        width_input.pack()


        #radio buttons to choose shape
        shape_label = tk.Label(top, text="Shape")
        self.shape_selection = tk.StringVar()
        shape_combobox = ttk.Combobox(top, textvariable=self.shape_selection)
        shape_combobox["values"] = ("Cone","Cube","Cylinder","Line","Sphere")
        shape_label.pack()
        shape_combobox.pack()
        self.shape_selection.set("Cube")
        self.symmetrical=True
        width_input.configure(state="disabled")


        def handle_shape_selection(event):
            if self.shape_selection.get() == "Cone":
                self.symmetrical=True
                self.radius=False
                width_input.configure(state="disabled")
                height_label.configure(text="Lengh")
                width_label.configure(text="")
                
            elif self.shape_selection.get() == "Cube":
                self.symmetrical=True
                self.radius=False
                width_input.configure(state="disabled")
                height_label.configure(text="Size")
                width_label.configure(text="")
                
            elif self.shape_selection.get() == "Cylinder":
                self.symmetrical=True
                self.radius=True
                width_input.configure(state="disabled")
                height_label.configure(text="Radius")
                width_label.configure(text="")
                
            elif self.shape_selection.get() == "Line":
                self.symmetrical=False
                self.radius=False
                width_input.configure(state="normal")
                height_label.configure(text="Width")
                width_label.configure(text="Length")
                
            elif self.shape_selection.get() == "Sphere":
                self.symmetrical=True
                self.radius=True
                width_input.configure(state="disabled")
                height_label.configure(text="Radius")
                width_label.configure(text="")
                

        shape_combobox.bind("<<ComboboxSelected>>", handle_shape_selection)


        #option_feet = tk.Radiobutton(top, text="Circle", variable=self.shape_selection, value="circle")
        #option_miles = tk.Radiobutton(top, text="Square", variable=self.shape_selection, value="square")
        #option_feet.pack()
        #option_miles.pack()
    


# def handle_selection(event):
#     print(f"today is {selected_weekday.get()}")
#     print(weekday.current())

# weekday.bind("<<ComboboxSelected>>", handle_selection)


        # preset_label = tk.Label(top, text="Presets")
        # self.preset_selection = tk.StringVar()
        # preset_combobox = ttx.Combobox(top, textvariable=self.preset_selection)
        # preset_combobox["values"] = ("fireball")


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
        if self.symmetrical==True:
            self.width = self.height_selection.get()
        else:
            self.width = self.width_selection.get()

        #if its a radius then double it for the full size
        if self.radius==True:
            self.width=self.width*2
            self.height=self.height*2

        self.color = self.color_selection.get()

        self.top.destroy()


'''
Cone
A cone extends in a direction you choose from its point of Origin. A cone’s width at a given point along its length is equal to that point’s distance from the point of Origin. A cone’s area of effect specifies its maximum length.
A cone’s point of Origin is not included in the cone’s area of effect, unless you decide otherwise.

Cube
You select a cube’s point of Origin, which lies anywhere on a face of the cubic effect. The cube’s size is expressed as the length of each side.
A cube’s point of Origin is not included in the cube’s area of effect, unless you decide otherwise.

Cylinder
A cylinder’s point of Origin is the center of a circle of a particular radius, as given in the spell description. The circle must either be on the ground or at the height of the spell effect. The energy in a Cylinder expands in straight lines from the point of Origin to the perimeter of the circle, forming the base of the Cylinder. The spell’s effect then shoots up from the base or down from the top, to a distance equal to the height of the Cylinder.

A cylinder’s point of Origin is included in the cylinder’s area of effect.

Line
A line extends from its point of Origin in a straight path up to its length and covers an area defined by its width.

A line’s point of Origin is not included in the line’s area of effect, unless you decide otherwise.

Sphere
You select a sphere’s point of Origin, and the Sphere extends outward from that point. The sphere’s size is expressed as a radius in feet that extends from the point.

A sphere’s point of Origin is included in the sphere’s area of effect.
'''
"Cone","Cube","Cylinder","Line","Sphere"
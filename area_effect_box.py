import tkinter as tk
from tkinter import ttk

# a popup window to create an area effect

class AreaEffectBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)


        self.symmetrical = False
        self.radius = False

        main_container = ttk.Frame(top)
        main_container.grid(sticky="nsew")

        #label and combo box for presets
        preset_label = tk.Label(main_container, text="Preset")
        self.preset_selection = tk.StringVar()
        preset_combobox = ttk.Combobox(main_container, textvariable=self.preset_selection)
        preset_combobox["values"] = ("","Fireball","Thunderwave","Lightning Bolt", "Cone of Cold")
        preset_label.grid(row=0, column=0, pady=5, padx=5, sticky="W")
        preset_combobox.grid(row=0, column=1, pady=5, padx=5)

        #load the preset info 
        # i wanna load these from a file eventually
        def handle_preset_selected(event):
            if self.preset_selection.get()=="Fireball":
                #set the shape selection and then invoke the shape handler
                #to set all the stuff that sets, tricky!
                self.shape_selection.set("Sphere")
                handle_shape_selection(event)
                self.height_selection.set(20)
                self.width_selection.set(20)
                self.color_selection.set("Red")

            if self.preset_selection.get()=="Thunderwave":
                self.shape_selection.set("Cube")
                handle_shape_selection(event)
                self.height_selection.set(15)
                self.width_selection.set(15)
                self.color_selection.set("Indigo")

            if self.preset_selection.get()=="Lightning Bolt":
                self.shape_selection.set("Line")
                handle_shape_selection(event)
                self.height_selection.set(5)
                self.width_selection.set(100)
                self.color_selection.set("Yellow")

            if self.preset_selection.get()=="Cone of Cold":
                self.shape_selection.set("Cone")
                handle_shape_selection(event)
                self.height_selection.set(60)
                self.width_selection.set(60)
                self.color_selection.set("Blue")

            #if they pick the blank one again, dont need to do anything
            else:
                pass

        #when they pick a preset call the preset event handler
        preset_combobox.bind("<<ComboboxSelected>>", handle_preset_selected)

        #spinbox to get the heignt
        height_label = tk.Label(main_container, text="Height")
        self.height_selection = tk.IntVar(value=5)
        height_input = tk.Spinbox(main_container, from_=1, to=100, textvariable=self.height_selection)
        height_label.grid(row=1, column=0, pady=5, padx=5, sticky="W")
        height_input.grid(row=1, column=1, pady=5, padx=5)



        #spinbox to get the width
        width_label = tk.Label(main_container, text="Width")
        self.width_selection = tk.IntVar(value=5)
        width_input = tk.Spinbox(main_container, from_=1, to=100, textvariable=self.width_selection)
        width_label.grid(row=2, column=0, pady=5, padx=5, sticky="W")
        width_input.grid(row=2, column=1, pady=5, padx=5)

        


        #combo box for shape
        shape_label = tk.Label(main_container, text="Shape")
        self.shape_selection = tk.StringVar()
        shape_combobox = ttk.Combobox(main_container, textvariable=self.shape_selection)
        shape_combobox["values"] = ("Cone","Cube","Cylinder","Line","Sphere")
        shape_label.grid(row=3, column=0, pady=5, padx=5, sticky="W")
        shape_combobox.grid(row=3, column=1, pady=5, padx=5)

        #set default shape values
        #can i call the event handler and just pass null as the event or something?
        self.shape_selection.set("Cube")
        self.symmetrical=True
        self.radius=False
        width_input.configure(state="disabled")
        height_label.configure(text="Size")
        width_label.configure(text="")

        #do various things with the fields depending on what shape the selected
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
                
        #when the pick a shape, call the shape event handler to mess witht he fields
        shape_combobox.bind("<<ComboboxSelected>>", handle_shape_selection)



        #combo box for picking color
        color_label = tk.Label(main_container, text="Color")
        self.color_selection = tk.StringVar()
        color_combobox = ttk.Combobox(main_container, textvariable=self.color_selection)
        color_combobox["values"] = ("Red","Orange","Yellow","Green","Blue","Indigo","Violet","Black","White","Grey")
        color_label.grid(row=4, column=0, pady=5, padx=5, sticky="W")
        color_combobox.grid(row=4, column=1, pady=5, padx=5)
        self.color_selection.set("red")

        #container so the buttons can have different columns than the rest of the fields
        button_container = ttk.Frame(main_container)
        button_container.grid(row=5, column=0, columnspan=2, sticky="NSWE")

        #cancel button
        cancel_button = tk.Button(button_container, text="Cancel", command=self.cancel, width="15")
        cancel_button.grid(row=0, column=0, pady=5, padx=(5,2.5))
        
        #ok button
        ok_button = tk.Button(button_container, text="OK", command=self.ok, width="15")
        ok_button.grid(row=0, column=1, pady=5, padx=(2.5,5))

        


    #if they clicked cancel return null
    def cancel(self):
        #this is how the calling progam can tell they clicked cancel
        self._return = False
        self.top.destroy()

    #if they clicked ok set all the values
    def ok(self):
        #this is how the calling program can tell they clicked ok
        self._return = True
        
        #set shape and height
        self.shape = self.shape_selection.get()
        self.height = self.height_selection.get()

        #if the object is symmetrical return the height as the width too
        #otherwise set he width 
        if self.symmetrical==True:
            self.width = self.height_selection.get()
        else:
            self.width = self.width_selection.get()

        #if its a radius then double it for the full size
        if self.radius==True:
            self.width=self.width*2
            self.height=self.height*2

        #set the color
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
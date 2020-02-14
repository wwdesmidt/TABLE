import tkinter as tk
from tkinter import ttk

# a popup window to get a unit of measure and measurement
# to be used in combination with dragging out a distance 
# to to set a distance scale on a map

class MeasureBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        instructions_label = tk.Label(top, text="After selecting a distance, click OK\nand draw a line that length on the map.")
        instructions_label.grid(row=0, column=0, columnspan=2)

        #main container for grid layout
        main_container = ttk.Frame(top)
        main_container.grid(sticky="NSEW")



        #spinbox to get the number part
        distance_label = tk.Label(main_container, text="Distance to set")
        self.distance_value = tk.IntVar(value=5)
        distance_spinbox = tk.Spinbox(main_container, from_=1, to=1000, textvariable=self.distance_value)
        distance_label.grid(row=1, column=0, pady=5, padx=5, sticky="W")
        distance_spinbox.grid(row=1, column=1, pady=5, padx=5)

        #radio buttons to choose between feet and miles
        unit_radio_button_frame = ttk.Frame(main_container)
        unit_radio_button_frame.grid(row=2, column=1)

        distance_units_label = tk.Label(main_container, text="Units")

        self.distance_units = tk.StringVar()
        option_feet = tk.Radiobutton(unit_radio_button_frame, text="Feet", variable=self.distance_units, value="feet")
        option_miles = tk.Radiobutton(unit_radio_button_frame, text="Miles", variable=self.distance_units, value="miles")

        distance_units_label.grid(row=2, column=0, pady=5, padx=5,sticky="W")
        option_feet.grid(row=0, column=0, padx=5)
        option_miles.grid(row=1, column=0, padx=5)
        self.distance_units.set("feet")

        # #ok button
        # ok_button = tk.Button(main_container, text="OK", command=self.ok)
        # ok_button.grid()

        # #cancel button
        # cancel_button = tk.Button(main_container, text="Cancel", command=self.cancel)
        # cancel_button.grid()

        #container so the buttons can have different columns than the rest of the fields
        button_container = ttk.Frame(main_container)
        button_container.grid(row=3, column=0, columnspan=2, sticky="NSWE")

        #cancel button
        cancel_button = tk.Button(button_container, text="Cancel", command=self.cancel, width="15")
        cancel_button.grid(row=0, column=0, pady=5, padx=(5,2.5))
        
        #ok button
        ok_button = tk.Button(button_container, text="OK", command=self.ok, width="15")
        ok_button.grid(row=0, column=1, pady=5, padx=(2.5,5))




    def cancel(self):
        #if they clicked cancel return null
        self.result=None
        self.top.destroy()

    def ok(self):

        #get values from widgets
        distance = self.distance_value.get()
        units = self.distance_units.get()

        #if the user input miles, convert to feet
        if units == "miles":
            distance = distance*5280
        
        #set the return value to be read in the main app
        self.result = distance

        self.top.destroy()



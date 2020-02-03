import tkinter as tk

# a popup window to get a unit of measure and measurement
# to be used in combination with dragging out a distance 
# to to set a distance scale on a map

class MeasureBox:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        tk.Label(top, text="Value").pack()

        #spinbox to get the number part
        self.distance_value = tk.IntVar(value=5)
        distance_input = tk.Spinbox(top, from_=1, to=1000, textvariable=self.distance_value)
        distance_input.pack()

        #radio buttons to choose between feet and miles
        self.distance_units = tk.StringVar()
        option_feet = tk.Radiobutton(top, text="Feet", variable=self.distance_units, value="feet")
        option_miles = tk.Radiobutton(top, text="Miles", variable=self.distance_units, value="miles")
        option_feet.pack()
        option_miles.pack()
        self.distance_units.set("feet")

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

        #get values from widgets
        distance = self.distance_value.get()
        units = self.distance_units.get()

        #if the user input miles, convert to feet
        if units == "miles":
            distance = distance*5280
        
        #set the return value to be read in the main app
        self.result = distance

        self.top.destroy()



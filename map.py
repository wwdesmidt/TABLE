from PIL import Image, ImageTk
import json
import pathlib
import os

class Map():
    def __init__(self, file_name, canvas):

        #store the canvas that we will br drawing the map to locally
        #as long as we never reassign it (self.canvas=whatever)
        #we can use it as a reference
        self.canvas = canvas

        #store the file name of the image in the class instance
        #we arent assuming it is a relative or absolute path
        self.file_name = file_name

        #get the absolute path for the map image
        self.image_file = pathlib.Path(self.file_name)

        #get the absolute path the json file (rules are same file name same directory)
        self.json_file = pathlib.Path(self.image_file.parent,self.image_file.stem+".json")

        #if the json file doesnt exist yet initialize it
        if not os.path.isfile(self.json_file):
            #initial json data
            #this needs to contain whatever is read below
            initial_json_data = {
                "image_file":self.image_file.name,
                "width_feet":1,
                "height_feet":1
            }
            with open(self.json_file, "w+") as f:
                json.dump(initial_json_data,f)




        #get the map image file name (dont know if we even need that
        # and width and height in feet out of the json file
        with open(self.json_file) as f:
            data = json.load(f)
            self.image_file_name = data["image_file"]
            self.map_width_feet = data["width_feet"]
            self.map_height_feet = data["height_feet"]



        self.map_image = Image.open(self.image_file)
        #self.map_width_feet = 9950000
        #self.map_height_feet  = 7550000

        #need to keep track of if we rotated the map, because if we did
        #we need to write the scale backwards
        self.rotated = False

        #rotate the image to fill the screen best
        #supports landscape and portrait monitors
        if self.canvas.winfo_screenwidth() > self.canvas.winfo_screenheight():
            if self.map_image.height > self.map_image.width:
                self.map_image = self.map_image.rotate(90, expand=True)
                self._tmp = self.map_width_feet
                self.map_width_feet = self.map_height_feet
                self.map_height_feet = self._tmp
                self.rotated = True
        else:
            if self.map_image.height < self.map_image.width:
                self.map_image = self.map_image.rotate(90, expand=True)
                self._tmp = self.map_width_feet
                self.map_width_feet = self.map_height_feet
                self.map_height_feet = self._tmp
                self.rotated = True

        #get the aspect ratios of the screen and the map
        self.screen_aspect_ratio = self.canvas.winfo_screenwidth()/self.canvas.winfo_screenheight()
        self.map_aspect_ratio = self.map_image.width/self.map_image.height



        #if the map is taller than the screen
        #resize height to screen height, and resize width based on image aspect ratio
        if self.map_aspect_ratio < self.screen_aspect_ratio:
            self.map_new_height = self.canvas.winfo_screenheight()
            self.map_new_width = int(self.map_new_height*(self.map_image.width/self.map_image.height))
        #otherwise do it the other way
        else:
            self.map_new_width =  self.canvas.winfo_screenwidth()
            self.map_new_height = int(self.map_new_width*(self.map_image.height/self.map_image.width))


        self.max_map_size = (self.map_new_width, self.map_new_height)
        self.map_image = self.map_image.resize(self.max_map_size)


        #get the photoimage after transformations
        self.map = ImageTk.PhotoImage(self.map_image)


        #now that the map is created and resized, calculate feet pet pixel
        #just using the width for this... height or width should both work
        #needs to be stored as one of the file dimensions instad of just 
        #having feet_per_pixel in the json file because of different screen resolutions
        self.map_feet_per_pixel = self.map_width_feet / self.map_image.width


    #simple method to just draw the map
    def draw_map(self):
        self.canvas.create_image(self.canvas.winfo_screenwidth()/2, self.canvas.winfo_screenheight()/2,image=self.map)

    #use a pixels per foot measurement from the main app to update 
    # the height and width of the map in the json file
    def set_distance(self, pixels_per_foot):

        #print(f"width:  {pixels_per_foot} / {self.map_new_width} = {pixels_per_foot/self.map_new_width}")
        #print(f"height: {pixels_per_foot} / {self.map_new_height} = {pixels_per_foot/self.map_new_height}")

        #print(f"width:  {self.map_new_width} / {pixels_per_foot}  = {self.map_new_width/pixels_per_foot}")
        #print(f"height: {self.map_new_height} / {pixels_per_foot}  = {self.map_new_height/pixels_per_foot}")
        
        #set the new values to the class member variables 
        # so they take immediately
        #self.map_width_feet = round(pixels_per_foot/self.map_new_width)
        #self.map_height_feet = round(pixels_per_foot/self.map_new_height)
        self.map_width_feet = round(self.map_new_width/pixels_per_foot)
        self.map_height_feet = round(self.map_new_height/pixels_per_foot)



        #open the current json file and pull out the data
        with open(self.json_file, "r") as f:
            json_data = json.load(f)

        #print(json_data)

        #update the width and height
        #(backwards if we rotated the map when displaying it)
        if self.rotated == True:
            json_data["height_feet"] = self.map_width_feet
            json_data["width_feet"] = self.map_height_feet
        else:
            json_data["width_feet"] = self.map_width_feet
            json_data["height_feet"] = self.map_height_feet

        #print(json_data)

        #write the new values back to the file
        with open(self.json_file, "w") as f:
            json.dump(json_data,f)

        #finally recalculate pixels per feet for the current instance
        self.map_feet_per_pixel = self.map_width_feet / self.map_image.width


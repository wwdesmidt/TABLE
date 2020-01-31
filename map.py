from PIL import Image, ImageTk
import json
from pathlib import Path, PurePath

class Map():
    def __init__(self, file_name, canvas):

        print(f"map class got file name: {file_name}")

        #map files and height and width in feet
        #eventually these will be bundled
        #maybe an image file + some json or xml with matching names?
        #distances in feet even for large maps (require units and add auto conversion?)

        #map_image = Image.open("./sample_assets/sample_dungeon_map.jpg")
        #map_width_feet = 105
        #map_height_feet  = 135

        self.canvas = canvas

        #self.map_image = Image.open("./sample_assets/sample_world_map.jpg")
        
        path = Path(file_name).parents[0]

        print(f"map class got path: {path}")

        #get the width and height out of the json file
        with open(file_name) as f:
            data = json.load(f)
            self.image_file_name = self.image_file_name = Path(path, data["image_file_name"])
            self.map_width_feet = data["width_feet"]
            self.map_height_feet  = data["height_feet"]

        print(f"map class got image file name: {self.image_file_name}")
        print(f"map class got map dimensions: {self.map_width_feet},{self.map_height_feet}")

        self.map_image = Image.open(self.image_file_name)
        #self.map_width_feet = 9950000
        #self.map_height_feet  = 7550000

        print(f"map class got image: {self.map_image}")

        #rotate the image to fill the screen best
        #supports landscape and portrait monitors
        if self.canvas.winfo_screenwidth() > self.canvas.winfo_screenheight():
            if self.map_image.height > self.map_image.width:
                self.map_image = self.map_image.rotate(90, expand=True)
                self._tmp = self.map_width_feet
                self.map_width_feet = self.map_height_feet
                self.map_height_feet = self._tmp
        else:
            if self.map_image.height < self.map_image.width:
                self.map_image = self.map_image.rotate(90, expand=True)
                self._tmp = self.map_width_feet
                self.map_width_feet = self.map_height_feet
                self.map_height_feet = self._tmp

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

        self.canvas.create_image(self.canvas.winfo_screenwidth()/2, self.canvas.winfo_screenheight()/2,image=self.map)


        #now that the map is created and resized, calculate feet pet pixel
        #could use height or width, using an average of the two for now incase ratios are off
        self.map_feet_per_pixel = ((self.map_height_feet / self.map_image.height) + (self.map_width_feet / self.map_image.width))/2


    def draw_map(self):
        self.canvas.create_image(self.canvas.winfo_screenwidth()/2, self.canvas.winfo_screenheight()/2,image=self.map)

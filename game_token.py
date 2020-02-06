import tkinter as tk
from map import Map
import uuid
from PIL import Image, ImageTk, ImageDraw

class GameToken:
    def __init__(self, file_name, canvas, map, x, y, radius, color):

        #generate a unique id for this token 
        #so we can find it and delete it when we move it
        self.id = uuid.uuid4()

        print(f"hi, im a token, my name is {self.id}")

        #file name for the image, not used yet
        self.file_name = file_name


        #the canvas that we will draw the token on
        self.canvas = canvas

        #the map we are drawing on, need this for size calculations (feet->pixels) etc.
        self.map = map

        #radius, this will be read from a json file eventually
        self.radius = radius
        self.radius_pixels = round(self.radius/self.map.map_feet_per_pixel)

        #where it is initially positioned... need to come up with something for this
        self.x = x
        self.y = y

        #outline color... also need to figure this out
        self.outline_color = color

        #image processing stuff
        self.image = Image.open(self.file_name)
        #make the image square and the right size
        self.image_size = (self.radius_pixels*2, self.radius_pixels*2)
        self.image = self.image.resize(self.image_size)
        #generate a new temporary image (black with a white circle) to use as an alpha mask
        mask = Image.new('L', self.image_size, 0)
        mask_draw = ImageDraw.Draw(mask) 
        mask_draw.ellipse((0, 0) + self.image_size, fill=255)
        self.image.putalpha(mask)
        #generate the photoimage to draw
        self.token = ImageTk.PhotoImage(self.image)


    #set the position of the token
    def set_position(self, x, y):
        self.x=x
        self.y=y

    def move(self, x, y):
        self.undraw()
        self.set_position(x,y)
        self.draw()

    #draw the token in its current position
    #doesnt take coords, use move to set position
    def draw(self):
        x1 = self.x - self.radius_pixels
        y1 = self.y - self.radius_pixels
        x2 = self.x + self.radius_pixels
        y2 = self.y + self.radius_pixels
        #use the unique id we generated in the constructor as the tag
        self.canvas.create_image(self.x, self.y,image=self.token, tag=self.id)
        #draw the border seperately, dont know why it wasnt working putting it directly on the image
        #(it was cutting off the right and bottom of the circle)
        self.canvas.create_oval(x1,y1,x2,y2, outline=self.outline_color, fill="", width="3", tag=self.id)

    
    #delete all instances of the token based on its unique id
    def undraw(self):
        for tmp_token in self.canvas.find_withtag(self.id):
            self.canvas.delete(tmp_token)


    #a method to determine if a set of x,y coords are "inside" the token
    def contains(self, x,y):
        x1 = self.x - self.radius_pixels
        y1 = self.y - self.radius_pixels
        x2 = self.x + self.radius_pixels
        y2 = self.y + self.radius_pixels

        if x > x1 and x < x2 and y > y1 and y < y2:
            return True
        else:
            return False


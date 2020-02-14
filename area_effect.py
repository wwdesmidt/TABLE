import tkinter as tk
from map import Map
import uuid
from PIL import Image, ImageTk
import cmath, math

class AreaEffect:
    def __init__(self, canvas, map, shape, height, width, color, x, y):

        #generate a unique id for this token 
        #so we can find it and delete it when we move it
        self.id = uuid.uuid4()


        self.canvas = canvas
        self.map = map
        self.shape = shape
        
        self.height = height
        self.width = width

        #do something stupid so it doesnt break
        self.radius = round((self.height+self.width)/2)

        self.color = color
        self.x = x
        self.y = y
        self.complex_angle=0.0
        self.radius_pixels = round(self.radius/self.map.map_feet_per_pixel)
        self.height_pixels = round(self.height/self.map.map_feet_per_pixel)
        self.width_pixels = round(self.width/self.map.map_feet_per_pixel)


    def draw(self):

        if self.shape=="circle" or self.shape=="oval":
            # x1 = self.x - self.radius_pixels
            # y1 = self.y - self.radius_pixels
            # x2 = self.x + self.radius_pixels
            # y2 = self.y + self.radius_pixels

            x1 = self.x - self.width_pixels/2
            x2 = self.x + self.width_pixels/2
            y1 = self.y - self.height_pixels/2
            y2 = self.y + self.height_pixels/2


            self.points=[(x1, y1), (x2, y2)]

            self.canvas.create_oval(self.points, outline=self.color, fill=self.color, width=3, tag=self.id)

        elif self.shape=="square" or self.shape=="rectangle":


            x1 = self.x - self.width_pixels/2
            y1 = self.y - self.height_pixels/2
            x2 = self.x + self.width_pixels/2
            y2 = self.y - self.height_pixels/2
            x3 = self.x + self.width_pixels/2
            y3 = self.y + self.height_pixels/2
            x4 = self.x - self.width_pixels/2
            y4 = self.y + self.height_pixels/2

            self.points=[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]

            if self.complex_angle == 0.0:
                self.canvas.create_polygon(self.points,outline=self.color, fill=self.color, width=3, tag=self.id )
            else:
                offset = complex(self.x, self.y)
                new_points = []
                for x, y in self.points:
                    v = self.complex_angle * (complex(x, y) - offset) + offset
                    new_points.append(v.real)
                    new_points.append(v.imag)
                    new_points.append((v.real,v.imag))

                self.canvas.create_polygon(new_points,outline=self.color, fill=self.color, width=3, tag=self.id )


    

    def rotate_by_mouse(self, mouse_x, mouse_y):
        self.undraw()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.complex_angle = complex(dx, dy)
        self.complex_angle = self.complex_angle / abs(self.complex_angle)
        self.draw()






    #delete all instances of the token based on its unique id
    def undraw(self):
        for tmp_token in self.canvas.find_withtag(self.id):
            self.canvas.delete(tmp_token)


    def move(self, x, y):
        self.undraw()
        self.x=x
        self.y=y
        self.draw()

    #a method to determine if a set of x,y coords are "inside" the area effect
    def contains(self, x,y):

        
        x1 = self.x - self.width_pixels/2
        y1 = self.y - self.height_pixels/2
        x2 = self.x + self.width_pixels/2
        y2 = self.y + self.height_pixels/2

        if x > x1 and x < x2 and y > y1 and y < y2:
            return True
        else:
            return False
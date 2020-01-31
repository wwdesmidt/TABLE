import tkinter as tk
import time
import math
from PIL import Image, ImageTk
from map import Map
from PIL import Image, ImageTk
import json

#try to set windows dpi awareness
#if it doesnt work (like if you arent on windows) just do nothing
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

#full screen root window
root = tk.Tk()
root.attributes("-fullscreen", True)

#the table top canvas
#make it the same size as the full screen window
table_top = tk.Canvas(root, width = root.winfo_screenwidth(), height = root.winfo_screenheight(), background="black", highlightthickness=0)
table_top.pack()

#local variables
#the current mode
#determines what happens with the left mouse button
mode = "move"
map = None

#start menu section
###############################################################################################

def set_draw_mode(): 
    global mode
    mode="draw"

def set_move_mode():
    global mode
    mode="move"

def load_large_map():
    global map
    map = Map("./sample_assets/sample_world_map.json", table_top)
    map.draw_map()

def load_small_map():
    global map
    map = Map("./sample_assets/sample_dungeon_map.json", table_top)
    map.draw_map()


# create a popup menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Draw", command=set_draw_mode)
menu.add_command(label="Move", command=set_move_mode)
menu.add_command(label="Sample Map: Large", command=load_large_map)
menu.add_command(label="Sample Map: Small", command=load_small_map)
menu.add_command(label="Exit", command=root.quit)

def popup(event):
    menu.post(event.x_root, event.y_root)

#end menu section
###############################################################################################




#map = Map("./sample_assets/sample_world_map.jpg", table_top)
#map.draw_map()


#table_top.create_image(table_top.winfo_screenwidth()/2, table_top.winfo_screenheight()/2,image=map.map)

#Start input section
###############################################################################################

#strarting position for dragging distance
draging_distance_start_x = 0
draging_distance_start_y = 0

#starting position for drawing
drawing_start_x = 0
drawing_start_y = 0



def left_mouse_button_press(event):
    if mode=="move":
        left_mouse_button_press_move(event)
    elif mode=="draw":
        left_mouse_button_press_draw(event)

def left_mouse_button_press_move(event):
        #get the global variables for where we are starting and set them to where the left button was pressed
        global draging_distance_start_x
        global draging_distance_start_y
        draging_distance_start_x = event.x
        draging_distance_start_y = event.y

def left_mouse_button_press_draw(event):
    #get the global variables for where we are starting and set them to where the left button was pressed
    global drawing_start_x
    global drawing_start_y
    drawing_start_x = event.x
    drawing_start_y = event.y



def left_mouse_button_drag(event):
    if mode=="move":
        left_mouse_button_drag_move(event)
    elif mode=="draw":
        left_mouse_button_drag_draw(event)

def left_mouse_button_drag_move(event):
    #calculate the distance between the starting point and the current point
    dist = math.sqrt((event.x - draging_distance_start_x)**2 + (event.y - draging_distance_start_y)**2)
    #add in calculation for feet per pixel
    dist = dist*map.map_feet_per_pixel

    #miles or feet
    #we'll change over at 1/4 mile and see how that works
    if dist < (5280/4):
        #whole feet
        dist = round(dist)
        distance_unit = "Feet"
    else:
        #miles with 1 decimal point
        dist = dist/5280
        distance_unit = "Miles"
        dist = round(dist,1)
 
    #delete the old distance text and line and draw new ones
    table_top.delete(table_top.find_withtag("dragging_distance_line"))
    table_top.delete(table_top.find_withtag("dragging_distance_text"))
    table_top.create_line(draging_distance_start_x, draging_distance_start_y, event.x, event.y, tag = "dragging_distance_line")
    table_top.create_text(event.x+15, event.y, text=f"{dist} {distance_unit}", tag="dragging_distance_text", anchor="w")


def left_mouse_button_drag_draw(event):
    #get global variables for where the mouse is moving from
    global drawing_start_x
    global drawing_start_y
    
    #draw a line from where the mouse was last time it moved until now
    table_top.create_line(drawing_start_x, drawing_start_y, event.x, event.y, tag="drawn_line")

    #set the starting position for next time with the ending position this time
    drawing_start_x = event.x
    drawing_start_y = event.y


def left_mouse_button_release(event):
    if mode=="move":
        left_mouse_button_release_move(event)
    elif mode=="draw":
        left_mouse_button_release_draw(event)

def left_mouse_button_release_move(event):
    #the user let go of the left mouse button, delete the distance line and text
    table_top.delete(table_top.find_withtag("dragging_distance_line"))
    table_top.delete(table_top.find_withtag("dragging_distance_text"))

def left_mouse_button_release_draw(event):
    #dont need to do anything right now when the user lets go of the mouse button while drawing
    pass



def right_mouse_button_press(event):
    #get the global variables for where we are starting and set them to where the left button was pressed
    global drawing_start_x
    global drawing_start_y
    drawing_start_x = event.x
    drawing_start_y = event.y

def right_mouse_button_drag(event):
    #get global variables for where the mouse is moving from
    global drawing_start_x
    global drawing_start_y
    
    #draw a line from where the mouse was last time it moved until now
    table_top.create_line(drawing_start_x, drawing_start_y, event.x, event.y, tag="drawn_line")

    #set the starting position for next time with the ending position this time
    drawing_start_x = event.x
    drawing_start_y = event.y

    #for dragging also call the normal movement handler
    #mouse_move(event)


def right_mouse_button_release(event):
    #user right clicked, open menu
    table_top.create_rectangle(event.x+20, event.y+20, event.x-20, event.y-20, tag="menu")

#destroy every object with a certain tag
def destroy_by_tag(tag):
    for line_segment in table_top.find_withtag(tag):
            table_top.delete(line_segment)




#set up all the key bindings
root.bind_all("<ButtonPress-1>", left_mouse_button_press)
root.bind_all("<B1-Motion>", left_mouse_button_drag)
root.bind_all("<ButtonRelease-1>", left_mouse_button_release)
root.bind_all("<ButtonRelease-3>", popup)

#end map section
###############################################################################################



table_top.mainloop()
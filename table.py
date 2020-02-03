import tkinter as tk
from tkinter import filedialog
import time
import math
from PIL import Image, ImageTk
from map import Map
from PIL import Image, ImageTk
import json
from measure_box import MeasureBox

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

#start variable section
###############################################################################################
#the current mode
#determines what happens with the left mouse button
mode = "move"

#the current map object
map = None

#values for drawing
draw_color="black"
draw_width=3

#strarting position for dragging distance
draging_distance_start_x = 0
draging_distance_start_y = 0

#starting position for drawing
drawing_start_x = 0
drawing_start_y = 0

#values for setting distance scale
distance_scale_feet = 0
scale_start_x = 0
scale_start_y = 0
scale_end_x = 0
scale_end_y = 0

#end variable section
###############################################################################################

#start menu section
###############################################################################################



def set_mode():
    global mode
    mode=mode_selection.get()

def set_draw_color():
    global draw_color
    draw_color=color_selection.get()

'''
def load_large_map():
    global map
    map = Map("./sample_assets/sample_world_map.jpg", table_top)
    map.draw_map()
'''

'''
def load_small_map():
    global map
    map = Map("./sample_assets/sample_dungeon_map.jpg", table_top)
    map.draw_map()
'''

def load_map():
    global map
    file = filedialog.askopenfile(parent=root,mode="rb",title="Choose a file",  filetypes =(("Image Files", ("*.bmp","*.jpg","*.png")),("All Files","*.*")))
    map = Map(file.name, table_top)
    map.draw_map()

def set_distance_scale():
    global distance_scale_feet
    global mode
    #pop up the distance scale box to get the distance in feet
    measure_box = MeasureBox(root)
    root.wait_window(measure_box.top)

    #set the local scale variable
    distance_scale_feet = measure_box.result

    #if the user didnt click cancel
    if not distance_scale_feet == None:
        #set the mode
        mode = "scale"
        #print instructions (if they picked miles this is gonna be messed up)
        table_top.create_text(table_top.winfo_width()/2, table_top.winfo_height()/2, text=f"Draw a line that is {distance_scale_feet} feet long", tag="scale_text", anchor="center")

def clear_drawing():
    destroy_by_tag("drawn_line")



# create a popup menu




menu = tk.Menu(root, tearoff=0)
map_tools_menu = tk.Menu(menu, tearoff=0)
draw_colors_menu = tk.Menu(menu, tearoff=0)


#menu.add_command(label="Move", command=set_move_mode)
#menu.add_command(label="Draw", command=set_draw_mode)



mode_selection = tk.StringVar()
color_selection = tk.StringVar()

menu.add_radiobutton(label="Move", variable=mode_selection, value="move", command=set_mode)
menu.add_radiobutton(label="Draw", variable=mode_selection, value="draw", command=set_mode)

menu.add_command(label="Clear Drawing", command=clear_drawing)

menu.add_cascade(label="Draw Colors", menu=draw_colors_menu)

menu.add_cascade(label="Map ...", menu=map_tools_menu)
menu.add_separator()
menu.add_command(label="Exit", command=root.quit)

map_tools_menu.add_command(label="Load Map", command=load_map)
#map_tools_menu.add_command(label="Sample Map: Small", command=load_small_map)
#map_tools_menu.add_command(label="Sample Map: Large", command=load_large_map)
map_tools_menu.add_command(label="Set Distance Scale", command=set_distance_scale)

draw_colors_menu.add_radiobutton(label="black", variable=color_selection, value="black", command=set_draw_color)
draw_colors_menu.add_radiobutton(label="red", variable=color_selection, value="red", command=set_draw_color)
draw_colors_menu.add_radiobutton(label="green", variable=color_selection, value="green", command=set_draw_color)
draw_colors_menu.add_radiobutton(label="blue", variable=color_selection, value="blue", command=set_draw_color)

def popup(event):
    menu.post(event.x_root, event.y_root)

#end menu section
###############################################################################################





#Start input section
###############################################################################################



def left_mouse_button_press(event):
    if mode=="move":
        left_mouse_button_press_move(event)
    elif mode=="draw":
        left_mouse_button_press_draw(event)
    elif mode=="scale":
        left_mouse_button_press_scale(event)

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

def left_mouse_button_press_scale(event):
    global scale_start_x
    global scale_start_y
    scale_start_x = event.x
    scale_start_y = event.y



def left_mouse_button_drag(event):
    if mode=="move":
        left_mouse_button_drag_move(event)
    elif mode=="draw":
        left_mouse_button_drag_draw(event)
    elif mode=="scale":
        left_mouse_button_drag_scale(event)

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
    table_top.create_line(drawing_start_x, drawing_start_y, event.x, event.y, width=draw_width, fill=draw_color, tag="drawn_line")

    #set the starting position for next time with the ending position this time
    drawing_start_x = event.x
    drawing_start_y = event.y

def left_mouse_button_drag_scale(event):
    global scale_end_x
    global scale_end_y
    scale_end_x = event.x
    scale_end_y = event.y
    destroy_by_tag("scale_line")
    table_top.create_line(scale_start_x, scale_start_y, scale_end_x, scale_end_y, width=1, fill="black", tag="scale_line")

def left_mouse_button_release(event):
    if mode=="move":
        left_mouse_button_release_move(event)
    elif mode=="draw":
        left_mouse_button_release_draw(event)
    elif mode=="scale":
        left_mouse_button_release_scale(event)

def left_mouse_button_release_move(event):
    #the user let go of the left mouse button, delete the distance line and text
    table_top.delete(table_top.find_withtag("dragging_distance_line"))
    table_top.delete(table_top.find_withtag("dragging_distance_text"))

def left_mouse_button_release_draw(event):
    #dont need to do anything right now when the user lets go of the mouse button while drawing
    pass

def left_mouse_button_release_scale(event):
    global mode
    #print("user finished dragging a scale")
    destroy_by_tag("scale_line")
    destroy_by_tag("scale_text")
    dist = math.sqrt((scale_end_x - scale_start_x)**2 + (scale_end_y - scale_start_y)**2)
    #print(f"user dragged {dist} px")
    #print(f"scale is {dist/distance_scale_feet} pixels per foot")
    map.set_distance(dist/distance_scale_feet)
    mode="move"
    


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

#load title screen
map = Map("./sample_assets/title_screen.png", table_top)
map.draw_map()


table_top.mainloop()
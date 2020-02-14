import tkinter as tk
from tkinter import filedialog
import time
import math
from PIL import Image, ImageTk
from map import Map
import json
from measure_box import MeasureBox
from area_effect_box import AreaEffectBox
from game_token import GameToken
from area_effect import AreaEffect

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

#debug?
debug = True

#a list of tokens
tokens = set()
moving_tokens = set()
right_clicked_token = None

#area effect variables
area_effects = set()
left_clicked_area_effect = None
right_clicked_area_effect = None
area_effect_moving = False
left_clicked_area_effect_offset_x = 0
left_clicked_area_effect_offset_y = 0

#values for right click position
right_click_x = 0
right_click_y = 0

#values for moving 
token_moving = False
left_clicked_token = None

#values for drawing
draw_color="black"
draw_width=3

#values for erasing
eraser_size=20

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





#token popup menu
def delete_token():
    #get access to the tokens set
    global tokens
    global right_clicked_token

    #undraw the token
    right_clicked_token.undraw()
    #delete the token
    tokens.remove(right_clicked_token)
    #forget about the token compeletely
    right_clicked_token = None


#make this better eventually
def set_token_color_red(): right_clicked_token.set_color("red")
def set_token_color_orange(): right_clicked_token.set_color("orange")
def set_token_color_yellow(): right_clicked_token.set_color("yellow")
def set_token_color_green(): right_clicked_token.set_color("green")
def set_token_color_blue(): right_clicked_token.set_color("blue")
def set_token_color_indigo(): right_clicked_token.set_color("indigo")
def set_token_color_violet(): right_clicked_token.set_color("violet")
def set_token_color_black(): right_clicked_token.set_color("black")
def set_token_color_white(): right_clicked_token.set_color("white")
def set_token_color_grey(): right_clicked_token.set_color("grey")

#radius so send half of size
def set_token_size_fine(): right_clicked_token.set_redius(0.25)
def set_token_size_diminutive(): right_clicked_token.set_redius(0.5)
def set_token_size_tiny(): right_clicked_token.set_redius(1.25)
def set_token_size_small(): right_clicked_token.set_redius(2)
def set_token_size_medium(): right_clicked_token.set_redius(2.5)
def set_token_size_large(): right_clicked_token.set_redius(5)
def set_token_size_huge(): right_clicked_token.set_redius(7.5)
def set_token_size_gargantuan(): right_clicked_token.set_redius(10)
def set_token_size_colossal(): right_clicked_token.set_redius(15)
def set_token_size_wtf(): right_clicked_token.set_redius(50)



token_menu = tk.Menu(root, tearoff=0)
token_size_menu = tk.Menu(token_menu, tearoff=0)
token_color_menu = tk.Menu(token_menu, tearoff=0)



token_menu.add_cascade(label = "Size ...", menu = token_size_menu)
token_menu.add_cascade(label = "Color ...", menu = token_color_menu)
token_menu.add_command(label = "Delete", command = delete_token)

token_color_menu.add_command(label = "Red", command = set_token_color_red, foreground="red")
token_color_menu.add_command(label = "Orange", command = set_token_color_orange, foreground="orange")
token_color_menu.add_command(label = "Yellow", command = set_token_color_yellow, foreground="yellow")
token_color_menu.add_command(label = "Green", command = set_token_color_green, foreground="green")
token_color_menu.add_command(label = "Blue", command = set_token_color_blue, foreground="blue")
token_color_menu.add_command(label = "Indigo", command = set_token_color_indigo, foreground="indigo")
token_color_menu.add_command(label = "Violet", command = set_token_color_violet, foreground="violet")
token_color_menu.add_command(label = "Black", command = set_token_color_black, foreground="black")
token_color_menu.add_command(label = "White", command = set_token_color_white, foreground="white")
token_color_menu.add_command(label = "Grey", command = set_token_color_grey, foreground="grey")

token_size_menu.add_command(label = "Fine (1/2 ft.)", command = set_token_size_fine)
token_size_menu.add_command(label = "Diminutive (1 ft.)", command = set_token_size_diminutive)
token_size_menu.add_command(label = "Tiny (2-1/2 ft.)", command = set_token_size_tiny)
token_size_menu.add_command(label = "Small (4 ft.)", command = set_token_size_small)
token_size_menu.add_command(label = "Medium (5 ft.)", command = set_token_size_medium)
token_size_menu.add_command(label = "Large (10 ft.)", command = set_token_size_large)
token_size_menu.add_command(label = "Huge (15 ft.)", command = set_token_size_huge)
token_size_menu.add_command(label = "Gargantuan (20 ft.)", command = set_token_size_gargantuan)
token_size_menu.add_command(label = "Colossal (30 ft.)", command = set_token_size_colossal)
token_size_menu.add_command(label = "WTF?", command = set_token_size_wtf)


# Got sizes from some dnd website
# Fine    1/2 ft.
# Diminutive  1 ft.
# Tiny    2-1/2 ft.
# Small   5 ft. (made this 4 ft. just so it looks different on the screen)
# Medium  5 ft.
# Large   10 ft.
# Huge    15 ft.
# Gargantuan  20 ft.
# Colossal    30 ft.


#main popup menu
def set_mode():
    global mode
    mode=mode_selection.get()

def set_draw_color():
    global draw_color
    draw_color=draw_color_selection.get()


def load_map():
    #get access to the map locally
    global map
    #file dialog to open a map image
    file = filedialog.askopenfile(parent=root,mode="rb",title="Choose a file",  filetypes =(("Image Files", ("*.bmp","*.jpg","*.png")),("All Files","*.*")))
    #create map instance
    map = Map(file.name, table_top)
    #draw the map
    map.draw_map()
    #get rid of all tokens
    for token in tokens:
        token.undraw()
    tokens.clear()

    for area_effect in area_effects:
        area_effect.undraw()
    area_effects.clear()

def add_token():
    #file dialog to load token image
    file = filedialog.askopenfile(parent=root,mode="rb",title="Choose a file",  filetypes =(("Image Files", ("*.bmp","*.jpg","*.png")),("All Files","*.*")))

    #create a token where the right click was
    tokens.add(GameToken(file.name, table_top, map,right_click_x,right_click_y,)) 

    #redraw tokens  so the new one shows up
    # (will this cause all the other tokens to be doubled until they move again? 
    # maybe add a redraw function to token class that removes it first)
    for token in tokens:
        token.draw()

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


def create_area_effect():
    #put up the area effect creation box
    area_effect_box = AreaEffectBox(root)
    root.wait_window(area_effect_box.top)

    #if the user didnt click cancel create the new area effect
    if area_effect_box._return==True:
        area_effects.add(AreaEffect(table_top, map, area_effect_box.shape,area_effect_box.height, area_effect_box.width,area_effect_box.color,right_click_x,right_click_y))

        #redraw all area effects
        for area_effect in area_effects:
            area_effect.draw()

        #redraw all tokens
        #so area effects dont cover them
        for token in tokens:
            token.draw()


def clear_drawing():
    destroy_by_tag("drawn_line")



menu = tk.Menu(root, tearoff=0)
map_tools_menu = tk.Menu(menu, tearoff=0)
token_tools_menu = tk.Menu(menu, tearoff=0)
draw_colors_menu = tk.Menu(menu, tearoff=0)


#menu.add_command(label="Move", command=set_move_mode)
#menu.add_command(label="Draw", command=set_draw_mode)



mode_selection = tk.StringVar()
draw_color_selection = tk.StringVar()

menu.add_radiobutton(label="Move", variable=mode_selection, value="move", command=set_mode)
menu.add_radiobutton(label="Draw", variable=mode_selection, value="draw", command=set_mode)
menu.add_radiobutton(label="Erase", variable=mode_selection, value="erase", command=set_mode)

menu.add_command(label="Clear Drawing", command=clear_drawing)

menu.add_cascade(label="Draw Colors", menu=draw_colors_menu)

menu.add_cascade(label="Map ...", menu=map_tools_menu)
menu.add_cascade(label="Token ...", menu=token_tools_menu)
menu.add_separator()

menu.add_command(label="Create Area Effect", command=create_area_effect)

menu.add_command(label="Exit", command=root.quit)

map_tools_menu.add_command(label="Load Map", command=load_map)
#map_tools_menu.add_command(label="Sample Map: Small", command=load_small_map)
#map_tools_menu.add_command(label="Sample Map: Large", command=load_large_map)
map_tools_menu.add_command(label="Set Distance Scale", command=set_distance_scale)



token_tools_menu.add_command(label="Add Token", command=add_token)

draw_colors_menu.add_radiobutton(label="black", variable=draw_color_selection, value="black", command=set_draw_color, foreground="black")
draw_colors_menu.add_radiobutton(label="red", variable=draw_color_selection, value="red", command=set_draw_color, foreground="red")
draw_colors_menu.add_radiobutton(label="green", variable=draw_color_selection, value="green", command=set_draw_color, foreground="green")
draw_colors_menu.add_radiobutton(label="blue", variable=draw_color_selection, value="blue", command=set_draw_color, foreground="blue")

#right click mouse event (maybe could use a better name?)
def popup(event):

    #if there is an eraser box, delete it
    #TODO create a dedicated right click handler that then calls popup so this doesnt have to be here
    destroy_by_tag("eraser_bounds")

    #store the right click position (maybe theres a better way to do this?)
    global right_click_x
    global right_click_y
    right_click_x = event.x
    right_click_y = event.y

    token_clicked = False

    for token in tokens:
        if token.contains(event.x, event.y):
            global right_clicked_token
            right_clicked_token = token
            token_clicked = True
            break

    area_effect_clicked = False

    if token_clicked == False:
        for area_effect in area_effects:
            if area_effect.contains(event.x, event.y):
                global right_clicked_area_effect
                right_clicked_area_effect = area_effect
                area_effect_clicked = True
                break



    if token_clicked == True:
        token_menu.post(event.x_root, event.y_root)
    elif area_effect_clicked == True:
        #area_effect_menu.post(event.x_root, event.y_root)
        global mode
        mode = "rotating_area_effect"
    else:
        menu.post(event.x_root, event.y_root)

#end menu section
###############################################################################################


def print_debug():
    tracked_items = table_top.find_all()

    all_tags = set()

    for item in tracked_items:
        tags = table_top.gettags(item)
        for tag in tags:
            all_tags.add(tag)

    print_offset = 1
    print_spacing = 10
    
    destroy_by_tag("debug_text")

    table_top.create_rectangle(0,0,400,500,fill="white", tag="debug_text")

    table_top.create_text(200, print_offset*print_spacing, text = f"mode: {mode}", anchor="e", tag="debug_text")
    print_offset += 1
    table_top.create_text(200, print_offset*print_spacing, text = f"moving token: {token_moving}", anchor="e", tag="debug_text")
    print_offset += 1
    table_top.create_text(200, print_offset*print_spacing, text = f"moving area effect: {area_effect_moving}", anchor="e", tag="debug_text")
    print_offset += 1

    for tag in all_tags:
        
        table_top.create_text(200, print_offset*print_spacing, text = f"{tag}: {len(table_top.find_withtag(tag))}", anchor="e", tag="debug_text")
        print_offset+=1
        #print (f"{tag}: {len(table_top.find_withtag(tag))}")

    

#Start input section
###############################################################################################

def mouse_moved(event):
    #if we are in erase mode draw the eraser bounds
    if mode=="erase":
        destroy_by_tag("eraser_bounds")
        table_top.create_rectangle(event.x-(eraser_size/2), event.y-(eraser_size/2), event.x+(eraser_size/2),event.y+(eraser_size/2), tag="eraser_bounds")

    if mode=="rotating_area_effect":
        right_clicked_area_effect.rotate_by_mouse(event.x,event.y)

    if debug == True:
        print_debug()

        
    


def left_mouse_button_press(event):
    if mode=="move":
        left_mouse_button_press_move(event)
    elif mode=="draw":
        left_mouse_button_press_draw(event)
    elif mode=="scale":
        left_mouse_button_press_scale(event)
    elif mode=="rotating_area_effect":
        left_mouse_button_press_rotating_area_effect(event)

def left_mouse_button_press_move(event):
        #get the global variables for where we are starting and set them to where the left button was pressed
        global draging_distance_start_x
        global draging_distance_start_y
        draging_distance_start_x = event.x
        draging_distance_start_y = event.y

        #only get 1 token and store it instead of having a bunch to move
        for token in tokens:
            if token.contains(event.x, event.y):
                global token_moving
                global left_clicked_token
                token_moving = True
                left_clicked_token = token
                break

        #only try to move an area effect if you arent moving a token
        #tokens take precedence
        if token_moving == False:
            for area_effect in area_effects:
                if area_effect.contains(event.x, event.y):
                    global area_effect_moving
                    global left_clicked_area_effect
                    global left_clicked_area_effect_offset_x
                    global left_clicked_area_effect_offset_y
                    left_clicked_area_effect_offset_x = event.x - area_effect.x
                    left_clicked_area_effect_offset_y = event.y - area_effect.y
                    area_effect_moving = True
                    left_clicked_area_effect = area_effect
                    break

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

def left_mouse_button_press_rotating_area_effect(event):
    global mode
    global right_clicked_area_effect
    mode = "move"
    right_clicked_area_effect = None

def left_mouse_button_drag(event):
    if mode=="move":
        left_mouse_button_drag_move(event)
    elif mode=="draw":
        left_mouse_button_drag_draw(event)
    elif mode=="scale":
        left_mouse_button_drag_scale(event)
    elif mode=="erase":
        left_mouse_button_drag_erase(event)

def left_mouse_button_drag_move(event):

    if debug == True:
        print_debug()

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
 


    
    destroy_by_tag("dragging_distance_message")

    #bottom, right side up
    table_top.create_rectangle(
        (table_top.winfo_width()/2)-100, 
        table_top.winfo_height()-40, 
        (table_top.winfo_width()/2)+100, 
        table_top.winfo_height()-10, 
        fill="white",
        stipple="gray50",
        tag="dragging_distance_message"
        )

    table_top.create_text(
        table_top.winfo_width()/2, 
        table_top.winfo_height()-25, 
        text=f"{dist} {distance_unit}", 
        font=("TkDefaultFont", 24), 
        tag="dragging_distance_message"
        )

    #top, upside down
    table_top.create_rectangle(
        (table_top.winfo_width()/2)-100, 
        40, 
        (table_top.winfo_width()/2)+100, 
        10, 
        fill="white",
        stipple="gray50",
        tag="dragging_distance_message"
        )

    table_top.create_text(
        table_top.winfo_width()/2, 
        25, 
        text=f"{dist} {distance_unit}", 
        font=("TkDefaultFont", 24), 
        tag="dragging_distance_message",
        angle=180
        )

    #right side
    table_top.create_rectangle(
        table_top.winfo_width()-40, 
        (table_top.winfo_height()/2)-100, 
        table_top.winfo_width()-10, 
        (table_top.winfo_height()/2)+100, 
        fill="white",
        stipple="gray50",
        tag="dragging_distance_message"
        )

    table_top.create_text(
        table_top.winfo_width()-25, 
        table_top.winfo_height()/2, 
        text=f"{dist} {distance_unit}", 
        font=("TkDefaultFont", 24), 
        tag="dragging_distance_message",
        angle=90
        )

    #left side
    table_top.create_rectangle(
        40, 
        (table_top.winfo_height()/2)-100, 
        10, 
        (table_top.winfo_height()/2)+100, 
        fill="white",
        stipple="gray50",
        tag="dragging_distance_message"
        )

    table_top.create_text(
        25, 
        table_top.winfo_height()/2, 
        text=f"{dist} {distance_unit}", 
        font=("TkDefaultFont", 24), 
        tag="dragging_distance_message",
        angle=270
        )


    if token_moving == True:
        destroy_by_tag("moving_outline")

        x1 = event.x-left_clicked_token.radius_pixels
        y1 = event.y-left_clicked_token.radius_pixels
        x2 = event.x+left_clicked_token.radius_pixels
        y2 = event.y+left_clicked_token.radius_pixels

        table_top.create_line(left_clicked_token.x, left_clicked_token.y, event.x, event.y, width=3, dash=(30,10), tag="moving_outline")
        table_top.create_oval(x1, y1, x2, y2, width=3, outline=left_clicked_token.outline_color, tag="moving_outline")

    elif area_effect_moving == True:

        left_clicked_area_effect.move(event.x-left_clicked_area_effect_offset_x, event.y-left_clicked_area_effect_offset_y)

        #redraw all tokens so they stay on top of the area effect
        for token in tokens:
            token.undraw()
            token.draw()

    else:
        #only draw this line if we are "measuring" and not moving
        #delete the old distance text and line and draw new ones
        destroy_by_tag("dragging_distance_line")
        table_top.create_line(draging_distance_start_x, draging_distance_start_y, event.x, event.y, width=3, dash=(30,10), tag = "dragging_distance_line")
        #table_top.create_text(event.x+15, event.y, text=f"{dist} {distance_unit}", tag="dragging_distance_message", anchor="w")
        #table_top.create_text(table_top.winfo_width()/2, table_top.winfo_height()/2, text=f"{dist} {distance_unit}", tag="dragging_distance_message")

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

def left_mouse_button_drag_erase(event):
    destroy_by_tag("eraser_bounds")
    table_top.create_rectangle(event.x-(eraser_size/2), event.y-(eraser_size/2), event.x+(eraser_size/2),event.y+(eraser_size/2), tag="eraser_bounds")
    
    for drawn_line_segment in table_top.find_withtag("drawn_line"):
        if (table_top.coords(drawn_line_segment)[0]>event.x-(eraser_size/2) and 
            table_top.coords(drawn_line_segment)[0]<event.x+(eraser_size/2) and 
            table_top.coords(drawn_line_segment)[1]>event.y-(eraser_size/2) and 
            table_top.coords(drawn_line_segment)[1]<event.y+(eraser_size/2)):
            table_top.delete(drawn_line_segment)

def left_mouse_button_release(event):

    if debug==True:
        print_debug()

    if mode=="move":
        left_mouse_button_release_move(event)
    elif mode=="draw":
        left_mouse_button_release_draw(event)
    elif mode=="scale":
        left_mouse_button_release_scale(event)

def left_mouse_button_release_move(event):
    global token_moving
    global area_effect_moving
    #the user let go of the left mouse button, delete the distance line and text

    if token_moving == True:
        global left_clicked_token
        
        destroy_by_tag("moving_outline")
        destroy_by_tag("dragging_distance_message")
        left_clicked_token.move(event.x, event.y)

        
        
        token_moving = False
        left_clicked_token = None

        moving_tokens.clear()
    elif area_effect_moving == True:

        global left_clicked_area_effect
        
        destroy_by_tag("dragging_distance_message")

        area_effect_moving=False
        left_clicked_area_effect = None

        

    else:
        destroy_by_tag("dragging_distance_line")
        destroy_by_tag("dragging_distance_message")


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
    


#destroy every object with a certain tag
def destroy_by_tag(tag):
    for line_segment in table_top.find_withtag(tag):
            table_top.delete(line_segment)




#set up all the key bindings
root.bind_all("<Motion>", mouse_moved)
root.bind_all("<ButtonPress-1>", left_mouse_button_press)
root.bind_all("<B1-Motion>", left_mouse_button_drag)
root.bind_all("<ButtonRelease-1>", left_mouse_button_release)
root.bind_all("<ButtonRelease-3>", popup)

#end map section
###############################################################################################

#load title screen
map = Map("./sample_assets/sample_dungeon_map.jpg", table_top)
map.draw_map()



#draw_token()

table_top.mainloop()
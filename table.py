import tkinter as tk
import time
import math


#full screen root window
root = tk.Tk()
root.attributes("-fullscreen", True)

#the table top canvas
#make it the same size as the full screen window
table_top = tk.Canvas(root, width = root.winfo_screenwidth(), height = root.winfo_screenheight())
table_top.pack()

#strarting position for dragging distance
draging_distance_start_x = 0
draging_distance_start_y = 0

#starting position for drawing
drawing_start_x = 0
drawing_start_y = 0

#print some instructions
font=("TkDefaultFont", 14)
table_top.create_text(root.winfo_screenwidth()/2, (root.winfo_screenheight()/2)-30, text=f"table", font=("TkDefaultFont", 24))
table_top.create_text(root.winfo_screenwidth()/2, (root.winfo_screenheight()/2)+15, text=f"left click to measure distance")
table_top.create_text(root.winfo_screenwidth()/2, (root.winfo_screenheight()/2)+30, text=f"right click to draw")
table_top.create_text(root.winfo_screenwidth()/2, (root.winfo_screenheight()/2)+45, text=f"double right click to clear drawing")
table_top.create_text(root.winfo_screenwidth()/2, (root.winfo_screenheight()/2)+60, text=f"press escape to quit")


#keybindings and event handlers (hopefully can move these to a different file?)
def exit(event):
    root.quit()


def mouse_move(event):
    #delete the old position text and print the new positions
    table_top.delete(table_top.find_withtag("mouse_position"))
    table_top.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2, text=f"{event}", tag="mouse_position")


def left_mouse_button_press(event):
    #get the global variables for where we are starting and set them to where the left button was pressed
    global draging_distance_start_x
    global draging_distance_start_y
    draging_distance_start_x = event.x
    draging_distance_start_y = event.y

def left_mouse_button_drag(event):

    #calculate the distance between the starting point and the current point
    dist = round(math.sqrt((event.x - draging_distance_start_x)**2 + (event.y - draging_distance_start_y)**2))


    #delete the old distance text and line and draw new ones
    table_top.delete(table_top.find_withtag("dragging_distance_line"))
    table_top.delete(table_top.find_withtag("dragging_distance_text"))
    table_top.create_line(draging_distance_start_x, draging_distance_start_y, event.x, event.y, tag = "dragging_distance_line")
    table_top.create_text(event.x+15, event.y, text=f"{dist}px", tag="dragging_distance_text", anchor="w")

    #for dragging also call the normal movement handler
    mouse_move(event)

def left_mouse_button_release(event):
    #the user let go of the left mouse button, delete the distance line and text
    table_top.delete(table_top.find_withtag("dragging_distance_line"))
    table_top.delete(table_top.find_withtag("dragging_distance_text"))


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
    mouse_move(event)

def right_mouse_button_double_click(event):
    #delete all the little line segments 
    for line_segment in table_top.find_withtag("drawn_line"):
        table_top.delete(line_segment)

    

#set up all the key bindings
root.bind_all("<Escape>", exit)
root.bind_all("<Motion>", mouse_move)
root.bind_all("<ButtonPress-1>", left_mouse_button_press)
root.bind_all("<B1-Motion>", left_mouse_button_drag)
root.bind_all("<ButtonRelease-1>", left_mouse_button_release)
root.bind_all("<ButtonPress-3>", right_mouse_button_press)
root.bind_all("<B3-Motion>", right_mouse_button_drag)
root.bind_all("<Double-Button-3>", right_mouse_button_double_click)


table_top.mainloop()
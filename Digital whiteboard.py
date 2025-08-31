from tkinter import *
from tkinter import simpledialog
import math

# Initialize
root = Tk()
root.title("Digital Whiteboard")

# Current drawing color and size deafault
current_color = "black"
brush_size = 3
current_tool = "brush"  # Can be "brush", "eraser", or a shape name

last_x = None
last_y = None

# --- Drawing Functions ---
def set_color(new_color):
    global current_color, current_tool
    current_color = new_color
    current_tool = "brush"

def set_brush_size():
    global brush_size
    try:
        new_size = int(brush_size_entry.get())
        if new_size > 0:
            brush_size = new_size
    except:
        pass

def set_eraser():
    global current_tool
    global brush_size
    current_tool = "eraser"
    try:
        new_size = int(eraser_size_entry.get())
        if new_size > 0:
            brush_size = new_size
    except:
        pass

def draw(event):
    global last_x
    global last_y
    if current_tool in ["brush", "eraser"]:
        color = "white" if current_tool == "eraser" else current_color
        canvas.create_line(last_x, last_y, event.x, event.y, fill=color, width=brush_size,capstyle=ROUND, smooth=True)
    last_x, last_y = event.x, event.y

    
def start_draw(event):
    global last_x
    global last_y
    last_x = event.x
    last_y = event.y
    if current_tool in ["rectangle", "oval", "line", "triangle"]:
        create_shape(event)


def stop_draw(event):
    global last_x
    global last_y
    last_x = None
    last_y = None

def clear_canvas():
    canvas.delete("all")

# --- Shape Creation Functions ---
def prepare_shape(shape_type):
    global current_tool
    current_tool = shape_type
    canvas.config(cursor="cross")

def create_shape(event):
    global current_tool  # Moved to top of function to fix the error
    if current_tool == "rectangle":
        width = simpledialog.askinteger("Rectangle", "Width:", parent=root, minvalue=1)
        height = simpledialog.askinteger("Rectangle", "Height:", parent=root, minvalue=1)
        if width and height:
            canvas.create_rectangle(event.x, event.y, event.x + width, event.y + height, outline=current_color)
    elif current_tool == "oval":
        width = simpledialog.askinteger("Oval", "Width:", parent=root, minvalue=1)
        height = simpledialog.askinteger("Oval", "Height:", parent=root, minvalue=1)
        if width and height:
            canvas.create_oval(event.x, event.y, event.x + width, event.y + height, outline=current_color)
    elif current_tool == "line":
        length = simpledialog.askinteger("Line", "Length:", parent=root, minvalue=1)
        if length:
            canvas.create_line(event.x, event.y, event.x + length, event.y, width=brush_size)
    elif current_tool == "triangle":
        side = simpledialog.askinteger("Triangle", "Side Length:", parent=root, minvalue=1)
        if side:
            height = (math.sqrt(3)/2) * side
            points = [event.x, event.y,
                      event.x + side, event.y,
                      event.x + side/2, event.y + height]
            canvas.create_polygon(points, fill=current_color, outline=current_color)
    
    # Reset to brush tool after shape creation
    current_tool = "brush"
    canvas.config(cursor="")

# --- GUI Layout ---
# Main container frames
left_frame = Frame(root, bg="lightgray")
left_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
right_frame = Frame(root, bg="lightgray")
right_frame.pack(side=RIGHT, fill=Y, padx=5, pady=5)

# Color buttons
color_label = Label(left_frame, text="Colors", bg="lightgray")
color_label.pack(pady=(5, 0))
Button(left_frame, text="Red", bg="red", fg="black", width=8, command=lambda: set_color("red")).pack(pady=2)
Button(left_frame, text="Green", bg="green", fg="black", width=8, command=lambda: set_color("green")).pack(pady=2)
Button(left_frame, text="Blue", bg="blue", fg="white", width=8, command=lambda: set_color("blue")).pack(pady=2)
Button(left_frame, text="Yellow", bg="yellow", fg="black", width=8, command=lambda: set_color("yellow")).pack(pady=2)
Button(left_frame, text="Black", bg="black", fg="white", width=8, command=lambda: set_color("black")).pack(pady=2)
Button(left_frame, text="Orange", bg="orange", fg="black", width=8, command=lambda: set_color("orange")).pack(pady=2)
Button(left_frame, text="Purple", bg="purple", fg="white", width=8, command=lambda: set_color("purple")).pack(pady=2)
Button(left_frame, text="Brown", bg="brown", fg="white", width=8, command=lambda: set_color("brown")).pack(pady=2)
Button(left_frame, text="Pink", bg="pink", fg="black", width=8, command=lambda: set_color("pink")).pack(pady=2)

# Brush controls
brush_label = Label(left_frame, text="Brush", bg="lightgray")
brush_label.pack(pady=(10, 0))
Label(left_frame, text="Size", bg="lightgray").pack()
brush_size_entry = Entry(left_frame, width=6)
brush_size_entry.insert(0, "3")
brush_size_entry.pack()
Button(left_frame, text="Set", width=6, command=set_brush_size).pack(pady=(2, 5))

# Eraser controls
eraser_label = Label(left_frame, text="Eraser", bg="lightgray")
eraser_label.pack(pady=(5, 0))
Button(left_frame, text="Eraser", width=8, command=set_eraser).pack(pady=2)
Label(left_frame, text="Size", bg="lightgray").pack()
eraser_size_entry = Entry(left_frame, width=6)
eraser_size_entry.insert(0, "10")
eraser_size_entry.pack()
Button(left_frame, text="Set", width=6, command=set_eraser).pack(pady=(2, 5))

# Clear button
Button(left_frame, text="Clear All", width=8, command=clear_canvas).pack(pady=10)

# Shape tools
shape_label = Label(right_frame, text="Shapes", bg="lightgray")
shape_label.pack(pady=(5, 0))
Button(right_frame, text="Rectangle", width=8, command=lambda: prepare_shape("rectangle")).pack(pady=2)
Button(right_frame, text="Oval", width=8, command=lambda: prepare_shape("oval")).pack(pady=2)
Button(right_frame, text="Line", width=8, command=lambda: prepare_shape("line")).pack(pady=2)
Button(right_frame, text="Triangle", width=8, command=lambda: prepare_shape("triangle")).pack(pady=2)

# Main Canvas
canvas = Canvas(root, bg="white")
canvas.pack(fill=BOTH, expand=True)

# Bind mouse events
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# Start the app
root.mainloop()

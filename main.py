import tkinter as tk
from tkinter.colorchooser import askcolor
from generator import generate_tile

# Initialisation
root = tk.Tk()

leftFrame = tk.Frame(root)
leftFrame.pack(side="left")

rightFrame = tk.Frame(root)
rightFrame.pack(side="right")

colorFrame= tk.Frame(rightFrame, bg="black")
colorFrame.pack(padx=10, pady=10)

# functions
def change_color(color):
    selectedColor = askcolor(title="Terraria Tile Color chooser")
    color.config(bg=selectedColor[1])

# Config
root.title("Terraria Tile Generator")
root.geometry("400x200")
root.resizable(False, False)

# components
# Visual aid for the color selected
color = tk.Label(colorFrame, width=10, height=4)
color.pack(padx=10, pady=10)

# Color selection for the tile
colorButton = tk.Button(rightFrame, text="Color", command= lambda: change_color(color), width=10)
colorButton.pack(padx=5, pady=5)

# Will initiate a generation subprocess which will then satisfy the process
generate = tk.Button(rightFrame, text="Generate", width=10, command= lambda: generate_tile(color['bg'], shades.get(), consistency.get(), name.get()))
generate.pack(padx=5, pady=5)

# Option 1: number of shades when making tile (max 5)
shadesLabel = tk.Label(leftFrame, text="number of shades when making tile (max 5)")
shadesLabel.pack(padx=20)

shades = tk.Scale(leftFrame, from_=3, to=10, orient="horizontal")
shades.pack()

# Option 2: Consistency (0 Smooth - 1 Jagged)
consistencyLabel = tk.Label(leftFrame, text="Consistency (0 Smooth - 1 Jagged)")
consistencyLabel.pack()

consistency = tk.Scale(leftFrame, from_=0, to=1, orient="horizontal", digits=3, resolution=0.01)
consistency.pack()

# Option 3: Name of ore
name = tk.Entry(leftFrame)
name.insert(0, "ore_name")
name.pack(pady=10)

root.mainloop()
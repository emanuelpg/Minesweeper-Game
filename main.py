from tkinter import *
import settings
import utils
import random
from Cell import Cell


root = Tk()
root.bind("<Key>", Cell.key_pressed)
# Override the settings of the window
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    root,
    bg="black",
    width=utils.width_prct(25),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=utils.height_prct(25))

center_frame = Frame(
    root,
    bg='black',
    width=utils.width_prct(75),
    height=utils.height_prct(75)
)

center_frame.place(
    x=utils.width_prct(25),
    y=utils.height_prct(25)
)

# Writing Game Title
game_title = Label(
    top_frame,
    bg="black",
    fg="white",
    text="MINESWEEPER GAME",
    width=24,
    height=4,
    font=("Arial", 60)
)

game_title.place(
    x=190,
    y=-90,
)

# Writing Game Instructions
game_instructions = Label(
    left_frame,
    bg="black",
    fg="white",
    text="HOW TO PLAY\nLeft mouse button reveals cell\nRight mouse button marks cell\nPress 'R' to restart the game\nPress 'O' to give up the game",
    width=40,
    height=8,
    font=("Arial", 15)
)

game_instructions.place(
    x=-40,
    y=200
)

# Initiating Game Settings
Cell.set_game_location(center_frame)

Cell.set_label_location(left_frame)

Cell.start_new_game(center_frame)

# Run the window
root.mainloop()

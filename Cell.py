from tkinter import Button, Label, messagebox
import random
import settings


class Cell:
    all = []
    cell_count_label_object = None
    cell_count = settings.CELL_COUNT
    cell_count_label_location = None
    game_location = None
    gave_up = False

    """ ------------------ SETTING METHODS ------------------ """
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.shown = False

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def __repr__(self):
        return f"Cell({self.y}, {self.x})"

    def create_btn_object(self, location):
        btn = Button(
            location,
            bg='#DEDEDE',
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Left Click
        btn.bind('<Button-3>', self.right_click_actions)  # Right Click
        self.cell_btn_object = btn

    """ ----------------------------------------------------- """

    """ ------------------- STATIC METHODS ------------------ """

    @staticmethod
    def set_game_location(location):
        Cell.game_location = location

    @staticmethod
    def set_label_location(location):
        Cell.cell_count_label_location = location

    @staticmethod
    def set_initial_settings(location):
        Cell.all = []
        Cell.cell_count_label_object = None
        Cell.cell_count = settings.CELL_COUNT
        Cell.gave_up = False
        Cell.game_location = location

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left: {Cell.cell_count}",
            width=12,
            height=4,
            font=("Arial", 30)
        )
        Cell.cell_count_label_object = lbl

    @staticmethod
    def update_cell_count_label():
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(text=f"Cells Left: {Cell.cell_count}")

    @staticmethod
    def get_cell_by_axis(x, y):
        # Return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        return None

    @staticmethod
    def key_pressed(event):
        if event.char == 'r':
            Cell.restart_game()
        if event.char == 'o':
            Cell.give_up_game()

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    @staticmethod
    def start_new_game(location):
        Cell.set_initial_settings(location)

        for x in range(settings.GRID_SIZE):
            for y in range(settings.GRID_SIZE):
                c = Cell(x, y)
                c.create_btn_object(Cell.game_location)
                c.cell_btn_object.grid(
                    column=x, row=y
                )

        # Call the label from the Cell class
        Cell.create_cell_count_label(Cell.cell_count_label_location)
        Cell.cell_count_label_object.place(
            x=40, y=0
        )

        Cell.randomize_mines()

    @staticmethod
    def restart_game():
        Cell.start_new_game(Cell.game_location)

    @staticmethod
    def lose_game():
        messagebox.showinfo(
            title="GAME OVER!!!",
            message="You clicked on a mine!"
        )
        Cell.start_new_game(Cell.game_location)

    @staticmethod
    def win_game():
        messagebox.showinfo(
            title="CONGRATULATIONS!!!",
            message="You won the game!"
        )
        Cell.start_new_game(Cell.game_location)
    
    @staticmethod
    def give_up_game():
        Cell.gave_up = True
        for cell in Cell.all:
            if not cell.is_mine:
                cell.show_cell()
            else:
                cell.show_mine()
        messagebox.showinfo(
            title="GAME OVER!!!",
            message="You gave up the game!"
        )
        Cell.start_new_game(Cell.game_location)

    """ ----------------------------------------------------- """

    """ -------------  USER INTERACTION METHODS ------------- """
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
            if self.surrounded_mines_quantity == 0:
                for cell in self.surrounded_cells():
                    cell.show_cell()

    def right_click_actions(self, event):
        if self.cell_btn_object.cget("bg") == "#DEDEDE":
            self.cell_btn_object.configure(bg="orange")
        else:
            self.cell_btn_object.configure(bg="#DEDEDE")

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        Cell.cell_count -= 1
        # Replace the text of cell count label with newer count
        Cell.update_cell_count_label()
        if not Cell.gave_up:
            Cell.lose_game()

    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_mines_quantity(self):
        mine_quantity = 0
        for cell in self.surrounded_cells():
            if cell.is_mine:
                mine_quantity += 1
        return mine_quantity

    def show_cell(self):
        if self.shown:
            return
        else:
            self.cell_btn_object.configure(text=f"{self.surrounded_mines_quantity}")
            self.shown = True
        Cell.cell_count -= 1
        # Replace the text of cell count label with newer count
        Cell.update_cell_count_label()
        if Cell.cell_count == settings.MINES_COUNT and not Cell.gave_up:
            Cell.win_game()

    """ ----------------------------------------------------- """

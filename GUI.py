from PIL import ImageTk, Image
import numpy as np
import tkinter as tk
import queue
import os
from typing import Sequence, Optional

DEFAULT_IMG = "./images/empty_cell.jpg"
X_IMG = "./images/x.png"
O_IMG = "./images/o.png"


class MainScreen(tk.Tk):
    def __init__(self, shared_content, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_attributes('-fullscreen', True)
        self.exit_button = tk.Button(self, text='r', font=('webdings', 8), width=self.winfo_screenwidth(), relief='flat',
                                     background="grey28", activebackground="red", command=lambda: self.on_exit(shared_content))

        self.exit_button.pack(side="top", fill="both")

        self.mainframe = MainFrame(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg="white")
        self.mainframe.pack(side="bottom", fill="both", expand=True)
        self.mainframe.Init()
        self.main_thread = None

    def update_board(self, move, player):
        self.mainframe[move[0]][move[1]].set_image(X_IMG if player else O_IMG)
        self.update()

    def reset(self):
        self.mainframe.reset()

    def the_winner_is(self, player, winning_pattern):
        self.mainframe.mark_cells(winning_pattern, "red")
        pass
        # TODO - put some indicative announcement

    def on_exit(self, shared_content):
        # wait for thread to finish
        shared_content.games_are_played = False
        self.quit()


class MainFrame(tk.Frame):

    def __init__(self, controller, **kw):
        tk.Frame.__init__(self, **kw)
        self.controller = controller
        self.cells = [
            [],
            [],
            []
        ]

    def Init(self):
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            for j in range(3):
                self.cells[i].append(Cell(self))
                self.cells[i][j].grid(row=i, column=j)
                self.cells[i][j].Init()
                self.cells[i][j].set_image(DEFAULT_IMG)

    def __getitem__(self, x):
        assert 0 <= x <= 2
        return self.cells[x]

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.cells[i][j].set_image(DEFAULT_IMG)
        self.mark_cells()

    def mark_cells(self, cells: Optional[Sequence[Sequence[int]]] = None, color="white"):
        if cells is None:
            for row in range(len(self.cells)):
                for col in range(len(self.cells[row])):
                    self.cells[row][col].mark_cell(color=color)
        else:
            for row in cells:
                self.cells[row[0]][row[1]].mark_cell(color=color)


class Cell(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.cell = tk.Label(self,  width=500, height=255)

    def Init(self):
        self.cell.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_image(DEFAULT_IMG)

    def set_image(self, img_addr):
        img = ImageTk.PhotoImage(Image.open(img_addr))
        self.cell.configure(image=img)
        self.cell.image = img

    def mark_cell(self, color="white"):
        self.configure(bg=color)

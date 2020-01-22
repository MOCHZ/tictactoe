#!/usr/bin/env python3
# Author:   ParticleVoid
# Email:    particle.void@0x00.guru
# Date:     2020
import tkinter as tk
import tkinter.messagebox as msg


class Game:
    window = tk.Tk()
    window.title("Tic Tac Toe")
    menu_bar = ""

    geometry = {
        "width": 210,
        "height": 220
    }

    tiles = {}
    default_image = ""

    frm_grid = tk.Frame(window)
    button_grid = []
    score_map = [
        list(range(3)),
        list(range(3)),
        list(range(3))
    ]
    button = {
        "id": 0,
        "width": 64,
        "height": 64
    }

    player = {
        "current": 1,
        "symbol": [None, "X", "O"]
    }

    def __init__(self, **kwargs):
        if "geometry" in kwargs:
            try:
                self.window.geometry(kwargs.get("geometry"))
            except ValueError as ve:
                print(ve)
        else:
            self.window.geometry("{}x{}".format(self.geometry.get("width"), self.geometry.get("height")))
        if "resize" in kwargs:
            if kwargs.get("resize"):
                self.window.resizable(True, True)
            else:
                self.window.resizable(False, False)
        else:
            self.window.resizable(False, False)

        self.tiles = {
            "player1": tk.PhotoImage("img/player1.gif"),
            "player2": tk.PhotoImage("img/player2.gif"),
            "default": tk.PhotoImage("img/default.gif")
        }
        self.default_image = tk.PhotoImage(file=self.tiles.get("default"))
        self.draw_grid()

    def draw_grid(self):
        for row in range(3):
            for col in range(3):
                self.append_to_grid(row, col)
                self.button["id"] += 1

        self.frm_grid.pack(side=tk.LEFT, anchor=tk.SW)

    def append_to_grid(self, row, col):
        self.button_grid.append(tk.Button(self.frm_grid, image=self.default_image, text=" ",
                                          width=self.button.get("width"), height=self.button.get("height"),
                                          command=lambda button=self.button.get("id"): self.change_tile(button,
                                                                                                        row, col)))

        self.button_grid[self.button.get("id")].image = self.default_image
        self.button_grid[self.button.get("id")].grid(row=row, column=col)

    def change_tile(self, button, row, col):
        if self.player.get("current") == 1:
            new_image = tk.PhotoImage(file=self.tiles.get("player1"))
        else:
            new_image = tk.PhotoImage(file=self.tiles.get("player2"))

        self.button_grid[button].text = self.player.get("symbol")[self.player.get("current")]
        self.score_map[row][col] = self.player.get("symbol")[self.player.get("current")]

        self.button_grid[button].configure(image=new_image, state=tk.DISABLED)
        self.button_grid[button].image = new_image

        self.has_won()

    def has_won(self):
        player_won = False
        conditions = {"player1": ["X", "X", "X"], "player2": ["O", "O", "O"]}
        combinations = []

        for col in range(3):
            current_column = []
            for row in range(3):
                if col == 0:
                    combinations.append(self.score_map[row])
                current_column.append(self.score_map[row][col])
            combinations.append(current_column)

        combinations.append([self.score_map[0][0], self.score_map[1][1], self.score_map[2][2]])
        combinations.append([self.score_map[0][2], self.score_map[1][1], self.score_map[2][0]])

        for row in combinations:
            if row == conditions.get("player1") or row == conditions.get("player2"):
                player_won = True

        if player_won:
            answer = msg.askokcancel("Congratulations!",
                                     "Player {} won the match!\n"
                                     "Do you want to play again?".format(self.player.get("current")))
            if answer:
                del combinations
                self.reset()
            else:
                self.window.quit()
        else:
            if self.player.get("current") == 1:
                self.player["current"] = 2
            else:
                self.player["current"] = 1

    def reset(self):
        self.player["current"] = 1

        for btn in self.button_grid:
            btn.configure(text=" ", image=self.default_image, state=tk.ACTIVE)
            btn.image = self.default_image
            btn.text = " "

        self.score_map = [
            list(range(3)),
            list(range(3)),
            list(range(3)),
        ]

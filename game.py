import tkinter as tk
from tkinter import messagebox
from cell import Cell
import random


class MineSweeper:

    def __init__(self,parent:tk.Widget,grid_size:int,bomb_count:int):
        ''' This class creates a MineSweeper game instance'''
        self._parent = parent
        self._grid = {}
        self.game_on = True
        self.winning = True

        #Create grid
        for c in range(grid_size):
            for r in range(grid_size):
                cell = Cell(self._parent,c,r)
                cell.get_btn_instance().grid(column=c,row=r)
                self._grid[(c,r)] = cell

        #Set random bombs
        bomb_cells : list[Cell] = random.choices([self._grid[k] for k in self._grid.keys()],k=bomb_count)
        for cell in bomb_cells:
            cell.set_to_bomb()

        #Count all near bombs
        for pos,cell in self._grid.items():
            cell : Cell

            #If cell do not have nothing written inside
            if not cell.is_set():

                #Search all near bombs
                bombs_near = self._count_near_bombs(pos)

                #If bombs > 0, write value to button text
                if bombs_near:
                    cell.set_cell_text(str(bombs_near))

            #Set neightbours
            cell.set_neightbours(self._get_neightbours(pos))

        #Display info and rules
        text  = 'Welcome to Minesweeper game!\nRules are simple:\n'
        text += ' - Discover and mark all bomb position\n'
        text += ' - Show all bomb-free position\n'

        text += 'How to play:\n'
        text += 'Right Click: Mark/Unmark cell as bomb\n'
        text += 'Left Click: Uncover cell\n'

        messagebox.showinfo('GAME START',text)

    def _get_neightbours(self,pos:tuple) -> list[Cell]:
        '''This method gets all neightbours of a given position'''
        #Get current column and row
        col,row = pos

        #Get all neightbours (3x3 excluding position itself)
        neightbours = []
        for c in range(3):
            for r in range(3):

                #Create position to access grid dictionary
                nb_pos = (col-1+c,row-1+r)

                #If is starting position, skip
                if nb_pos == pos:
                    continue

                #Get neightbour
                neightbour = self._grid.get(nb_pos)

                #If exists, save as new neightbour
                if neightbour:
                    neightbours.append(neightbour)

        return neightbours

    def _count_near_bombs(self,pos:tuple) -> int:
        ''' This method searchs for near bombs at the given position
            Return the number of bombs found'''
        #Get all neightbours
        neightbours : list[Cell] = self._get_neightbours(pos)

        #Return count of neightbours that are bombs
        return len([n for n in neightbours if n._is_bomb])

    def check_game_task(self,event=None):
        '''This method checks game rules'''
        all_not_bomb_cell_discovered = True
        all_bomb_cell_flagged = True
        for cell in self._grid.values():
            cell : Cell

            #Check if cell is not bomb and is not pressed
            if not cell.is_bomb() and not cell.is_pressed():
                #Not all cells are discovered, keep playing
                all_not_bomb_cell_discovered = False

            #Check if cell is bomb and is pressed
            if cell.is_bomb() and cell.is_pressed():
                #Player have stepped on a mine, gameover
                self.winning = False
                self.game_on = False

            #Check if cell is bomb and is not marked
            if cell.is_bomb() and not cell.is_marked():
                #Wait untill player mark all bombs
                all_bomb_cell_flagged = False


        #If game still on (no bomb has been stepped on)
        if self.game_on:
            #If player found discovered all not bomb and marked all bombs
            if all_not_bomb_cell_discovered and all_bomb_cell_flagged:
                #Game ended
                self.game_on = False

        if not self.game_on:
            if self.winning:
                messagebox.showinfo('WIN','You win!\nYou successfully cleared the field!')
            else:
                messagebox.showerror('GAMEOVER','****Kabooooom****\n\nYou stepped on a mine.')

            self._parent.destroy()

            



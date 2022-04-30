import random
import tkinter as tk


from game import MineSweeper


class MineSweeperGUI:

    def __init__(self):
        self.root = tk.Tk()
        mMineSweeper = MineSweeper(self.root,grid_size=20,bomb_count=10)
        self.schedule_function(mMineSweeper.check_game_task,10)
        self.root.mainloop()

    def schedule_function(self,func,timeout:int):
        '''This method schedules a function to be executed every timeout timer'''

        #Create a scheduled function that recalls itself
        def scheduled_func():
            func()
            self.root.after(timeout,scheduled_func)

        #Start scheduling
        self.root.after(timeout,scheduled_func)
        

if __name__ == '__main__':
    MineSweeperGUI()
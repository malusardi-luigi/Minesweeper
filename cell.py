import tkinter as tk


class Cell:

    def __init__(self,parent:tk.Widget,column:int,row:int):

        #Save data
        self._default_color = parent['background']
        self._column        = column
        self._row           = row
        self._is_bomb       = False
        self._status        = 'hidden'
        self._neightbours :list[Cell] = []

        #Create associated button
        self._btn = tk.Button(parent,text=' ',width=2,height=1,command=self._press)
        self._btn.bind('<Button-3>',self._mark)
        self._btn.configure(foreground=self._btn['background'])

    def _press(self,e=None):
        '''This method is called when the button associated to the cell is pressed'''
        self._btn.configure(foreground='black',relief='sunken',background='darkgrey')
        self._status = 'pressed'

        #If button do not have text, uncover all neightbours
        if not self.is_set():
            for neightbour in self._neightbours:
                if not neightbour.is_pressed():
                    neightbour._press()

    def _mark(self,e=None):
        '''This method is called to mark the associated cell as probable mine position'''
        #If button already pressed
        if self._status == 'pressed':
            return
        
        #If button is not already marked
        if self._status != 'marked':
            #Mark button
            self._btn.configure(background='red',foreground='red')
            self._status = 'marked'
        else:
            #Unmark button
            self._btn.configure(background=self._default_color,
                                foreground=self._default_color)
            self._status = 'hidden'

    def get_pos(self) -> tuple:
        '''Return position of cell as a tuple (column,row)'''
        return (self._column,self._row)

    def set_cell_text(self,text:str):
        '''This method sets the text of the cell'''
        self._btn.configure(text=text)

    def set_to_bomb(self):
        '''This method sets a bomb in this cell'''
        self._is_bomb = True
        self.set_cell_text('B')

    def set_neightbours(self,neightbours:list):
        '''This method sets the neightbours of this cell'''
        self._neightbours = neightbours

    def get_btn_instance(self) -> tk.Button:
        '''This method returns the button instance of cell to allow for grid display'''
        return self._btn

    def is_bomb(self) -> bool:
        '''This method return True if the cell is a bomb'''
        return self._is_bomb

    def is_pressed(self) -> bool:
        '''Returns True if the cell is pressed'''
        return self._status == 'pressed' 

    def is_marked(self) -> bool:
        '''This method returns True if the cell is marked'''
        return self._status == 'marked' 

    def is_set(self) -> bool:
        '''Returns True if the cell have something written in it'''
        return self._btn['text'] != ' '
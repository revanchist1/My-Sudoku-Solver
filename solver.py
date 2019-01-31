# Sudoku solver version 0.1 
# Created by Soren Sabet Sarvestany based on strategies learned while playing sudoku
# 01-13-2019 1:28 AM

import numpy as np
import math

# Overall strategy:
# Create a cell object  
# Create a row object 
# Create a column object 
# Create a block object

# Create a function to read in a puzzle from a text file (for now)
# Create a function to update cells, rows, and colummn objects, and blocks
# Try to use pointers, so that each row, column, and block's elements are each cell. 

class cell:
    def __init__(self):
        self.value = np.nan
        self.possible_values = [1,2,3,4,5,6,7,8,9]
        self.impossible_values = []
        self.row = np.nan # Row number, ranges from 1-9 as defined below 
        self.col = np.nan # Column number, ranges from 1-9 as defined below
        self.box = np.nan # Box number, ranges from 1-9 as defined below 
        self.cell_id = (row,col)

class row: 
    def __init__(self):
        self.position = np.nan  # ranges from 1-9, top to bottom 
        self.cells = []

class col: 
    def __init__(self):         # ranges from 1-9, left to right 
        self.position = np.nan 
        self.cells = []
        
class box:
    def __init__(self):
        self.position = np.nan # ranges from 1-9, 1 2 3 | 4 5 6| 7 8 9 
        self.cells = []
        
class grid:
    def __init__(self):
        self.complete = False 
        self.correct = False
        self.rows = []
        self.cols = []
        self.boxes = []
        self.unsolved_cells[]
    
    def print_grid(self):
        top_row = '┌─────────┬─────────┬─────────┐'
        mid_row = '├─────────┼─────────┼─────────┤'
        bot_row = '└─────────┴─────────┴─────────┘'
        
        print(top_row)
        for i in range(0,9):
            row_string = '|'
            for j in range(0,9):
                cell_val = self.rows[i].cells[j].value
                if (np.isnan(cell_val)):
                    cell_val = ' '
                else:
                    cell_val = int(cell_val)
                    
                row_string += ' ' + str(cell_val) + ' ' 
                if (j == 2 or j == 5 or j == 8):
                    row_string += '|'
                #if (j % 3 == 0):
                #    row_string += '|'
            print(row_string)
            if (i == 2 or i == 5):
                print(mid_row)
        print(bot_row)

def initialize_grid(brd):
    # Fill the grid with row, column, and boxes 
    for i in range(1,10):
        brd.rows.append(row())
        brd.cols.append(col())
        brd.boxes.append(box())
    
def process_starting_input(inp):
    the_grid = grid()
    initialize_grid(the_grid) # Now grid has rows, columns, and boxes

    # Input: The raw input 
    # Output: Filters the raw game grid, and fills in rows, columns, and boxes with the appropriate cells. 
    for i in range(1,10):        # Row num
        for j in range(1,10):    # Col num
            curr_cell = cell()
            curr_cell.cell_id = (i,j)
            curr_cell.row = i 
            curr_cell.col = j 
            curr_cell.box = 3*int((i-1)/3) + max(1,math.ceil((j)/3))
            curr_cell.value =inp[i-1,j-1]
            if np.isnan(curr_cell.value) == False:
                curr_cell.possible_values = []
                curr_cell.impossible_values = [] 
            the_grid.unsolved_cells.append(curr_cell)
            the_grid.rows[i-1].cells.append(curr_cell)
            the_grid.cols[j-1].cells.append(curr_cell)
            the_grid.boxes[curr_cell.box-1].cells.append(curr_cell)
            #print('Appended cell %s to box %d!' % (str(curr_cell.cell_id), curr_cell.box))
    return the_grid                

# Step 1. Read in puzzle, and fill in rows, grids, and cells. 
n = np.nan
input_grid = np.array([[n,n,8,2,n,n,9,n,3],
                       [3,4,2,n,9,5,n,n,7],
                       [1,9,7,n,n,n,n,n,4],
                       [n,n,5,3,1,2,4,7,9],
                       [n,n,n,n,n,n,n,n,n],
                       [2,n,n,n,7,4,5,n,n],
                       [n,2,n,n,n,1,n,n,5],
                       [n,7,n,n,n,6,8,9,1],
                       [8,n,n,4,3,n,7,n,6]]) 
    
game_grid = process_starting_input(input_grid)
game_grid.print_grid()

# Step 1 - simple logic: For each cell in each row, check row, column and grid, and exclude possibilities. If only 1 left after all 3 checks, assign value, update, and show plot. 

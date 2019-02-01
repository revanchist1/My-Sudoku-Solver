# Sudoku solver version 0.2
# Created by Soren Sabet Sarvestany based on strategies learned while playing sudoku
# 01-13-2019 1:28 AM

import numpy as np
import math
import os 

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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

# Row, col, and box are essentially the same class. I can simplify the code by only using one class for these 3. 
class row: 
    def __init__(self):
        self.position = np.nan  # ranges from 1-9, top to bottom 
        self.cells = []
        self.impossible_values = []

class col: 
    def __init__(self):         # ranges from 1-9, left to right 
        self.position = np.nan 
        self.cells = []
        self.impossible_values = []
        
class box:
    def __init__(self):
        self.position = np.nan # ranges from 1-9, 1 2 3 | 4 5 6| 7 8 9 
        self.cells = []
        self.impossible_values = []
        
class grid:
    def __init__(self):
        self.complete = False 
        self.correct = False
        self.rows = []
        self.cols = []
        self.boxes = []
        self.unsolved_cells = []
    
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
        
    def explain_exclusions(self, cell, impossible_values, celltype, cellnum):
        exc_string = ''
        exc_values = []
        exc_count = 0
        pronoun = ''
        
        for idx, num in enumerate(impossible_values):
            try:
                cell.possible_values.remove(num)
                exc_values.append(num)
                exc_count += 1 
            except ValueError: 
                continue
        
        for idx, num in enumerate(exc_values):
            if (exc_count == 1):
                exc_string += str(num)
                pronoun = 'it is'
                break
            elif (exc_count == 2):
                if (idx == 0):
                    exc_string += str(num) + ' or '
                else:
                    exc_string += str(num) 
                pronoun = 'they are'
            else:
                pronoun = 'they are'
                if (idx == len(impossible_values)-1):
                    exc_string += 'or ' + str(num) 

                else:
                    exc_string += str(num) + ', '
        
        print('Cannot be ' + exc_string + ' because ' + pronoun + ' already in ' + celltype + ' # ' + str(cellnum))
        print('Possible values: ' + str(cell.possible_values))
        cell.possible_values.sort()
        
    def multi_cell_compare(self, cell, curr_obj, obj_name):
            # If two cells in the same row or column have n possible values that are the same, then they can be excluded from all other cells in that row and column. 
            # Step 1. Loop through all other cells in that row and column 
            # Step 2. Compare possible values in these cells to possible values in the current cell 
            # Step 3. If the possible values match, then exclude those possible values from all other cells in the row (if searching over row) or column (if searching over column)
            # The above works in a two number case, but what if there are more numbers? 
            # Suppose there were 3 numbers that I could exclude. 
            # Step 1. Count number of cells that have the same possible values 
            # Step 2. Count number of possible values. If this matches the number of cells, 
            # Step 3. Go to all unsolved cells that don't have the same possible values, and remove possible values from them. 
            
            print('')
            print('Now inside multi_cell_compare, examining ' + obj_name)
            print('Current cell: ' + str(cell.cell_id))
            
            count = 0
            cells_to_ignore = [cell]
            cells_to_ignore_ids = [cell.cell_id]
            cells_to_update = []
            
            for curr_cell in curr_obj.cells: 
                if (np.isnan(curr_cell.value) == False):
                    continue
                if (curr_cell == cell): # If we are at the same cell
                    count += 1
                    continue
                
                print('Comparison cell: ' + str(curr_cell.cell_id))
                print('Current cell possible values: ' + str(cell.possible_values))
                print('Comparison cell possible values: ' + str(curr_cell.possible_values))
                
                if (cell.possible_values == curr_cell.possible_values):
                    cells_to_ignore.append(curr_cell)
                    cells_to_ignore_ids.append(curr_cell.cell_id)
                    count += 1
                else:
                    cells_to_update.append(curr_cell)
            
            print('count: ' + str(count))
            print('cells_to_ignore: ' + str(len(cells_to_ignore)))
            print('cells_to_ignore_ids: ' + str(cells_to_ignore_ids))
            
            if (len(cells_to_ignore)==count and count > 1):
                for curr_cell in cells_to_update:
                    for val in cell.possible_values:
                        curr_cell.possible_values.remove(val)
                        print('Cell ' + str(curr_cell.cell_id) + ' cannot be any of ' + str(cell.possible_values) + ' because of cells: ' + str(cells_to_ignore_ids))
            return
            
    def iterate(self):
        solved_cells = []
        iterate_count = 0
        
        # Loops through each unsolved cell in the game board, and tries to solve.
        for cell in self.unsolved_cells:
            
            print('Now trying to solve cell: ' + str(cell.cell_id))
            print('Starting possible values: ' + str(cell.possible_values))
            
            # easier to understand code if I give the impossible values names
            row = self.rows[cell.row-1]
            col = self.cols[cell.col-1]
            box = self.boxes[cell.box-1]
            
            nums_in_row = row.impossible_values
            nums_in_col = col.impossible_values
            nums_in_box = box.impossible_values

            self.explain_exclusions(cell, nums_in_row, 'row', cell.row)
            self.explain_exclusions(cell, nums_in_col, 'column', cell.col)
            self.explain_exclusions(cell, nums_in_box, 'box', cell.box)

            self.multi_cell_compare(cell, row, 'row')
            #self.multi_cell_compare(cell, col, 'col')
            
            # If only 1 possible number, set cell value as that, and update row, col, and box possibilities, and remove from solved cells. 
            # otherwise, continue
            if len(cell.possible_values) == 1:
                cell.value = cell.possible_values[0]
                row.impossible_values.append(cell.value)
                col.impossible_values.append(cell.value)
                box.impossible_values.append(cell.value)
                solved_cells.append(cell)
                print('Solved this cell') # input logic to deal with correct cell later. 
            else:
                input('Press enter to continue')
            print('Unable to solve during this iteration, continuing to next empty cell!')
            cls()
            self.print_grid()
            iterate_count += 1
            if (iterate_count > 6):
                break
        
        for cell in solved_cells:
            self.unsolved_cells.remove(cell)                    
        

            # Since the more populated a row, grid, or column is, the more information  
            # it provides on a first run, I should dynamically go through them. But that optimization 
            # can come later. 
            
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
            if np.isnan(curr_cell.value) == False: # If the cell has a value 
                curr_cell.possible_values = []
                curr_cell.impossible_values = [] 
                the_grid.rows[i-1].impossible_values.append(int(curr_cell.value))
                the_grid.cols[j-1].impossible_values.append(int(curr_cell.value))
                the_grid.boxes[curr_cell.box-1].impossible_values.append(int(curr_cell.value))
            else:
                the_grid.unsolved_cells.append(curr_cell) # Use this list to track empty cells to allow faster iteration
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
game_grid.iterate()

# Step 1 - simple logic: For each cell in each row, check row, column and grid, and exclude possibilities. If only 1 left after all 3 checks, assign value, update, and show plot. 

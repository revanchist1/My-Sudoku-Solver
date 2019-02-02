# Sudoku solver version 0.2
# Created by Soren Sabet Sarvestany based on strategies learned while playing sudoku
# 01-13-2019 1:28 AM

import copy 
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
        self.solved_cells = []
        self.changed_during_iteration = False # Infinite loop if no changes to gameboard after iteration 
    
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
        
        print('Now inside explain exclusions!')
        print('Impossible values inside column: ' + str(impossible_values))
        print('Possible values inside cell: ' + str(cell.possible_values))
        
        for idx, num in enumerate(impossible_values):
            try:
                cell.possible_values.remove(num)
                exc_values.append(num)
                exc_count += 1 
                print('Succesfully removed ' + str(num) + ' from possible values!')
            except ValueError: 
                #print('Error!')
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
       
        #print('exclusion count: ' + str(exc_count))
        
        if (exc_count > 0):
            print('Cannot be ' + exc_string + ' because ' + pronoun + ' already in ' + celltype + ' # ' + str(cellnum))
            cell.possible_values.sort()
            self.changed_during_iteration = True
        
    def multi_cell_compare(self, cell, curr_obj, obj_name):
            # If two cells in the same row or column or box have n possible values that are the same, then they can be excluded from all other cells in that row and column and box. 
            # Step 1. Loop through all other cells in that row and column and box
            # Step 2. Compare possible values in these cells to possible values in the current cell 
            # Step 3. If the possible values match, then exclude those possible values from all other cells in the row (if searching over row) or column (if searching over column) or box (if searching over box)
            # The above works in a two number case, but what if there are more numbers? 
            # Suppose there were 3 numbers that I could exclude. 
            # Step 1. Count number of cells that have the same possible values 
            # Step 2. Count number of possible values. If this matches the number of cells, 
            # Step 3. Go to all unsolved cells that don't have the same possible values, and remove possible values from them. 
            
#            print('')
#            print('Now inside multi_cell_compare, examining ' + obj_name)
#            print('Current cell: ' + str(cell.cell_id))
            
            count = 0
            cells_to_ignore = [cell]
            cells_to_ignore_ids = [cell.cell_id]
            cells_to_update = []
            cells_to_update_ids = []
            
            for curr_cell in curr_obj.cells: 
                if (np.isnan(curr_cell.value) == False):
                    continue
                if (curr_cell == cell): # If we are at the same cell
                    count += 1
                    continue
                
                # I need a way to update the current cells possible values based on the box, row, or column being considered 
                if (obj_name == 'col'):
                    item = cell.col
                elif (obj_name == 'row'):
                    item = cell.row
                elif (obj_name == 'box'):
                    item = cell.box
                
                self.explain_exclusions(curr_cell, curr_cell.impossible_values, obj_name, item)
                
#                print('Comparison cell: ' + str(curr_cell.cell_id))
#                print('Current cell possible values: ' + str(cell.possible_values))
#                print('Comparison cell possible values: ' + str(curr_cell.possible_values))
                
                if (cell.possible_values == curr_cell.possible_values):
                    cells_to_ignore.append(curr_cell)
                    cells_to_ignore_ids.append(curr_cell.cell_id)
                    count += 1
                else:
                    cells_to_update.append(curr_cell)
                    cells_to_update_ids.append(curr_cell.cell_id)
            
#            print('count: ' + str(count))
#            print('cells_to_ignore: ' + str(len(cells_to_ignore)))
#            print('cells_to_ignore_ids: ' + str(cells_to_ignore_ids))
            
            explanation_string = 'Since cells ' + str(cells_to_ignore_ids) + ' can each only contain one of ' + str(cell.possible_values) + ', then cells ' + str(cells_to_update_ids) + ' cannot contain these values.' 
            
            if (len(cells_to_ignore)==count and count > 1 and len(cells_to_ignore[0].possible_values) == count):
                for curr_cell in cells_to_update:
                    if (np.isnan(curr_cell.value) == False):
                        continue
                    for val in cell.possible_values:
                        try:
                            curr_cell.possible_values.remove(val)
                            self.changed_during_iteration = True
                        except ValueError:
                            pass
                    #print('Cell ' + str(curr_cell.cell_id) + ' cannot be any of ' + str(cell.possible_values) + ' because of cells: ' + str(cells_to_ignore_ids))
                if (len(cells_to_update_ids) > 0):
                    print(explanation_string)
                    print('')
            return
    
    def column_cell_exclusions(self, cell, col_obj):
        # Check all empty cells in a column. If none of them can hold the value of interest, then it must go into the current cell. 
        count = 0
        cells_to_ignore = [cell]
        cells_to_ignore_ids = [cell.cell_id]
        cells_to_update = []
        cells_to_update_ids = []
        
        # Step 1. Update impossible values for every cell in the column. 
        for col_cell in col_obj.cells:
            if (np.isnan(col_cell.value) == False):
                continue
            print('Column impossible values: ' + str(self.cols[cell.col-1].impossible_values))
            print('Col cell: ' + str(col_cell.cell_id) + ' possible values: ' + str(col_cell.possible_values))
            self.explain_exclusions(col_cell, self.cols[cell.col-1].impossible_values, 'col', cell.col)
            print('Updated Col cell possible values: ' + str(col_cell.possible_values))

#        for val in cell.possible_values: 
#            for col_cell in col_obj.cells:
#                if (np.isnan(col_cell) == False):
#                    continue
#                
#                # Update impossible values for the column cell 
#                self.explain_exclusions(col_cell, col = self.cols[cell.col-1].impossible_values, 'col', cell.col)
#                
                
                
        
    def grid_cell_exclusions(self, cell, box_obj):
        # Okay. This function checks if a specific value can't exist in any other cell in the grid, based on the values present in other rows and columns that intersect with the grid 
        
        # Step 1: Loop over posible values in the cell 
        # Step 2: Loop over all other cells in the box 
        # Step 3: Check if the current possible value can be excluded based on row and column of all other cells in the grid 
        # Step 4: If the posible value can only eixst in that cell, then update the current value 
                
        for val in cell.possible_values:
            
            # Edge case, one is false, but the cell in that row is full. 
            # Edge case 1: Can't be in both rows, and 2 other column cells are full (along the row)
            # Edge case 2: Can't be in both columns, but 2 other row cells are full (along the column)
            
            # Get row num and column num 
            row_num = cell.row
            col_num = cell.col
            
            # Step 1. Functionality to check correct rows and columns 
            col1_idx = 0
            col2_idx = 0
            row1_idx = 0
            row2_idx = 0
            
            if (col_num % 3 == 0): # If column = 3,6,9
                col1_idx = col_num - 2 # col 1,4,7 
                col2_idx = col_num - 1 # col 2,5,8
            elif (col_num % 3 == 1):        
                col1_idx = col_num + 1 # col 2, 5, 8
                col2_idx = col_num + 2 # col 3, 6, 9
            elif (col_num % 3 == 2):
                col1_idx = col_num - 1 # col 1, 4, 7
                col2_idx = col_num + 1 # col 3, 6, 9
            col1cell = self.rows[cell.row-1].cells[col1_idx-1]
            col2cell = self.rows[cell.row-1].cells[col2_idx-1]
                
            if (row_num % 3 == 0): # If row = 3, 6, 9
                row1_idx = row_num - 2 # row 1, 4, 7
                row2_idx = row_num - 1
            elif (row_num % 3 == 1):
                row1_idx = row_num + 1
                row2_idx = row_num + 2
            elif (row_num % 3 == 2):
                row1_idx = row_num - 1
                row2_idx = row_num + 1 
            row1cell = self.cols[cell.col-1].cells[row1_idx-1]
            row2cell = self.cols[cell.col-1].cells[row2_idx-1]
#                print('Relevant column indices: ' + str(col1_idx) + ', ' + str(col2_idx))
#                print('Relevant row indices: ' + str(row1_idx) + ', ' + str(row2_idx))
            
            row1vals = self.rows[row1_idx-1].impossible_values
            row2vals = self.rows[row2_idx-1].impossible_values
            col1vals = self.cols[col1_idx-1].impossible_values
            col2vals = self.cols[col2_idx-1].impossible_values
            
#                print('row1_idx: ' + str(row1_idx))
#                print('row2_idx: ' + str(row2_idx))
#                print('row1cell id: ' + str(row1cell.cell_id))
#                print('row2cell id: ' + str(row2cell.cell_id))
#                print('col1_idx: ' + str(col1_idx))
#                print('col2_idx: ' + str(col2_idx))
#                print('col1cell id: ' + str(col1cell.cell_id))
#                print('col2cell id: ' + str(col2cell.cell_id))
      
            case1 = val in row1vals and val in row2vals and val in col1vals and val in col2vals
            case2 = val in row1vals and val in row2vals and np.isnan(col1cell.value) == False and np.isnan(col2cell.value) == False
            case3 = val in col1vals and val in col2vals and np.isnan(row1cell.value) == False and np.isnan(row2cell.value) == False
            case4 = val in col1vals and val in col2vals and val in row1vals and np.isnan(row2cell.value) == False
            case5 = val in col1vals and val in col2vals and val in row2vals and np.isnan(row1cell.value) == False
            case6 = val in row1vals and val in row2vals and val in col1vals and np.isnan(col2cell.value) == False
            case7 = val in row1vals and val in row2vals and val in col2vals and np.isnan(col1cell.value) == False
            
            print('Current value of interest: ' + str(val))
            
#                print('row1vals: ' + str(row1vals) + ' val in row1vals: ' + str(val in row1vals))
#                print('row2vals: ' + str(row2vals) + ' val in row2vals: ' + str(val in row2vals))
#                print('col1vals: ' + str(col1vals) + ' val in col1vals: ' + str(val in col1vals))
#                print('col2vals: ' + str(col2vals) + ' val in col2vals: ' + str(val in col2vals))
            
#                print('case1: ' + str(case1))
#                print('case2: ' + str(case2))
#                print('case3: ' + str(case3))
            if (case1 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in rows ' + str(row1_idx) + ' and ' + str(row2_idx) + ' and columns ' + str(col1_idx) + ' and ' + str(col2_idx))
            elif (case2 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in rows ' + str(row1_idx) + ' and ' + str(row2_idx) + ' and cells ' + str(col1cell.cell_id) + ' and ' + str(col2cell.cell_id) + ' are already populated')
            elif (case3 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in columns ' + str(col1_idx) + ' and ' + str(col2_idx) + ' and cells ' + str(row1cell.cell_id) + ' and ' + str(row2cell.cell_id) + ' are already populated')
            elif (case4 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in columns ' + str(col1_idx) + ' and ' + str(col2_idx) + ' and row ' + str(row1_idx) + ' and cell ' + str(row2cell.cell_id) + ' is already populated')
            elif (case5 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in columns ' + str(col1_idx) + ' and ' + str(col2_idx) + ' and row ' + str(row2_idx) + ' and cell ' + str(row1cell.cell_id) + ' is already populated')
            elif (case6 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in rows ' + str(row1_idx) + ' and ' + str(row2_idx) + ' and column ' + str(col1_idx) + ' and cell ' + str(col2cell.cell_id) + ' is already populated')
            elif (case7 == True):
                print('Cell ' + str(cell.cell_id) + ' can only be ' + str(val) + ' because there are ' + str(val) + '\'s in rows ' + str(row1_idx) + ' and ' + str(row2_idx) + ' and column ' + str(col2_idx) + ' and cell ' + str(col1cell.cell_id) + ' is already populated')

            # I actually needed to iterate over the cells in the grid. re-incorporate that functionality tomorrow. 

            # If the current possible value is impossible in all 4 of the above, then assign value to this cell. 
            if (case1 or case2 or case3 or case4 or case5 or case6 or case7):
                cell.possible_values = [val]
                return
            input ('Press enter to continue')


                # Need to get rows 
#                row = self.rows[cell.row-1]
#                col = self.cols[cell.col-1]
#                box = self.boxes[cell.box-1]
#                
#                if val in impossible_values of rows above and below and left-right column:
    
    def solve_cell(self, cell): 
        if (np.isnan(cell.value) == False):
            return 
        
        cls()
        self.print_grid()
        
        print('Now trying to solve cell: ' + str(cell.cell_id))
        print('Starting possible values: ' + str(cell.possible_values))
            
        # easier to understand code if I give the impossible values names
        row = self.rows[cell.row-1]
        col = self.cols[cell.col-1]
        box = self.boxes[cell.box-1]
        
        nums_in_row = row.impossible_values
        nums_in_col = col.impossible_values
        nums_in_box = box.impossible_values

#        if (len(cell.possible_values) != 1):
#            self.explain_exclusions(cell, nums_in_row, 'row', cell.row)
        if (len(cell.possible_values) != 1):
            self.explain_exclusions(cell, nums_in_col, 'column', cell.col)
#        if (len(cell.possible_values) != 1):
#            self.explain_exclusions(cell, nums_in_box, 'box', cell.box)
#        print('Possible values: ' + str(cell.possible_values))

#        if (len(cell.possible_values) != 1):
#            self.multi_cell_compare(cell, row, 'row')
#        if (len(cell.possible_values) != 1):
#            self.multi_cell_compare(cell, col, 'col')
#        if (len(cell.possible_values) != 1):
#            self.multi_cell_compare(cell, box, 'box')
        # Need multi-cell box solver as well, e.g. see cell (6,3) using left to right solution
            
#        if (len(cell.possible_values) != 1):
#            self.grid_cell_exclusions(cell, box)
#        if (len(cell.possible_values) != 1):
#            self.row_cell_exclusions(cell, row)
        if (len(cell.possible_values) != 1):
            self.column_cell_exclusions(cell, row)
        
        # If only 1 possible number, set cell value as that, and update row, col, and box possibilities, and remove from solved cells. 
        # otherwise, continue
        if len(cell.possible_values) == 1:
            cell.value = cell.possible_values[0]
            row.impossible_values.append(cell.value) # Probably better to use a set for impossible values, to avoid duplicate values being entered.
            col.impossible_values.append(cell.value)
            box.impossible_values.append(cell.value)
            self.solved_cells.append(cell)
            print('Solved this cell') # input logic to deal with correct cell later. 
            input ('Press enter to continue')

            # Recursion is fancy, but it is not intuitive for a human, and the objective is to have an interpretable sudoku solver. 
#            for row_cell in row.cells:
#                self.solve_cell(row_cell)
#            for col_cell in col.cells:
#                self.solve_cell(col_cell)
#            for box_cell in box.cells:
#                self.solve_cell(box_cell)
            
        else:
            print('Could not solve cell, continuing to next empty cell...')
            input('Press enter to continue 1')
            return 

            
    def iterate(self):
        self.changed_during_iteration = False
        
        # Loops through each unsolved cell in the game board, and tries to solve.
        for cell in self.unsolved_cells:
            if (np.isnan(cell.value) == False): # In case it was solved in a previous recursion instance
                self.solved_cells.append(cell)
            else:
                self.solve_cell(cell)
        
        for cell in self.solved_cells:
            try:
                self.unsolved_cells.remove(cell)          
            except ValueError:
                continue
        
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

#input_grid = np.array([[1,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n],
#                       [n,n,n,n,n,n,n,n,n]]) 
    
game_grid = process_starting_input(input_grid)
iter_count = 1

while True:
    game_grid.iterate()
    cls()
    print('Completed iteration # ' + str(iter_count))
    game_grid.print_grid()      
    iter_count += 1
    # Check if it has been solved or not
    if (len(game_grid.unsolved_cells) == 0):
        print('Congratulations! The program was able to solve this Sudoku puzzle')
        break
    elif (game_grid.changed_during_iteration == False):
        print('No changes were made during the previous iteration - no unique solution found')
        break
    
# Step 1 - simple logic: For each cell in each row, check row, column and grid, and exclude possibilities. If only 1 left after all 3 checks, assign value, update, and show plot. 

# Okay. Add code so that if there is only 1 element in each row, column, or box, it automatically solves it instead of going in order, then comes back to where it was. 
# Also need to add code so that if a human could obviously infer what the number would be based on surrounding empty cells in the same grid, then the algorithm should figure it out too. 
# Also need to add functionality to automatically loop until the game board has been sovled, or recognize when it is in an infinite loop. # This last feature will be easiest to implement first, because if I implement the others I might be able to solve the puzzle in one iteration. 

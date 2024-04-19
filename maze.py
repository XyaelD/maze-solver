import random
from time import sleep
from cell import Cell

LEFT_AND_UP = -1
RIGHT_AND_DOWN = 1

class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win=None,
                 seed=None
                 ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self.__win = win
        self._cells: list[Cell] = []
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        for _ in range(self._num_cols):
            curr_row = []
            for _ in range(self._num_rows):
                curr_row.append(Cell(self.__win))
            self._cells.append(curr_row)
            
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
        
    def _animate(self):
        self.__win.redraw()
        sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows -1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows -1)
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_cell_choices = []
            left_value = i - 1
            right_value = i + 1
            up_value = j - 1
            down_value = j + 1
            if left_value >= 0:
                if not self._cells[left_value][j].visited:
                    next_cell_choices.append([left_value, j, "left"])
            if right_value <= self._num_cols - 1:
                if not self._cells[right_value][j].visited:
                    next_cell_choices.append([right_value, j, "right"])
            if up_value >= 0:
                if not self._cells[i][up_value].visited:
                    next_cell_choices.append([i, up_value, "up"])
            if down_value <= self._num_rows - 1:
                if not self._cells[i][down_value].visited:
                    next_cell_choices.append([i, down_value, "down"])
            if len(next_cell_choices) == 0:
                self._draw_cell(i, j)
                return
            next_cell = random.choice(next_cell_choices)
            match next_cell[2]:
                case "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_right_wall = False                    
                case "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_left_wall = False
                case "up":
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_bottom_wall = False
                case "down":
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_top_wall = False
            self._break_walls_r(next_cell[0], next_cell[1])
            
    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False
                
    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True
        left_value = i - 1
        right_value = i + 1
        up_value = j - 1
        down_value = j + 1
        
        if left_value >= 0:
            if not self._cells[left_value][j].visited and not self._cells[i][j].has_left_wall:
                self._cells[i][j].draw_move(self._cells[left_value][j])
                if self._solve_r(left_value, j):
                    return True
                self._cells[i][j].draw_move(self._cells[left_value][j], undo=True)
                
        if right_value <= self._num_cols - 1:
            if not self._cells[right_value][j].visited and not self._cells[i][j].has_right_wall:
                self._cells[i][j].draw_move(self._cells[right_value][j])
                if self._solve_r(right_value, j):
                    return True
                self._cells[i][j].draw_move(self._cells[right_value][j], undo=True)
                
        if up_value >= 0:
            if not self._cells[i][up_value].visited and not self._cells[i][j].has_top_wall:
                self._cells[i][j].draw_move(self._cells[i][up_value])
                if self._solve_r(i, up_value):
                    return True
                self._cells[i][j].draw_move(self._cells[i][up_value], undo=True)
                
        if down_value <= self._num_rows - 1:
            if not self._cells[i][down_value].visited and not self._cells[i][j].has_bottom_wall:
                self._cells[i][j].draw_move(self._cells[i][down_value])
                if self._solve_r(i, down_value):
                    return True
                self._cells[i][j].draw_move(self._cells[i][down_value], undo=True)
        
        return False      
from graphics import Line, Point

class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window
        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        if self.has_left_wall:
            left_wall = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(left_wall)
        else:    
            left_wall = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(left_wall, "white")
                        
        if self.has_right_wall:
            right_wall = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(right_wall)
        else:
            right_wall = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(right_wall, "white")
                            
        if self.has_top_wall:
            top_wall = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(top_wall)
        else:
            top_wall = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(top_wall, "white")
            
        if self.has_bottom_wall:
            bottom_wall = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(bottom_wall)
        else:
            bottom_wall = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(bottom_wall, "white")            
            
        
    def draw_move(self, to_cell, undo=False):
        own_x_center = (self._x1 + self._x2) // 2
        own_y_center = (self._y1 + self._y2) // 2
        other_x_center = (to_cell._x1 + to_cell._x2) // 2
        other_y_center = (to_cell._y1 + to_cell._y2) // 2
        line = Line(Point(own_x_center, own_y_center), Point(other_x_center, other_y_center))
        if not undo:
            self._win.draw_line(line, "red")
        else:
            self._win.draw_line(line, "gray")
    
               
    def __repr__(self) -> str:
        return "Cell"
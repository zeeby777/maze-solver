from tkinter import Tk, BOTH, Canvas

class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line():
    def __init__(self, pointA: Point, pointB: Point):
        self.pointA = pointA
        self.pointB = pointB

    def draw(self, canvas: Canvas, fill_color: str, width: int):
        canvas.create_line(self.pointA.x, self.pointA.y, self.pointB.x, self.pointB.y, fill=fill_color, width=width)

class Cell():
    def __init__(self, top_left_corner: Point = None, bottom_right_corner: Point = None, walls: list[str] = ['top', 'bottom', 'left', 'right']):
        self.walls = walls

        self.x0 = top_left_corner.x
        self.y0 = top_left_corner.y
        self.x1 = bottom_right_corner.x
        self.y1 = bottom_right_corner.y

        self.bottom_right_corner = bottom_right_corner
        self._win = win         #referencing global var 

    def draw(self, canvas: Canvas, fill_color: str, width: int):
        if('left' in self.walls):
            Line(
                Point(self.x0, self.y0),
                Point(self.x0, self.y1)
            ).draw(canvas, fill_color, width)
        if('right' in self.walls):
            Line(
                Point(self.x1, self.y0),
                Point(self.x1, self.y1)
            ).draw(canvas, fill_color, width)
        if('top' in self.walls):
            Line(
                Point(self.x0, self.y0),
                Point(self.x1, self.y0)
            ).draw(canvas, fill_color, width)
        if('bottom' in self.walls):
            Line(
                Point(self.x0, self.y1),
                Point(self.x1, self.y1)
            ).draw(canvas, fill_color, width)

    def draw_move(self, to_cell: 'Cell', undo=False):
        self_center = Point(
            ((self.x0 + self.x1) / 2), 
            ((self.y0 + self.y1) / 2))
        
        destination_center = Point(
            ((to_cell.x0 + to_cell.x1) / 2), 
            ((to_cell.y0 + to_cell.y1) / 2)
        )

        self._win.draw_line(Line(self_center, destination_center), ('gray', 'red') [undo], 2)

class Maze():
    def _draw_cell(self, col, row):
        pass

    def _create_cells(self):
        for col in range(self.num_cols):
            self._cells[col] = []
            for row in range(self.num_rows):
                self._cells[col][row] = Cell()
                self._draw_cell(col, row)

    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, win: 'Window'):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._cells: list[Cell] = None

        self._create_cells(self)




class Window():
    def __init__(self, width: int, height: int):
        self.__rootWidget = Tk()
        self.__rootWidget.title = "Maze solver"
        self.__rootWidget.geometry(f"{width}x{height}")
        self.__rootWidget.protocol("WM_DELETE_WINDOW", self.close())

        self.__canvas = Canvas()
        self.__canvas.pack()

        self.__running = False
    
    def redraw(self):
        self.__rootWidget.update_idletasks()
        self.__rootWidget.update()
    
    def wait_for_close(self):

        self.__running = True

        while(self.__running):
            self.redraw()
    
    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str, width: int):
        line.draw(self.__canvas, fill_color, width)

    def draw_cell(self, cell: Cell, fill_color: str, width: int):
        cell.draw(self.__canvas, fill_color, width)



if __name__ == "__main__":
    win = Window(800, 600)
    cell = Cell(
             Point(10, 20),
             Point(20, 10),
             ['top', 'bottom', 'left']
             )
    cell2 = Cell( 
            Point(50, 20),
            Point(60, 10),
            ['top', 'bottom', 'right'],
            )
    win.draw_cell(cell, 'black', 2)
    win.draw_cell(cell2, 'black', 2)
    cell.draw_move(cell2)
    win.wait_for_close()
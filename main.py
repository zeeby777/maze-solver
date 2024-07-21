from tkinter import Tk, BOTH, Canvas
import time, random

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
    def __init__(self, top_left_corner: Point = None, bottom_right_corner: Point = None, walls: list[str] = ['top', 'bottom', 'left', 'right'], win: 'Window' = None):
        self.walls = walls

        if(top_left_corner):
            self.x0 = top_left_corner.x
            self.y0 = top_left_corner.y
        if(bottom_right_corner):
            self.x1 = bottom_right_corner.x
            self.y1 = bottom_right_corner.y

        self.visited = False

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
    def _animate(self):
        win.redraw()
        time.sleep(0.05)
        

    def _draw_cell(self, col, row):
        top_left_corner = Point(
            self.x0 + col * self.cell_size_x, 
            self.y0 + row * self.cell_size_x)
        
        bottom_right_corner = Point(
            top_left_corner.x + self.cell_size_x,
            top_left_corner.y + self.cell_size_y
        )


        walls = ['top', 'left', 'right', 'bottom']
        if(col == 0 and row == 0):
            walls.remove('top')
        if(row == num_rows - 1 and col == num_cols - 1):
            walls.remove('bottom')
            print("created exit")
        

        cell = Cell(top_left_corner, bottom_right_corner, walls)
        win.draw_cell(cell, 'black', 2)
        self._animate()

    def _break_walls_r(self, col, row):
        current_cell = self._cells[col][row]
        current_cell.visited = True
        while True:
            DIRECTIONS = {
                'left': (-1, 0), 
                'top': (1, 0), 
                'bottom': (0, -1), 
                'right': (0, 1)}
            destinations = []

            for dir_name, offset in DIRECTIONS.items():
                try:
                    potential_destination = self._cells[col + offset[0]][row + offset[1]]
                except IndexError:
                    continue

                if(potential_destination.visited == False):
                    destinations.append({
                        'dest_cell': potential_destination,
                        'dest_dirname': dir_name,
                        'dest_offset': offset
                    })

            if(destinations == []):
                win.draw_cell(current_cell, 'black', 2)
                return
            else:
                result = random.choice(destinations)
                print(result['dest_cell'].visited)

                try:
                    result['dest_cell'].walls.remove(result['dest_dirname'])
                except:
                    pass

                self._break_walls_r(col + result['dest_offset'][0], row + result['dest_offset'][1])

    def _create_cells(self):
        for col in range(self.num_cols):
            self._cells.append([])
            for row in range(self.num_rows):
                self._cells[col].append(Cell())
                
        self._break_walls_r(0, 0)

        for col in self._cells:
            for row in self._cells:
                win.draw_cell(self._cells[col][row], 'black', 2)


                
                
                

    def __init__(self, x0: int, y0: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, win: 'Window' = None, seed: bool = False):
        self.x0 = x0
        self.y0 = y0
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if(seed == False):
            random.seed(0)
        else:
            random.seed()


        self._cells: list[Cell][Cell] = []

        self._create_cells()




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
        print(f"x0 {cell.x0} y0 {cell.y0} x1 {cell.x1} y1 {cell.y1}")
        print(cell.walls)
        cell.draw(self.__canvas, fill_color, width)



if __name__ == "__main__":
    win = Window(800, 600)
    num_rows = 3
    num_cols = 2
    m1 = Maze(20, 20, num_rows, num_cols, 20, 20)
    print("finished creating maze")
    
    win.wait_for_close()
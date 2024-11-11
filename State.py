import copy
import time

class State:
    
    def __init__(self, grid, status, previous):
        self.grid = grid  
        self.status = status 
        self.previous = previous
        self.next_states = None


    def print_grid(self):
        for row in self.grid:
            for cell in row:
                if cell.cell_type == "empty":
                    print("0", end=" ")
                elif cell.cell_type == "wall":
                    print("1", end=" ")
                elif cell.cell_type == "player":
                    print(cell.color, end=" ")
                elif cell.cell_type == "target":
                    print(f"{cell.cell_type}_{cell.color}", end=" ")
                elif cell.cell_type == "merge":
                    print(f"{cell.cell_type}_{cell.color}_{cell.color2}", end=" ")
            print()  
    
    def check(self, other_state):
        if len(self.grid) != len(other_state.grid):
            print(False)
            return 
        for row_self, row_other in zip(self.grid, other_state.grid):
            if len(row_self) != len(row_other):
                print(False)
                return
            for cell_self, cell_other in zip(row_self, row_other):
                if cell_self.cell_type != cell_other.cell_type or cell_self.color != cell_other.color:
                    print(False)
                    return
        print(True)
        return
    
    def win(self):
        for row in self.grid:
            for cell in row:
                if cell.cell_type == "player" or cell.cell_type == "merge":
                    print("still play")
                    return True
        print("End game")
        return False
    
    def move_players_right(self):
        new_grid = copy.deepcopy(self.grid)
        updated_colors = [] 
        for row in range(len(new_grid)):
            for col in range(len(new_grid[0])):
                if new_grid[row][col].cell_type == "player" or new_grid[row][col].cell_type == "merge":
                    if new_grid[row][col].color in updated_colors:
                        continue 
                    next_col = col + 1
                    while next_col < len(new_grid[0]) and new_grid[row][next_col].cell_type != "wall" and new_grid[row][next_col].cell_type != "player" and new_grid[row][next_col].cell_type != "merge":
                        if new_grid[row][col].cell_type == "player":
                            if new_grid[row][next_col].cell_type == "empty":
                                new_grid[row][next_col].cell_type = "player"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color == new_grid[row][next_col].color:
                                new_grid[row][next_col].cell_type = None
                                new_grid[row][next_col].color = None
                                new_grid[row][col].cell_type = None
                                new_grid[row][col].color = None
                                break
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color != new_grid[row][next_col].color:
                                color2 = new_grid[row][next_col].color
                                new_grid[row][next_col].cell_type = "merge"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][next_col].color2 = color2
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                        else :
                            if new_grid[row][next_col].cell_type == "empty":
                                new_grid[row][next_col].cell_type = "player"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color == new_grid[row][next_col].color:
                                new_grid[row][next_col].cell_type = "empty"
                                new_grid[row][next_col].color = None
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color != new_grid[row][next_col].color:
                                color = new_grid[row][next_col].color
                                new_grid[row][next_col].cell_type = "merge"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][next_col].color2 = color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                        col = next_col 
                        next_col += 1
                    updated_colors.append(new_grid[row][col].color)
        new_state1 = State(new_grid,self.status,self)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self)
        return new_state

    def move_players_left(self):
        new_grid = copy.deepcopy(self.grid)
        updated_colors = []
        for row in range(len(new_grid)):
            for col in range(len(new_grid[0])-1,-1,-1):
                if new_grid[row][col].cell_type == "player" or new_grid[row][col].cell_type == "merge":
                    if new_grid[row][col].color in updated_colors:
                        continue 
                    next_col = col - 1
                    while next_col >= 0 and new_grid[row][next_col].cell_type != "wall" and new_grid[row][next_col].cell_type != "player" and new_grid[row][next_col].cell_type != "merge":
                        if new_grid[row][col].cell_type == "player":
                            if new_grid[row][next_col].cell_type == "empty":
                                new_grid[row][next_col].cell_type = "player"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color == new_grid[row][next_col].color:
                                new_grid[row][next_col].cell_type = "empty"
                                new_grid[row][next_col].color = None
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                                break
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color != new_grid[row][next_col].color:
                                color2 = new_grid[row][next_col].color
                                new_grid[row][next_col].cell_type = "merge"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][next_col].color2 = color2
                                print(new_grid[row][next_col].color2)
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                        else :
                            if new_grid[row][next_col].cell_type == "empty":
                                new_grid[row][next_col].cell_type = "player"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color == new_grid[row][next_col].color:
                                new_grid[row][next_col].cell_type = "empty"
                                new_grid[row][next_col].color = None
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[row][next_col].cell_type == "target" and new_grid[row][col].color != new_grid[row][next_col].color:
                                color = new_grid[row][next_col].color
                                new_grid[row][next_col].cell_type = "merge"
                                new_grid[row][next_col].color = new_grid[row][col].color
                                new_grid[row][next_col].color2 = color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                        col = next_col
                        next_col -= 1
                    updated_colors.append(new_grid[row][col].color)
        new_state1 = State(new_grid,self.status,self)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self)
        return new_state

    def move_players_up(self):
        new_grid = copy.deepcopy(self.grid)
        updated_colors = []
        for col in range(len(new_grid[0])):
            for row in range(len(new_grid)-1,-1,-1): 
                if new_grid[row][col].cell_type == "player" or new_grid[row][col].cell_type == "merge":
                    if new_grid[row][col].color in updated_colors:
                        continue 
                    next_row = row - 1
                    while next_row >= 0 and new_grid[next_row][col].cell_type != "wall" and new_grid[next_row][col].cell_type != "player" and new_grid[next_row][col].cell_type != "merge":
                        if new_grid[row][col].cell_type == "player":
                            if new_grid[next_row][col].cell_type == "empty":
                                new_grid[next_row][col].cell_type = "player"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color == new_grid[next_row][col].color:
                                new_grid[next_row][col].cell_type = "empty"
                                new_grid[next_row][col].color = None
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                                break
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color != new_grid[next_row][col].color:
                                color2 = new_grid[next_row][col].color
                                new_grid[next_row][col].cell_type = "merge"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[next_row][col].color2 = color2
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                        else :
                            if new_grid[next_row][col].cell_type == "empty":
                                new_grid[next_row][col].cell_type = "player"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color == new_grid[next_row][col].color:
                                new_grid[next_row][col].cell_type = "empty"
                                new_grid[next_row][col].color = None
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color != new_grid[next_row][col].color:
                                color = new_grid[next_row][col].color
                                new_grid[next_row][col].cell_type = "merge"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[next_row][col].color2 = color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                        row = next_row
                        next_row -= 1
                    updated_colors.append(new_grid[row][col].color)
        new_state1 = State(new_grid,self.status,self)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self)
        return new_state

    def move_players_down(self):
        new_grid = copy.deepcopy(self.grid)
        updated_colors = []
        for col in range(len(new_grid[0])):
            for row in range(len(new_grid)):
                if new_grid[row][col].cell_type == "player" or new_grid[row][col].cell_type == "merge":
                    if new_grid[row][col].color in updated_colors:
                        continue 
                    next_row = row + 1
                    while next_row < len(new_grid) and new_grid[next_row][col].cell_type not in ["wall", "player", "merge"]:
                        if new_grid[row][col].cell_type == "player":
                            if new_grid[next_row][col].cell_type == "empty":
                                new_grid[next_row][col].cell_type = "player"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color == new_grid[next_row][col].color:
                                new_grid[next_row][col].cell_type = "empty"
                                new_grid[next_row][col].color = None
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                                break
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color != new_grid[next_row][col].color:
                                color2 = new_grid[next_row][col].color
                                new_grid[next_row][col].cell_type = "merge"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[next_row][col].color2 = color2
                                new_grid[row][col].cell_type = "empty"
                                new_grid[row][col].color = None
                        else:
                            if new_grid[next_row][col].cell_type == "empty":
                                new_grid[next_row][col].cell_type = "player"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color == new_grid[next_row][col].color:
                                new_grid[next_row][col].cell_type = "empty"
                                new_grid[next_row][col].color = None
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                            elif new_grid[next_row][col].cell_type == "target" and new_grid[row][col].color != new_grid[next_row][col].color:
                                color = new_grid[next_row][col].color
                                new_grid[next_row][col].cell_type = "merge"
                                new_grid[next_row][col].color = new_grid[row][col].color
                                new_grid[next_row][col].color2 = color
                                new_grid[row][col].cell_type = "target"
                                new_grid[row][col].color = new_grid[row][col].color2
                                new_grid[row][col].color2 = None
                        row = next_row
                        next_row += 1
                    updated_colors.append(new_grid[row][col].color)
        new_state1 = State(new_grid,self.status,self)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self)
        return new_state
    

    def next_states_create(self):
        down = self.move_players_down()
        up = self.move_players_up()
        right = self.move_players_right()
        left = self.move_players_left()
        self.next_states = {
            "down": down,
            "up": up,
            "right": right,
            "left": left
        }



    

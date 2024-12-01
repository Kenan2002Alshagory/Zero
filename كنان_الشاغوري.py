
##########################
#صف الخلية 
#من خلال نعرف خلية من نوع هدف او لاعب او طريق او جدار 
##########################
class Cell:
    def __init__(self, cell_type, color, color2):
        self.cell_type = cell_type
        self.color = color
        self.color2 = color2

    def change_color(self, new_color):
        self.color = new_color

    def change_type(self, new_cell_type):
        self.cell_type = new_cell_type


##########################
#صف الحالة
#كل حالة تعبر عن رقعة تحمل مصفوفة من الخلايا و مجموعة من الحالات اللاحقة و الحالة الاب 
#و ما يعبر عن كون الحالة حالة فوز او لاء 
#يوجد توابع الحركة وتابع لتحقق من تساوي حالتين 
##########################

import copy

class State:
    
    def __init__(self, grid, status, previous,priority):
        self.grid = grid  
        self.status = status 
        self.previous = previous
        self.next_states = None
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

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
            return False
        for row_self, row_other in zip(self.grid, other_state.grid):
            if len(row_self) != len(row_other):
                return False
            for cell_self, cell_other in zip(row_self, row_other):
                if cell_self.cell_type != cell_other.cell_type or cell_self.color != cell_other.color:
                    return False
        return True
    
    def win(self):
        for row in self.grid:
            for cell in row:
                if cell.cell_type == "player" or cell.cell_type == "merge":
                    return True
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
        new_state1 = State(new_grid,self.status,self,self.priority)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self,self.priority)
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
        new_state1 = State(new_grid,self.status,self,self.priority)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self,self.priority)
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
        new_state1 = State(new_grid,self.status,self,self.priority)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self,self.priority)
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
        new_state1 = State(new_grid,self.status,self,self.priority)
        is_win = new_state1.win()
        new_state = State(new_grid,is_win,self,self.priority)
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

########################
#صف الرسم
#يعطي واجهات في حال المستخدم يريد اللعب 
########################

import pygame

class GameGUI:
    def __init__(self, width=550, height=500):
        self.cell_size = 50
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Zero Squares")
        self.clock = pygame.time.Clock()

    def draw_grid(self, state):
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        for i, row in enumerate(state.grid):
            for j, cell in enumerate(row):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                # Determine the color based on the cell type
                if cell.cell_type == "empty":
                    color = (255, 255, 255)  # White
                elif cell.cell_type == "wall":
                    color = (0, 0, 0)  # Black
                elif cell.cell_type == "player":
                    color = cell.color
                elif cell.cell_type == "target":
                    color = cell.color # White
                elif cell.cell_type == "merge":
                    color = cell.color

                # Draw the cell
                pygame.draw.rect(self.screen, color, (x1, y1, self.cell_size, self.cell_size))

                # Add text for target and merge cells
                if cell.cell_type == "target" or cell.cell_type == "merge":
                    font = pygame.font.SysFont(None, 24)
                    text_surface = font.render(cell.cell_type, True, cell.color if cell.cell_type == "merge" else (0, 0, 0))
                    self.screen.blit(text_surface, ((x1 + x2) // 2 - text_surface.get_width() // 2, (y1 + y2) // 2 - text_surface.get_height() // 2))

        pygame.display.flip()  # Update the display

    def update_grid(self, new_state):
        self.draw_grid(new_state)  # Redraw the grid based on the new state


########################
#صف الخوارزميات 
#يحتوي الخوارزميات لحل اللعبة تلقائيا
########################

import queue
class Algorithm:

  def __init__(self,init_state):
    self.init_state = init_state  


###############################################################################################

  def BFS(self):

    q = queue.Queue()
    path = []
    visited = []
    q.put(self.init_state)

    while not q.empty():

      current_state = q.get()
      visited.append(current_state)

      #################if game End#############################
      if current_state.status == False:
        path.append(current_state)
        while current_state.previous is not None:
          current_state = current_state.previous
          path.append(current_state)
        path.reverse()
        return path
      
      ##################if game not End#########################
      current_state.next_states_create()
      
      ###Add next states to queue
      for direction, state in current_state.next_states.items():
        if not any(state.check(visited_state) for visited_state in visited):
          q.put(state)

###############################################################################################


  def DFS(self):
        
    stack = []
    path = []
    visited = []
    stack.append(self.init_state)

    while stack:
      current_state = stack.pop()
      visited.append(current_state)

      #################if game End#############################
      if current_state.status == False:
          path.append(current_state)
          while current_state.previous is not None:
              current_state = current_state.previous
              path.append(current_state)
          path.reverse()
          return path

      ##################if game not End#########################
      current_state.next_states_create()

      ###Add next states to stack
      for direction, state in current_state.next_states.items():
          if not any(state.check(visited_state) for visited_state in visited):
              stack.append(state)


###########################################################################################

  def DFS_recursive(self, current_state=None, visited=None, path=None):
      if visited is None:
          visited = []
      if path is None:
          path = []
      
      if current_state is None:
          current_state = self.init_state

      visited.append(current_state)

      if current_state.status == False:  
          while current_state is not None:
              path.append(current_state)
              current_state = current_state.previous
          path.reverse()
          return path

      current_state.next_states_create()

      for direction, state in current_state.next_states.items():
          if not any(state.check(visited_state) for visited_state in visited):
              result = self.DFS_recursive(state, visited, path)
              if result:
                  return result

      return None


############################################################################################

  def UCS(self): 
    # Priority Queue for UCS (min-heap)
    pq = queue.PriorityQueue()
    path = []
    visited = []
    
    # Push initial state with cost 0
    pq.put((self.init_state.priority, self.init_state))

    while not pq.empty():
        # Pop the state with the lowest cost
        cost, current_state = pq.get()

        # Check if already visited
        if any(current_state.check(visited_state) for visited_state in visited):
            continue
        
        # Mark the current state as visited
        visited.append(current_state)

        ################# If game End #############################
        if current_state.status == False:
            # Build path from the current state to the initial state
            path.append(current_state)
            while current_state.previous is not None:
                current_state = current_state.previous
                path.append(current_state)
            path.reverse()
            return path

        ################## If game not End #########################
        current_state.next_states_create()

        for direction, state in current_state.next_states.items():
            if not any(state.check(visited_state) for visited_state in visited):
                pq.put((cost + 1, state))  


######################
#تابع الاساسي 
######################

import pygame
from GameGui import GameGUI
from Cell import Cell
from State import State
from Algorithm import Algorithm

def on_key_press(event, current_state):
    new_state = None

    if event.key == pygame.K_w:
        new_state = current_state.move_players_up()
        new_state.next_states_create()
        new_state.print_grid()
    elif event.key == pygame.K_a:
        new_state = current_state.move_players_left()
        new_state.next_states_create()
    elif event.key == pygame.K_s:
        new_state = current_state.move_players_down()
        new_state.next_states_create()
    elif event.key == pygame.K_d:
        new_state = current_state.move_players_right()
        new_state.next_states_create()
        new_state.print_grid()
    elif event.key == pygame.K_q:
        return None 

    return new_state

if __name__ == "__main__":

    ########################grids######################################

    grid1 = [
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None)],
        [Cell("wall", None, None), Cell("player", "red", None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("player", "blue", None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("target", "yellow", None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("player", "green", None), Cell("empty", None, None), Cell("target", "green", None), Cell("wall", None, None), Cell("target", "red", None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("player", "yellow", None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("target", "blue", None), Cell("wall", None, None)],
        [Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
    ]

    grid2 = [
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("player", "green", None), Cell("wall", None, None)],
        [Cell("wall", None, None),Cell("target", "green", None),Cell("wall", None, None),Cell("empty", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
    ]

    grid3 = [
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("player", "red", None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("target", "blue", None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("target", "red", None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("player", "blue", None), Cell("empty", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
        [Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None), Cell("wall", None, None)],
    ]
    
    #################################user_play###############################################
    
    # pygame.init()

    # status = True
    # initial_state = State(grid1, status,None) 
    # initial_state.next_states_create()

    # game_gui = GameGUI()

    # current_state = initial_state
    # game_gui.update_grid(current_state)

    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.KEYDOWN:
    #             new_state = on_key_press(event, current_state)
    #             if new_state is None:
    #                 running = False
    #             elif new_state != current_state:
    #                 current_state = new_state 
    #                 game_gui.update_grid(current_state) 

    #     if not current_state.win():
    #         font = pygame.font.SysFont(None, 48)
    #         text_surface = font.render("You win!", True, (0, 128, 0))
    #         game_gui.screen.blit(text_surface, (game_gui.width // 2 - text_surface.get_width() // 2, game_gui.height // 2 - text_surface.get_height() // 2))
    #         pygame.display.flip()
    #         pygame.time.wait(2000)
    #         break

    #     game_gui.clock.tick(60)

    # pygame.quit()
    
    ####################################Algorthim_play#########################################

    status = True
    initial_state = State(grid2, status, None,0) 
    algorithm = Algorithm(initial_state)

    bfs_soluation = algorithm.BFS()
    dfs_soluation = algorithm.DFS()
    dfs_recursive_soluation = algorithm.DFS_recursive(initial_state)
    ucs_soluation = algorithm.UCS()


    print("BFS____SOLUATION")
    for state in bfs_soluation:
        state.print_grid()
        print("####################################################")

    print("DFS____SOLUATION")
    for state in dfs_soluation:
        state.print_grid()
        print("####################################################")

    print("DFS____RECURSIVE___SOLUATION")
    for state in dfs_recursive_soluation:
        state.print_grid()
        print("####################################################")

    print("UCS____SOLUATION")
    for state in ucs_soluation:
        state.print_grid()
        print("####################################################")
import queue
import heapq
from itertools import count
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
        while current_state.previous != None:
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
          while current_state.previous != None:
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


############################################################################################

  def ucs_solve(self):
    priority_queue = []
    counter = count()

    heapq.heappush(priority_queue, (0, next(counter), self.initial_state))
    visited = set()

    while priority_queue:
        cumulative_cost, _, current_state = heapq.heappop(priority_queue)

        if current_state.check_win():
            return current_state

        state_id = tuple(tuple(cell.type_of_cell for cell in row) for row in current_state.grid)
        if state_id in visited:
            continue
        visited.add(state_id)

        current_state.next_states_create()

        if current_state.next_states:
            for next_state in current_state.next_states.values():
                cost = cumulative_cost + next_state.get_cost()
                heapq.heappush(priority_queue, (cost, next(counter), next_state))

    return None
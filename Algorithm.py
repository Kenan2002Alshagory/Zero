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
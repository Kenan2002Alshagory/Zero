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

        # Add next states to the priority queue with their cumulative cost
        for direction, state in current_state.next_states.items():
            if not any(state.check(visited_state) for visited_state in visited):
                pq.put((cost + 1, state))  # Uniform cost of 1 for each step

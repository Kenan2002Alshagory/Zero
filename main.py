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

    

    # status = True
    # initial_state = State(grid2, status, None, 0)  # Initial priority is 0
    # algorithm = Algorithm(initial_state)

    # ucs_solution = algorithm.UCS()

    # # Print or process the solution
    # for state in ucs_solution:
    #     state.print_grid()
    #     print()

    status = True
    initial_state = State(grid2, status, None,0) 
    algorithm = Algorithm(initial_state)

    # bfs_soluation = algorithm.BFS()
    # dfs_soluation = algorithm.DFS()
    ucs_soluation = algorithm.UCS()

    # print("BFS____SOLUATION")
    # for state in bfs_soluation:
    #     state.print_grid()
    #     print("####################################################")

    # print("DFS____SOLUATION")
    # for state in dfs_soluation:
    #     state.print_grid()
    #     print("####################################################")

    print("UCS____SOLUATION")
    for state in ucs_soluation:
        state.print_grid()
        print("####################################################")
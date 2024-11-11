import pygame

class GameGUI:
    def __init__(self, width=1000, height=1000):
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

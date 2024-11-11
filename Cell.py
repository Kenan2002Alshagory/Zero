class Cell:
    def __init__(self, cell_type, color, color2):
        self.cell_type = cell_type
        self.color = color
        self.color2 = color2

    def change_color(self, new_color):
        self.color = new_color

    def change_type(self, new_cell_type):
        self.cell_type = new_cell_type
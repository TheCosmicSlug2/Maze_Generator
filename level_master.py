from settings import *
from random import randint


class LevelMaster:
    def __init__(self, grid_dims) -> None:
        # 0 : vide / 1 : mur
        self.grid_dims = grid_dims
        self.map_data = [[1 for column in range(self.grid_dims[0])] for row in range(self.grid_dims[1])]
        self.cell_dims = (SCREEN_DIMS[0] // self.grid_dims[0], SCREEN_DIMS[1] // self.grid_dims[1])

        self.starting_grid_pos = (randint(0, self.grid_dims[0] - 1), randint(0, self.grid_dims[1] - 1))

        self.nb_cells = self.grid_dims[0] * self.grid_dims[1]

        self.ending_grid_pos = (None, None)
    
    def update_end(self, pos):
        self.ending_grid_pos = pos
    
    def update_maze_data(self, data):
        self.map_data = data
    
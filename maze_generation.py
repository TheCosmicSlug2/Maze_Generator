from random import choice
from renderer import Renderer
from level_master import LevelMaster
from settings import *

class DepthFirst:
    def __init__(self, level_master: LevelMaster, renderer: Renderer) -> None:

        self.level_master = level_master
        self.grid_dims = self.level_master.grid_dims
        self.starting_cell = self.level_master.starting_grid_pos
        self.map_data = self.level_master.map_data
        self.current_grid_pos = self.starting_cell

        self.renderer = renderer
        

        self.stack = [self.starting_cell]
        self.already_visited_cells = [self.starting_cell]
        self.convert_to_ground(self.starting_cell)

        self.current_distance = 0
        self.longest_distance = 0

        self.furthest_pos = None

        self.callback = 0
        self.nb_cells = self.level_master.nb_cells

        # Visualisation
        renderer.draw_rect_on_cache(self.renderer.cache_start, self.renderer.get_rect(self.starting_cell) , GREEN)
    
    def is_out_of_bounds(self, cell_grid_pos):
        x = cell_grid_pos[0]
        y = cell_grid_pos[1]
        return not (0 <= x < self.grid_dims[0] and 0 <= y < self.grid_dims[1])
    
    @staticmethod
    def find_middle_cell(first_cell, second_cell):
        middle_x = (first_cell[0] + second_cell[0]) // 2
        middle_y = (first_cell[1] + second_cell[1]) // 2
        return (middle_x, middle_y)
    
    def find_available_neighbours(self):
        neighbours = []

        possible_moves = [(0, -2), (-2, 0), (0, 2), (2, 0)]

        for move in possible_moves:
            neighbour_grid_pos = (self.current_grid_pos[0] + move[0], self.current_grid_pos[1] + move[1])
            if self.is_out_of_bounds(neighbour_grid_pos):
                continue
            if neighbour_grid_pos in self.already_visited_cells:
                continue
            if self.map_data[neighbour_grid_pos[1]][neighbour_grid_pos[0]] != 1:
                continue
            neighbours.append(neighbour_grid_pos)
        
        return neighbours
    
    def convert_to_ground(self, cell_pos):
        self.map_data[cell_pos[1]][cell_pos[0]] = 0
    
    def generate_maze(self):

        maze_generating = True
        while maze_generating:

            if not self.stack:
                maze_generating = False
                continue

            # Trouver les voisins disponibles
            neighbours = self.find_available_neighbours()

            # S'il n'y a pas de voisins, faire du backtracking
            if not neighbours and self.stack:
                self.current_grid_pos = self.stack.pop()
                self.current_distance -= 1

                # Visualisation
                self.renderer.cache_current_pos.fill((0, 0, 0, 0))
                self.renderer.draw_rect_on_cache(self.renderer.cache_current_pos, self.renderer.get_rect(self.current_grid_pos), RED)
                self.renderer.update()

                continue

            # Choisir un voisin au hasard et trouver la cellule intermédiaire
            new_cell_grid_pos = choice(neighbours)
            middle_cell = self.find_middle_cell(self.current_grid_pos, new_cell_grid_pos)

            # Transformer ces cellules en sol
            self.convert_to_ground(middle_cell)
            self.convert_to_ground(new_cell_grid_pos)

            # Ajouter la nouvelle cellule au stack et aux cellules déjà visitées
            self.stack.append(new_cell_grid_pos)
            self.already_visited_cells.append(new_cell_grid_pos)

            # La nouvelle cellule devient la cellule actuelle
            self.current_grid_pos = new_cell_grid_pos

            self.current_distance += 1

            if self.current_distance > self.longest_distance:
                self.longest_distance = self.current_distance
                self.furthest_pos = self.current_grid_pos

                # Visualisation
                self.renderer.cache_furthest_pos.fill((0, 0, 0, 0))
                self.renderer.draw_rect_on_cache(self.renderer.cache_furthest_pos, self.renderer.get_rect(self.current_grid_pos), BLUE)
            

            # Visualisation                
            self.renderer.add_maze_cell(middle_cell)
            self.renderer.add_maze_cell(self.current_grid_pos)
            self.renderer.cache_current_pos.fill((0, 0, 0, 0))
            self.renderer.draw_rect_on_cache(self.renderer.cache_current_pos, self.renderer.get_rect(self.current_grid_pos), RED)
            self.renderer.update()            


            if len(self.already_visited_cells) % self.grid_dims[0] == 0:

                avancement = round((len(self.already_visited_cells) / (self.nb_cells // 4)) * 100)
                print(f"Création... {avancement}%")
                self.renderer.rename_win(f"Depth-First {self.grid_dims} | Création... {avancement}%")
        
        self.renderer.cache_current_pos.fill((0, 0, 0, 0))

        self.renderer.render_grid(self.map_data)

        self.renderer.rename_win(f"Depth-First {self.grid_dims} | Création... Terminée")
        
        print("Création terminée")

        return self.map_data

import time
from settings import *
from copy import deepcopy
from settings import GRID_DIMS
from renderer import Renderer
from level_master import LevelMaster

class DeadEndFill:
    def __init__(self, level_master: LevelMaster, renderer: Renderer) -> None:
        self.original_map_data = level_master.map_data
        self.map_data = deepcopy(level_master.map_data)
        self.grid_dims = level_master.grid_dims
        self.renderer = renderer
        self.starting_grid_pos = level_master.starting_grid_pos
        self.ending_grid_pos = level_master.ending_grid_pos
        self.has_removed_cells = True
        self.exit_dst = 0
    
    def is_wall(self, grid_pos):
        x, y = grid_pos
        return self.map_data[y][x] == 1

    def is_out_of_bounds(self, grid_pos):
        x, y = grid_pos
        return not (0 <= x < self.grid_dims[0] and 0 <= y < self.grid_dims[1])

    def find_available_neighbours(self, cell_grid_pos):
        """Retourne le nombre de cellules voisines disponibles (valeur 0 = passage)."""
        neighbours = []
        possible_moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Haut, Gauche, Bas, Droite

        for move in possible_moves:
            neighbour_grid_pos = (cell_grid_pos[0] + move[0], cell_grid_pos[1] + move[1])

            if self.is_out_of_bounds(neighbour_grid_pos):
                continue  # On ignore les cellules en dehors des limites

            if self.is_wall(neighbour_grid_pos):  # Passage libre
                continue
            
            neighbours.append(neighbour_grid_pos)
        
        return neighbours

    def remove_dead_ends(self):
        """Supprime les impasses du labyrinthe en transformant les cellules à une seule connexion en mur."""
        self.liste_dead_ends = []
        self.has_removed_cells = False  # Réinitialiser le nombre de cellules supprimées
        dead_ends_removed = 0

        for row_idx, row in enumerate(self.map_data):
            for column_idx, column in enumerate(row):
                current_cell = (column_idx, row_idx)

                # Ignorer les cellules de départ et d'arrivée
                if current_cell == self.starting_grid_pos or current_cell == self.ending_grid_pos:
                    continue

                # Si ce n'est pas un passage
                if column != 0:
                    continue

                nb_neighbours = len(self.find_available_neighbours(current_cell))

                # Si la cellule est une impasse (un seul voisin libre)
                if nb_neighbours != 1:
                    continue

                self.map_data[row_idx][column_idx] = 1  # Transformer en mur
                self.liste_dead_ends.append(current_cell)
                dead_ends_removed += 1
                self.has_removed_cells = True
        
        if dead_ends_removed > 1:
            self.renderer.rename_win(f"Dead-End Fill | Solving... (removed {dead_ends_removed} dead ends)")
            print(f"removed {dead_ends_removed} dead ends")
    
    def solve_maze(self):
        """Résout le labyrinthe en supprimant toutes les impasses, puis rend le résultat."""

        self.renderer.rename_win(f"Dead-End Fill | Solving...")

        while self.has_removed_cells:
            self.remove_dead_ends()  # Suppression des impasses à chaque itération
            
            # Visualisation
            self.renderer.remove_cells(self.liste_dead_ends)
            self.renderer.update()

        # Visualisation
        self.renderer.render_grid(self.original_map_data)
        self.renderer.update()

        self.renderer.rename_win("Finding correct path...")

        current_pos = self.starting_grid_pos
        self.exit_path = [self.starting_grid_pos]
        while current_pos != self.ending_grid_pos:
            current_neighbours = self.find_available_neighbours(current_pos)

            # Enlever les chemins déjà présents

            new_neighbour = [neighbour for neighbour in current_neighbours if neighbour not in self.exit_path]

            self.exit_path.extend(new_neighbour)
            current_pos = self.exit_path[-1]

            self.exit_dst += 1

            # Visualisation
            self.renderer.draw_cell_rect(current_pos, RED)
            self.renderer.update()
        
        self.renderer.rename_win(f"Correct path found : {self.exit_dst} units")
            

        self.renderer.render_grid(self.original_map_data)
        self.renderer.render_path(self.exit_path)
        self.renderer.update()        
        



class WallFollower:
    def __init__(self, side, level_master: LevelMaster, renderer: Renderer) -> None:
        self.side = side
        self.level_master = level_master
        self.map_data = level_master.map_data
        self.starting_grid_pos = level_master.starting_grid_pos
        self.ending_grid_pos = level_master.ending_grid_pos
        self.renderer = renderer

        self.current_pos = self.starting_grid_pos

        self.grid_dims = level_master.grid_dims

        self.exit_path = []
        self.side = side
        self.exit_dst = 0

        self.heading = 0        
        # N E S W - just a helpful reminder
        # 0 1 2 3

        self.turn = {"right": -1, "left": 1}[side]

        self.count = 1 # Turning left, -1 for right

        self.completed = False

    def is_wall(self, pos):
        x, y = pos
        return self.map_data[y][x] == 1
    
    def is_out_of_bounds(self, pos):
        x, y = pos
        return not (0 <= y < self.grid_dims[0] and 0 <= x < self.grid_dims[1])
    
    def find_neighbours(self):

        neighbourgs = []
        # Haut 
        for vector in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nei_cell = (
                self.current_pos[0] + vector[0],
                self.current_pos[1] + vector[1]
            )
            
            if self.is_out_of_bounds(nei_cell) or self.is_wall(nei_cell):
                neighbourgs.append(None)
            else:
                neighbourgs.append(nei_cell)
        
        return neighbourgs

    def solve_maze(self):

        self.renderer.rename_win(f"WallFollower {self.side} | Solving... ")

        while self.current_pos != self.ending_grid_pos:
            self.exit_path.append(self.current_pos)

            self.renderer.render_path(self.exit_path)
            self.renderer.update()

            self.exit_dst += 1

            n = self.find_neighbours()

            # A gauche 
            if n[(self.heading - self.turn) % 4] != None:
                self.heading = (self.heading - self.turn) % 4
                self.current_pos = n[self.heading]
                continue

            # Tour droit
            if n[self.heading] != None:
                self.current_pos = n[self.heading]
                continue

            # A droite
            if n[(self.heading + self.turn) % 4] != None:
                self.heading = (self.heading + self.turn) % 4
                self.current_pos = n[self.heading]
                continue

            # Aller en arrière
            if n[(self.heading + 2) % 4] != None:
                self.heading = (self.heading + 2) % 4
                self.current_pos = n[self.heading]
                continue
    
        self.renderer.rename_win(f"WallFollower {self.side} | Solving... Terminé")


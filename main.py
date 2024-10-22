from renderer import Renderer
from level_master import LevelMaster
from settings import *
import pygame as pg
from maze_generation import DepthFirst
from maze_solving import DeadEndFill, WallFollower

# Ok dcp la durée entre 2 avancements est proportionnelle à l'avancement

pg.init()

level_master = LevelMaster(GRID_DIMS)
renderer = Renderer(level_master=level_master)

depth_first = DepthFirst(
    level_master=level_master,
    renderer=renderer
)

depth_first.generate_maze()

level_master.update_maze_data(depth_first.map_data)
level_master.update_end(depth_first.furthest_pos)

maze_solver = DeadEndFill(
    #side="right",
    renderer=renderer,
    level_master=level_master
)

maze_solver.solve_maze()
 
"""
maze_solver = DeadEndFill(
    level_master=level_master,
    renderer=renderer
)

maze_solver.solve_maze()
"""

print("")
print(f"Point de départ : {level_master.starting_grid_pos}")
print(f"Point d'arrivée : {depth_first.furthest_pos}")
print(f"Distance totale : {maze_solver.exit_dst} cellules")

renderer.dummy_loop()

pg.quit()
import pygame as pg
from settings import *

class Renderer:
    def __init__(self, level_master) -> None:
        self.level_master = level_master
        self.cell_dims = level_master.cell_dims
        self.SCREEN = pg.display.set_mode(SCREEN_DIMS)
        pg.display.set_caption("Maze Generator")
        self.clock = pg.time.Clock()
        self.map = pg.Surface(SCREEN_DIMS)
        self.cache_start = pg.Surface(SCREEN_DIMS, pg.SRCALPHA)
        self.cache_current_pos = pg.Surface(SCREEN_DIMS, pg.SRCALPHA)
        self.cache_furthest_pos = pg.Surface(SCREEN_DIMS, pg.SRCALPHA)

    def rename_win(self, title):
        pg.display.set_caption(title)
        self.get_events() # Pour pas que la fenêtre crashe



    def get_rect(self, cell_pos):
        return pg.Rect(cell_pos[0] * self.cell_dims[0], cell_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])


    def render_grid(self, grid_data):
        self.map.fill(BLACK)
        for row_idx, row in enumerate(grid_data):
            for column_idx, column in enumerate(row):
                if column == 1: # Si c'est un mur
                    continue

                rect = pg.Rect(column_idx * self.cell_dims[0], row_idx * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
                pg.draw.rect(self.map, WHITE, rect)
        
    
    def render_points(self, starting_grid_pos, ending_grid_pos, current_cell_grid_pos, current_cell_color):
        rect_start = pg.Rect(starting_grid_pos[0] * self.cell_dims[0], starting_grid_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
        rect_end = pg.Rect(ending_grid_pos[0] * self.cell_dims[0], ending_grid_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
        if current_cell_grid_pos:
            rect_current = pg.Rect(current_cell_grid_pos[0] * self.cell_dims[0], current_cell_grid_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
        
        pg.draw.rect(self.map, BLUE, rect_end)
        if current_cell_grid_pos:
            pg.draw.rect(self.map, current_cell_color, rect_current)
        pg.draw.rect(self.map, GREEN, rect_start)

    def render_path(self, path):
        for cell_grid_pos in path:
            x = cell_grid_pos[0]
            y = cell_grid_pos[1]
            rect = pg.Rect(x * self.cell_dims[0], y * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
            pg.draw.rect(self.map, RED, rect)
    
    def add_maze_cell(self, cell_pos):
        rect = pg.Rect(cell_pos[0] * self.cell_dims[0], cell_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
        pg.draw.rect(self.map, WHITE, rect)

    def draw_cell_rect(self, cell_pos, color):
        rect = pg.Rect(cell_pos[0] * self.cell_dims[0], cell_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
        pg.draw.rect(self.map, color, rect)
    
    def remove_cells(self, liste_cell_pos):
        for cell_pos in liste_cell_pos:
            rect = pg.Rect(cell_pos[0] * self.cell_dims[0], cell_pos[1] * self.cell_dims[1], self.cell_dims[0], self.cell_dims[1])
            pg.draw.rect(self.map, BLACK, rect)

    def draw_rect_on_cache(self, cache, rect, rect_color):
        pg.draw.rect(cache, rect_color, rect)
    
    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"


    def update(self):
        event = self.get_events()
        if event == "quit":
            pg.quit()
        self.SCREEN.blit(self.map, (0, 0))
        self.SCREEN.blit(self.cache_start, (0, 0))
        self.SCREEN.blit(self.cache_current_pos, (0, 0))
        self.SCREEN.blit(self.cache_furthest_pos, (0, 0))
        pg.display.flip()
        #self.clock.tick(FPS)
    

    def dummy_loop(self):
        running = True
        while running:
            event = self.get_events()
            if event == "quit":
                running = False
            pg.display.update()


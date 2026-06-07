import pygame
import random
import numpy as np
from config import TILES

class MapManager:
    TERRAIN_NONE = 0
    TERRAIN_SAND = 1
    TERRAIN_GRASS = 2
    TERRAIN_FOREST = 3
    TERRAIN_HILL = 4

    def __init__(self, image_path, target_size=(800, 800), chunk_size=50):
        raw_image = pygame.image.load(image_path)
        self.bg_image = pygame.transform.scale(raw_image, target_size)
        
        self.width = self.bg_image.get_width()
        self.height = self.bg_image.get_height()
        
        self.depleted_food = {}
        self.depleted_resources = {}
        self.chunk_size = chunk_size
        self.chunk_owners = {} # {(cx, cy): color}

        # 0: unwalkable, 1: walkable, 2: food (grass/forest)
        self.grid = np.zeros((self.width, self.height), dtype=np.uint8)
        self.terrain = np.zeros((self.width, self.height), dtype=np.uint8)
        self._initialize_grid()

    def _initialize_grid(self):
        non_walkable_colors = {
            TILES["deep_water"],
            TILES["shallow_water"],
            TILES["high_mountain"],
            TILES["peak_snow"],
            (0, 0, 0)
        }

        sand_color = TILES["sand"]
        grass_color = TILES["grass"]
        forest_color = TILES["forest"]
        hill_color = TILES["hill"]

        for x in range(self.width):
            for y in range(self.height):
                color = self.bg_image.get_at((x, y))
                r, g, b = color.r, color.g, color.b

                if (r, g, b) in non_walkable_colors:
                    self.grid[x, y] = 0
                    self.terrain[x, y] = MapManager.TERRAIN_NONE
                else:
                    self.grid[x, y] = 1
                    if (r, g, b) == sand_color:
                        self.terrain[x, y] = MapManager.TERRAIN_SAND
                    elif (r, g, b) == forest_color:
                        self.terrain[x, y] = MapManager.TERRAIN_FOREST
                        self.grid[x, y] = 2
                    elif (r, g, b) == grass_color:
                        self.terrain[x, y] = MapManager.TERRAIN_GRASS
                        self.grid[x, y] = 2
                    elif (r, g, b) == hill_color:
                        self.terrain[x, y] = MapManager.TERRAIN_HILL
                    elif g > r and g > b:
                        self.terrain[x, y] = MapManager.TERRAIN_GRASS
                        self.grid[x, y] = 2
                    else:
                        self.terrain[x, y] = MapManager.TERRAIN_SAND

    def get_chunk(self, x, y):
        return x // self.chunk_size, y // self.chunk_size

    def get_chunk_owner(self, cx, cy):
        return self.chunk_owners.get((cx, cy), None)

    def get_tile_type(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return MapManager.TERRAIN_NONE
        return self.terrain[x, y]

    def can_gather_resource(self, x, y):
        terrain_type = self.get_tile_type(x, y)
        if terrain_type in {
            MapManager.TERRAIN_SAND,
            MapManager.TERRAIN_GRASS,
            MapManager.TERRAIN_FOREST,
            MapManager.TERRAIN_HILL
        }:
            return (x, y) not in self.depleted_resources
        return False

    def gather_resource(self, x, y):
        terrain_type = self.get_tile_type(x, y)
        if (x, y) in self.depleted_resources:
            return None

        if terrain_type == MapManager.TERRAIN_SAND:
            if random.random() < 0.01:
                self.depleted_resources[(x, y)] = 120
                return "gold"
        elif terrain_type == MapManager.TERRAIN_GRASS:
            if random.random() < 0.05:
                self.depleted_resources[(x, y)] = 100
                return "wood"
        elif terrain_type == MapManager.TERRAIN_FOREST:
            if random.random() < 0.10:
                self.depleted_resources[(x, y)] = 100
                return "wood"
        elif terrain_type == MapManager.TERRAIN_HILL:
            if random.random() < 0.10:
                self.depleted_resources[(x, y)] = 150
                return "stone"
        return None

    def update_resources(self):
        self.update_food()
        to_remove = []
        for pos in list(self.depleted_resources):
            self.depleted_resources[pos] -= 1
            if self.depleted_resources[pos] <= 0:
                to_remove.append(pos)

        for pos in to_remove:
            del self.depleted_resources[pos]

    def set_chunk_owner(self, cx, cy, color):
        if color is None:
            self.chunk_owners.pop((cx, cy), None)
        else:
            self.chunk_owners[(cx, cy)] = color
    
    def is_walkable(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        return self.grid[x, y] != 0

    def has_food(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        if self.grid[x, y] == 2:
            if (x, y) not in self.depleted_food:
                return True
        return False

    def consume_food(self, x, y):
        self.depleted_food[(x, y)] = 150

    def update_food(self):
        to_remove = []
        for pos in list(self.depleted_food):  # list() ile sarmalandı
            self.depleted_food[pos] -= 1
            if self.depleted_food[pos] <= 0:
                to_remove.append(pos)
                
        for pos in to_remove:
            del self.depleted_food[pos]

    def get_random_walkable_pos(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[x, y] != 0:
                return x, y
            
    def get_walkable_pos_near(self, center_x, center_y, radius=30):
        for _ in range(100):
            x = center_x + random.randint(-radius, radius)
            y = center_y + random.randint(-radius, radius)
            if self.is_walkable(x, y):
                return x, y
        
        return self.get_random_walkable_pos()
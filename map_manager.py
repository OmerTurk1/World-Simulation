import pygame
import random
import numpy as np

class MapManager:
    def __init__(self, image_path, target_size=(800, 800), chunk_size=50):
        raw_image = pygame.image.load(image_path)
        self.bg_image = pygame.transform.scale(raw_image, target_size)
        
        self.width = self.bg_image.get_width()
        self.height = self.bg_image.get_height()
        
        self.depleted_food = {}
        self.chunk_size = chunk_size
        self.chunk_owners = {} # {(cx, cy): color}

        # 0: unwalkable (Sea, Peak Snow vb.), 1: Walkable, 2: Food (Forest/Grass)
        self.grid = np.zeros((self.width, self.height), dtype=np.uint8)
        self._initialize_grid()

    def _initialize_grid(self):
        non_walkable_colors = {
            (0, 0, 139),       # Deep Blue (Sea)
            (65, 105, 225),    # Sky Blue (Shallow Water)
            (105, 105, 105),   # Dark Gray (High Mountain)
            (255, 255, 255)    # White (Peak Snow)
        }

        for x in range(self.width):
            for y in range(self.height):
                color = self.bg_image.get_at((x, y))
                r, g, b = color.r, color.g, color.b

                if (r, g, b) in non_walkable_colors:
                    self.grid[x, y] = 0  # non-walkable area
                else:
                    if g > r and g > b:
                        self.grid[x, y] = 2  # foody
                    else:
                        self.grid[x, y] = 1  # walkable

    def get_chunk(self, x, y):
        return x // self.chunk_size, y // self.chunk_size

    def get_chunk_owner(self, cx, cy):
        return self.chunk_owners.get((cx, cy), None)

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
        for pos in self.depleted_food:
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
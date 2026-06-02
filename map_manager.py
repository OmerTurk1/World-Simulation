import pygame
import random

class MapManager:
    def __init__(self, image_path, target_size=(800, 800)):
        # Haritayı yükle ve anında hedef boyuta ölçekle
        raw_image = pygame.image.load(image_path)
        self.bg_image = pygame.transform.scale(raw_image, target_size)
        
        # Artık width ve height 800 olacak
        self.width = self.bg_image.get_width()
        self.height = self.bg_image.get_height()
        
        self.depleted_food = {} 

    def is_walkable(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
            
        color = self.bg_image.get_at((x, y))
        r, g, b = color.r, color.g, color.b
        
        # Deniz kontrolü (Mavi tonlar)
        if b > r and b > g: 
            return False
            
        # Dağ ve Karlı Zirve kontrolü (Gri/Beyaz tonlar)
        if abs(r - g) < 20 and abs(g - b) < 20 and r > 100: 
            return False
            
        return True

    def has_food(self, x, y):
        color = self.bg_image.get_at((x, y))
        r, g, b = color.r, color.g, color.b
        
        if g > r and g > b:
            if (x, y) not in self.depleted_food:
                return True
        return False

    def consume_food(self, x, y):
        self.depleted_food[(x, y)] = 300 

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
            if self.is_walkable(x, y):
                return x, y
            
    def get_walkable_pos_near(self, center_x, center_y, radius=30):
        for _ in range(100):
            x = center_x + random.randint(-radius, radius)
            y = center_y + random.randint(-radius, radius)
            if self.is_walkable(x, y):
                return x, y
        
        return self.get_random_walkable_pos()
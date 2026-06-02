import pygame
import random

class Agent:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.energy = 100 
        self.age = 0
        self.max_age = random.randint(1000, 2000) 
        self.alive = True
        self.color = color

    def update(self, map_manager, new_agents_list):
        if not self.alive:
            return

        self.age += 1
        self.energy -= 1

        if self.age > self.max_age or self.energy <= 0:
            self.alive = False
            return

        # Hareket sistemi organikleştirildi
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        new_x, new_y = self.x + dx, self.y + dy

        if map_manager.is_walkable(new_x, new_y):
            self.x, self.y = new_x, new_y

        if map_manager.has_food(self.x, self.y):
            self.energy += 15 
            map_manager.consume_food(self.x, self.y) 
            if self.energy > 200:
                self.energy = 200 

        if self.energy > 160:
            self.energy -= 100
            # Yeni doğan bebek hafifçe farklı bir pikselde doğsun ki üst üste binmesinler
            spawn_x = self.x + random.choice([-1, 1])
            spawn_y = self.y + random.choice([-1, 1])
            
            if map_manager.is_walkable(spawn_x, spawn_y):
                new_agents_list.append(Agent(spawn_x, spawn_y, self.color))
            else:
                new_agents_list.append(Agent(self.x, self.y, self.color))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 2)
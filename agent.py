import pygame
import random

class Agent:
    move_range = 2

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.energy = 100
        self.age = 0
        self.max_age = random.normalvariate(300, 400) 
        self.alive = True
        self.color = color
        self.reproduce_cooldown = 0

    def update(self, map_manager, new_agents_list):
        if not self.alive:
            return

        self.age += 1
        self.energy -= 1
        self.reproduce_cooldown = max(0, self.reproduce_cooldown - 1)

        if self.age > self.max_age or self.energy <= 0:
            self.alive = False
            return

        dx = random.randint(-Agent.move_range, Agent.move_range)
        dy = random.randint(-Agent.move_range, Agent.move_range)
        new_x, new_y = self.x + dx, self.y + dy

        if map_manager.is_walkable(new_x, new_y):
            self.x, self.y = new_x, new_y

        if map_manager.has_food(self.x, self.y):
            self.energy += 10
            map_manager.consume_food(self.x, self.y) 
            if self.energy > 200:
                self.energy = 200 

        if self.energy > 160 and self.reproduce_cooldown <= 0: # reproduction
            self.energy -= 120
            self.reproduce_cooldown = 10  # Set cooldown period

            spawn_x = self.x + random.choice([-1, 1])
            spawn_y = self.y + random.choice([-1, 1])
            
            if map_manager.is_walkable(spawn_x, spawn_y):
                new_agents_list.append(Agent(spawn_x, spawn_y, self.color))
            else:
                new_agents_list.append(Agent(self.x, self.y, self.color))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 2)
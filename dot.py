import pygame
import random
import math

class Dot:
    def __init__(self, window, lock_width, lock_radius):
        self.window = window
        # Randomly place the dot on the lock
        randNum = random.randint(0, 360)
        self.x = int(window.get_width() / 2 + math.cos(math.radians(randNum)) * (lock_radius - (lock_width / 2)))
        self.y = int(window.get_height() / 2 + math.sin(math.radians(randNum)) * (lock_radius - (lock_width / 2)))
        self.color = (255, 255, 0) # yellow
        self.radius = lock_width // 2


    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
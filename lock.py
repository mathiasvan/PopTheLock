import pygame

class Lock:
    def __init__(self, window, color, lock_width):
        self.window = window
        self.x = window.get_width() // 2
        self.y = window.get_height() // 2
        self.radius = window.get_width() // 4
        self.color = color
        self.lock_width = lock_width

    def draw(self):
        # Circle with a hole in the middle
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.window, (255, 255, 255), (self.x, self.y), self.radius - self.lock_width)
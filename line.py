import pygame
import math


class Line:
    def __init__(self, window, color, width, height):
        """Initializes the line object.

        Args:
            window (pygame.window): Pygame window
            color (Tuple(3)): The color of the line
            width (Int): Width of the rect
            height (Int): Height of the rect
        """
        self.window = window
        x = window.get_width() // 2 - width // 2
        y = window.get_height() // 2 - window.get_height() // 4
        self.rect = [[x, y], [x + width, y], [x + width, y + height], [x, y + height]]
        self.color = color
        self.rotation_angle = 90  # degrees, anti-clockwise, 0 is right
        self.speed = 2  # degrees per frame
        self.direction = 1  # 1 right, -1 left
        self.hitting_dot = False  # True if the line is hitting the dot, used for game over if line passes over the dot without user input
        self.prev_hitting_dot = False  # True if the line was hitting the dot in the previous frame, used for game over if line passes over the dot without user input

    def draw(self):
        # Draw the rectangle in line with the rotation
        pygame.draw.polygon(self.window, self.color, self.rect)

    def rotate(self, angle):
        """Rotates the rectangle by angle degrees around the center of the window.

        Args:
            angle (Int): Angle to turn by in degrees. Anti-clockwise.
        """
        # Get the center of the window
        center = (self.window.get_width() // 2, self.window.get_height() // 2)
        # Create a new rectangle
        new_rect = []
        for point in self.rect:
            # Translate the point to the origin
            x = point[0] - center[0]
            y = point[1] - center[1]
            # Rotate the point
            x1 = x * math.cos(angle * math.pi / 180) - y * math.sin(
                angle * math.pi / 180
            )
            y1 = x * math.sin(angle * math.pi / 180) + y * math.cos(
                angle * math.pi / 180
            )
            # Translate the point back
            x1 += center[0]
            y1 += center[1]
            # Add the point to the new rectangle
            new_rect.append([x1, y1])
        return new_rect

    def move(self):
        # Rotate the rectangle
        delta_angle = self.speed * self.direction
        self.rotation_angle += delta_angle
        self.rotation_angle %= 360
        self.rect = self.rotate(delta_angle)

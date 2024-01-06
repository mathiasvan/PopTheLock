import pygame
import numpy as np
from lock import Lock
from line import Line
from dot import Dot

pygame.init()

# Creating a window
WINDOW = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pop the lock")

# CLock
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game variables
score = 0
score_font = pygame.font.SysFont("Arial", 30)
CREATE_DOT_EVENT = pygame.USEREVENT + 1
relocating_dot = False

# Lock
LOCKWIDTH = 50
lock = Lock(WINDOW, BLACK, LOCKWIDTH)
line = Line(WINDOW, RED, 15, LOCKWIDTH)
dot = Dot(WINDOW, LOCKWIDTH, lock.radius)


# Utility functions
# Intersect (using fancy pantsy math from https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection)
# Thank you ShreevatsaR and PhindAI for the code
def pointInRectangle(P, rectangle):
    A, B, C, D = rectangle
    AP = np.subtract(P, A)
    AB = np.subtract(B, A)
    AD = np.subtract(D, A)
    return 0 <= np.dot(AP, AB) <= np.dot(AB, AB) and 0 <= np.dot(AP, AD) <= np.dot(
        AD, AD
    )


def intersectCircle(circle, line):
    P, R = circle
    A, B = line
    d = np.subtract(B, A)
    f = np.subtract(A, P)
    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - R**2
    discriminant = b**2 - 4 * a * c
    if discriminant >= 0:
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)
        if 0 <= t1 <= 1 or 0 <= t2 <= 1:
            return True
    return False


def intersect(circle, rectangle):
    P, R = circle
    A, B, C, D = rectangle
    return (
        pointInRectangle(P, rectangle)
        or intersectCircle(circle, (A, B))
        or intersectCircle(circle, (B, C))
        or intersectCircle(circle, (C, D))
        or intersectCircle(circle, (D, A))
    )


# Game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):
            if not game_over:
                line.direction = -line.direction
                if intersect([(dot.x, dot.y), dot.radius], line.rect):
                    pygame.time.set_timer(CREATE_DOT_EVENT, 300, 1)
                    relocating_dot = True
                    score += 1
                    line.prev_hitting_dot = False
                    line.hitting_dot = False
                    line.speed += 0.05 # Increase the speed of the line
                else:
                    game_over = True
            else:
                # Reset the game
                game_over = False
                score = 0
                line = Line(WINDOW, RED, 20, LOCKWIDTH)
                dot = Dot(WINDOW, LOCKWIDTH, lock.radius)
        if event.type == CREATE_DOT_EVENT:
            dot = Dot(WINDOW, LOCKWIDTH, lock.radius)
            while intersect([(dot.x, dot.y), dot.radius], line.rect): # Make sure the dot doesn't spawn on the line
                dot = Dot(WINDOW, LOCKWIDTH, lock.radius)
            relocating_dot = False

    if not game_over:
        # Update
        line.move()

        if not relocating_dot:
            line.prev_hitting_dot = line.hitting_dot
            if intersect([(dot.x, dot.y), dot.radius], line.rect):
                line.hitting_dot = True
            else:
                line.hitting_dot = False
            # Line has moved past the dot without user input
            if line.prev_hitting_dot and not line.hitting_dot:
                game_over = True

    # Draw
    WINDOW.fill(WHITE)
    score_text = score_font.render("Score: " + str(score), True, BLACK)
    WINDOW.blit(score_text, (10, 10))
    lock.draw()
    if not relocating_dot:
        dot.draw()
    line.draw()

    if game_over:
        game_over_text = score_font.render("Game Over", True, BLACK)
        WINDOW.blit(game_over_text, (WINDOW.get_width() // 2 - game_over_text.get_width() // 2, WINDOW.get_height() // 2 - game_over_text.get_height() // 2))

    pygame.display.update()
    clock.tick(60)
  
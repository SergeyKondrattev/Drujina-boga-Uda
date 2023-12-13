import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Solar System Simulation")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define classes for the planets
class Planet:
    def __init__(self, name, radius, distance, color, speed):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.color = color
        self.speed = speed
        self.angle = 0

    def move(self):
        self.angle += self.speed

    def draw(self):
        x = int(math.cos(self.angle) * self.distance) + size[0] // 2
        y = int(math.sin(self.angle) * self.distance) + size[1] // 2
        pygame.draw.circle(screen, self.color, (x, y), self.radius)

# Create instances of the planets
sun = Planet("Sun", 50, 0, YELLOW, 0)
mercury = Planet("Mercury", 10, 70, YELLOW, 0.03)
venus = Planet("Venus", 20, 110, BLUE, 0.02)
earth = Planet("Earth", 25, 150, BLUE, 0.01)
mars = Planet("Mars", 15, 200, RED, 0.008)

# Loop until the user clicks the close button.
done = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    sun.move()
    mercury.move()
    venus.move()
    earth.move()
    mars.move()

    # --- Drawing code should go here
    screen.fill(BLACK)

    sun.draw()
    mercury.draw()
    venus.draw()
    earth.draw()
    mars.draw()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()

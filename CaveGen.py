import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE  # Swap ROWS and COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cave Generator")

# Create a grid to represent the cave
grid = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Function to generate the cave using cellular automata
def generate_cave(grid, generations):
    for _ in range(generations):
        new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(1, ROWS - 1):
            for col in range(1, COLS - 1):
                neighbors = [
                    grid[row - 1][col - 1],
                    grid[row - 1][col],
                    grid[row - 1][col + 1],
                    grid[row][col - 1],
                    grid[row][col + 1],
                    grid[row + 1][col - 1],
                    grid[row + 1][col],
                    grid[row + 1][col + 1],
                ]
                wall_count = sum(neighbors)
                if wall_count >= 5:
                    new_grid[row][col] = 1
                elif wall_count <= 3:
                    new_grid[row][col] = 0
                else:
                    new_grid[row][col] = grid[row][col]
        grid = new_grid
    return grid

# Generate the cave
grid = generate_cave(grid, 5)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the grid on the screen
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(
                screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    pygame.display.flip()

pygame.quit()

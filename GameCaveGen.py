import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
SQUARE_SIZE = 15
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combined Game")

# Function to generate the cave using cellular automata
def generate_cave(generations):
    # Create the initial grid randomly
    grid = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]
    
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
    
    # Find valid spawn positions (white cells)
    spawn_positions = [(col * CELL_SIZE, row * CELL_SIZE) for row in range(ROWS) for col in range(COLS) if grid[row][col] == 1]
    
    return grid, spawn_positions

# Generate the cave and get valid spawn positions
cave_grid, spawn_positions = generate_cave(5)

# Initial square position in a random white cell
x, y = random.choice(spawn_positions)

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Calculate the next position based on key presses
    next_x, next_y = x, y
    if keys[pygame.K_w]:
        next_y -= 5
    if keys[pygame.K_s]:
        next_y += 5
    if keys[pygame.K_a]:
        next_x -= 5
    if keys[pygame.K_d]:
        next_x += 5
    
    # Check for collision with black cells
    cell_x, cell_y = next_x // CELL_SIZE, next_y // CELL_SIZE
    if 0 <= cell_x < COLS and 0 <= cell_y < ROWS and cave_grid[cell_y][cell_x] == 1:
        x, y = next_x, next_y

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid on the screen
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if cave_grid[row][col] == 1 else BLACK
            pygame.draw.rect(
                screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    # Draw the square
    pygame.draw.rect(screen, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()

    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()

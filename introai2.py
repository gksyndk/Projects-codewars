import pygame
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Agent
GREEN = (0, 255, 0)  # Resource (R)
RED = (255, 0, 0)  # Threat (T)

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Agent Prototype")

# Agent class
class Agent:
    def __init__(self, x, y, role):
        self.x = x  # Agent's X position
        self.y = y  # Agent's Y position
        self.role = role  # 'gatherer', 'defender', 'explorer'

    def move(self):
        """Move the agent randomly in one of four directions."""
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])  # Random direction
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:  # Stay within bounds
            self.x, self.y = new_x, new_y

    def perform_task(self, grid):
        """Perform tasks based on the agent's role."""
        if self.role == 'gatherer':  # Collect resources
            if grid[self.x][self.y] == 'R':  # Found a resource
                grid[self.x][self.y] = ''  # Collect the resource
                print(f"Gatherer collected a resource at ({self.x}, {self.y})!")

        elif self.role == 'defender':  # Neutralize threats
            if grid[self.x][self.y] == 'T':  # Found a threat
                grid[self.x][self.y] = ''  # Neutralize the threat
                print(f"Defender neutralized a threat at ({self.x}, {self.y})!")

        elif self.role == 'explorer':  # Explore new areas
            # Explorers do not interact but can help locate resources or threats.
            pass

# Create agents
agents = [
    Agent(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), 'gatherer'),
    Agent(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), 'defender'),
    Agent(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), 'explorer'),
]

# Create grid
grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place resources (R) and threats (T) randomly on the grid
for _ in range(30):  # Add 30 resources
    grid[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = 'R'
for _ in range(10):  # Add 10 threats
    grid[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = 'T'

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen

    # Draw the grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x][y] == 'R':  # Resource
                pygame.draw.rect(screen, GREEN, rect)
            elif grid[x][y] == 'T':  # Threat
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines

    # Update agents
    for agent in agents:
        agent.move()  # Move the agent
        agent.perform_task(grid)  # Perform their assigned task
        # Draw the agent
        pygame.draw.circle(
            screen,
            BLUE,
            (agent.x * CELL_SIZE + CELL_SIZE // 2, agent.y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3,
        )

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            running = False

    pygame.display.flip()  # Update the display
    pygame.time.delay(200)  # Slow down the loop for visibility

pygame.quit()

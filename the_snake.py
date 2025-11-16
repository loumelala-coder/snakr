from random import randint

import pygame

# Constants for field and grid sizes
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Speed
SPEED = 10

# Game window setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Initialize game object with position and color."""
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.body_color = body_color

    def draw(self):
        """Draw the game object. To be implemented in child classes."""
        pass

    def draw_cell(self, position, color):
        """Draw a single cell at given position with given color."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple class for the snake to eat."""

    def __init__(self):
        """Initialize apple with random position."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Set apple to random position on grid."""
        self.position = [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        ]

    def draw(self):
        """Draw the apple on the screen."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Snake class representing the player character."""

    def __init__(self):
        """Initialize snake with starting position and direction."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Reset snake to initial state."""
        self.positions = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.grew = False

    def update_direction(self):
        """Update direction after key press."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Get current head position."""
        return self.positions[0]

    def move(self):
        """Move the snake one step in current direction."""
        head = self.get_head_position()
        new_x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = [new_x, new_y]

        self.positions.insert(0, new_head)

        if not self.grew:
            self.last = self.positions.pop()
        else:
            self.grew = False

    def grow(self):
        """Make the snake grow on next move."""
        self.grew = True

    def draw(self):
        """Draw the snake on the screen."""
        # Draw body segments
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Draw head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase last segment if snake moved without growing
        if self.last and not self.grew:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def check_collision(self):
        """Check if snake collides with itself."""
        return self.get_head_position() in self.positions[1:]


def handle_keys(game_object):
    """Handle user input for controlling the snake."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main game function."""
    pygame.init()

    # Create game objects
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Handle user input
        handle_keys(snake)

        # Update snake direction
        snake.update_direction()

        # Move snake
        snake.move()

        # Check for apple collision
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            # Ensure apple doesn't appear on snake
            while apple.position in snake.positions:
                apple.randomize_position()

        # Check for self-collision
        if snake.check_collision():
            snake.reset()
            apple.randomize_position()

        # Draw everything
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

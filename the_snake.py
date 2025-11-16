from random import randint
from typing import List, Tuple

import pygame as pg

# Type aliases
Pointer = Tuple[int, int]
Color = Tuple[int, int, int]
Position = Tuple[int, int]

# Constants for field and grid sizes
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Movement directions
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Colors
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)

# Speed
SPEED: int = 10

# Game window setup
screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Snake')
clock: pg.time.Clock = pg.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, body_color: Color = BOARD_BACKGROUND_COLOR) -> None:
        """Initialize game object with position and color."""
        self.position: Position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: Color = body_color

    def draw(self) -> None:
        """Draw the game object. To be implemented in child classes."""
        raise NotImplementedError(
            'Method must be implemented in child class'
        )

    def draw_cell(self, position: Position, color: Color) -> None:
        """Draw a single cell at given position with given color."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple class for the snake to eat."""

    def __init__(self, occupied_positions: List[Position] = None) -> None:
        """Initialize apple with random position."""
        super().__init__(APPLE_COLOR)
        self.occupied_positions: List[Position] = occupied_positions or []
        self.randomize_position()

    def randomize_position(
        self, occupied_positions: List[Position] = None
    ) -> None:
        """Set apple to random position on grid."""
        if occupied_positions is not None:
            self.occupied_positions = occupied_positions

        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in self.occupied_positions:
                break

    def draw(self) -> None:
        """Draw the apple on the screen."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Snake class representing the player character."""

    def __init__(self) -> None:
        """Initialize snake with starting position and direction."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self) -> None:
        """Reset snake to initial state."""
        self.positions: List[Position] = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ]
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer = None
        self.last: Position = None
        self.grew: bool = False

    def update_direction(self) -> None:
        """Update direction after key press."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Position:
        """Get current head position."""
        return self.positions[0]

    def move(self) -> None:
        """Move the snake one step in current direction."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        self.last = self.positions.pop() if not self.grew else None
        self.grew = False if self.grew else self.grew

    def grow(self) -> None:
        """Make the snake grow on next move."""
        self.grew = True

    def draw(self) -> None:
        """Draw the snake on the screen."""
        # Draw body segments
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Draw head
        head_position = self.get_head_position()
        head_rect = pg.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase last segment if snake moved without growing
        if self.last and not self.grew:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def check_collision(self) -> bool:
        """Check if snake collides with itself."""
        return self.get_head_position() in self.positions[1:]


def handle_keys(game_object: Snake) -> None:
    """Handle user input for controlling the snake."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Main game function."""
    pg.init()

    # Create game objects
    snake = Snake()
    apple = Apple(snake.positions)

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
            apple.randomize_position(snake.positions)

        # Check for self-collision
        if snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        # Draw everything
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

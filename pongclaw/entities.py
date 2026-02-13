"""Game entities: Paddle and Ball."""

from dataclasses import dataclass


@dataclass
class Paddle:
    """Represents a paddle in the game."""

    x: int
    y: int
    height: int
    width: int = 1

    def move_up(self, screen_height: int) -> None:
        """Move paddle up, respecting screen bounds."""
        self.y = max(0, self.y - 1)

    def move_down(self, screen_height: int) -> None:
        """Move paddle down, respecting screen bounds."""
        self.y = min(screen_height - self.height, self.y + 1)

    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point collides with this paddle."""
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


@dataclass
class Ball:
    """Represents the ball in the game."""

    x: float
    y: float
    dx: float
    dy: float

    def move(self) -> None:
        """Move the ball by its velocity."""
        self.x += self.dx
        self.y += self.dy

    def bounce_vertical(self) -> None:
        """Reverse vertical direction (wall bounce)."""
        self.dy = -self.dy

    def bounce_horizontal(self, paddle_y: int, paddle_height: int) -> None:
        """Reverse horizontal direction and adjust angle based on paddle hit.
        
        Args:
            paddle_y: Y position of the paddle that was hit.
            paddle_height: Height of the paddle.
        """
        self.dx = -self.dx
        # Adjust angle based on where ball hit paddle
        hit_pos = (self.y - paddle_y) / paddle_height  # 0.0 to 1.0
        self.dy = (hit_pos - 0.5) * 1.5  # -0.75 to 0.75

    def reset(self, x: float, y: float, dx: float, dy: float) -> None:
        """Reset ball to initial position and velocity."""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

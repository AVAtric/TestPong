"""Main Pong game class."""

import sys
import time
import tty
import termios
from typing import Tuple

from .game_state import GameState


class PongGame:
    """Terminal Pong game with player and AI controls."""

    def __init__(self, win_score: int = 7):
        """Initialize the Pong game.

        Args:
            win_score: Number of points needed to win the game.
        """
        self.win_score = win_score
        self.reset_game()

    def reset_game(self) -> None:
        """Reset the game state."""
        self.width = 80
        self.height = 24
        self.paddle_height = 6
        self.paddle_width = 2

        # Player paddle (left)
        self.player_y = (self.height - self.paddle_height) // 2
        self.player_dir = 0  # -1 for up, 1 for down, 0 for stationary

        # AI paddle (right)
        self.ai_y = (self.height - self.paddle_height) // 2
        self.ai_speed = 0.1  # Speed of AI paddle

        # Ball
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dir_x = 0.15  # Speed of ball
        self.ball_dir_y = 0.15

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Game state
        self.paused = False
        self.game_over = False
        self.winner = None

    def process_input(self, char: str) -> None:
        """Process user input.

        Args:
            char: Input character.
        """
        if self.game_over:
            if char == 'r' or char == 'R':
                self.reset_game()
            elif char == 'q' or char == 'Q':
                sys.exit(0)
            return

        if char == 'p' or char == 'P':
            self.paused = not self.paused
            return

        if self.paused:
            return

        # Player controls
        if char == 'w' or char == 'W' or char == '\x1b[A':  # W or Up arrow
            self.player_dir = -1
        elif char == 's' or char == 'S' or char == '\x1b[B':  # S or Down arrow
            self.player_dir = 1
        elif char == '\x1b[A' or char == '\x1b[B':  # Arrow keys
            self.player_dir = 0
        else:
            self.player_dir = 0

    def update(self) -> None:
        """Update game state."""
        if self.paused or self.game_over:
            return

        # Update player paddle
        new_player_y = self.player_y + self.player_dir
        if 0 <= new_player_y <= self.height - self.paddle_height:
            self.player_y = new_player_y

        # Update AI paddle (simple tracking)
        ball_center = self.ball_y
        paddle_center = self.ai_y + self.paddle_height // 2

        if ball_center < paddle_center - 2:
            self.ai_y -= self.ai_speed
        elif ball_center > paddle_center + 2:
            self.ai_y += self.ai_speed

        # Clamp AI paddle
        if self.ai_y < 0:
            self.ai_y = 0
        elif self.ai_y > self.height - self.paddle_height:
            self.ai_y = self.height - self.paddle_height

        # Update ball
        self.ball_x += self.ball_dir_x
        self.ball_y += self.ball_dir_y

        # Wall collisions (top/bottom)
        if self.ball_y <= 0 or self.ball_y >= self.height - 1:
            self.ball_dir_y *= -1
            self.ball_y = max(0, min(self.height - 1, self.ball_y))

        # Paddle collisions
        # Left wall (player)
        if self.ball_dir_x < 0:
            if self.ball_y >= self.player_y and self.ball_y <= self.player_y + self.paddle_height:
                # Check if ball is near the left edge
                if self.ball_x <= 2:
                    self.ball_dir_x *= -1
                    self.ball_dir_y *= 1.05  # Increase angle slightly
                    # Add some spin based on where it hit the paddle
                    hit_pos = (self.ball_y - self.player_y) / self.paddle_height
                    self.ball_dir_y = 0.15 * (hit_pos * 2 - 1)
            elif self.ball_x <= 0:
                # Score for AI
                self.ai_score += 1
                self.reset_ball()
                self.check_win()

        # Right wall (AI)
        if self.ball_dir_x > 0:
            if self.ball_y >= self.ai_y and self.ball_y <= self.ai_y + self.paddle_height:
                # Check if ball is near the right edge
                if self.ball_x >= self.width - 3:
                    self.ball_dir_x *= -1
                    self.ball_dir_y *= 1.05
                    hit_pos = (self.ball_y - self.ai_y) / self.paddle_height
                    self.ball_dir_y = 0.15 * (hit_pos * 2 - 1)
            elif self.ball_x >= self.width:
                # Score for player
                self.player_score += 1
                self.reset_ball()
                self.check_win()

        # Scoring
        if self.ball_x <= 0:
            self.ai_score += 1
            self.reset_ball()
            self.check_win()
        elif self.ball_x >= self.width:
            self.player_score += 1
            self.reset_ball()
            self.check_win()

    def reset_ball(self) -> None:
        """Reset ball to center with random direction."""
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dir_x = 0.15 * (1 if self.player_score > self.ai_score else -1)
        self.ball_dir_y = 0.15 * (1 if (self.ball_dir_y > 0) else -1)

    def check_win(self) -> None:
        """Check if game is won."""
        if self.player_score >= self.win_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.win_score:
            self.game_over = True
            self.winner = "AI"

    def get_state(self) -> GameState:
        """Get current game state.

        Returns:
            Current game state.
        """
        return GameState(
            player_y=self.player_y,
            ai_y=self.ai_y,
            ball_x=self.ball_x,
            ball_y=self.ball_y,
            player_score=self.player_score,
            ai_score=self.ai_score,
            paused=self.paused,
            game_over=self.game_over,
            winner=self.winner
        )

    def render(self) -> None:
        """Render the game to terminal."""
        # Save terminal settings
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            # Set terminal to raw mode
            tty.setraw(sys.stdin.fileno())

            # Clear screen and move cursor to top
            print("\033[2J\033[H", end="")

            # Draw top score line
            print(f"{'=' * (self.width // 2 - 2)}", end="")
            print(f"  {self.player_score} - {self.ai_score}  ", end="")
            print(f"{'=' * (self.width // 2 - 2)}")

            # Draw top border
            print("+" + "-" * (self.width - 2) + "+")

            # Draw game area
            for y in range(self.height - 2):  # Leave room for borders
                line = "|"

                # Left wall
                if y == self.ball_y:
                    if y == self.player_y or y == self.player_y + 1:
                        line += "||"  # Player paddle
                    elif y == self.ai_y or y == self.ai_y + 1:
                        line += "  "  # AI paddle
                    else:
                        line += " "  # Empty space
                else:
                    if y == self.player_y or y == self.player_y + 1:
                        line += "||"  # Player paddle
                    elif y == self.ai_y or y == self.ai_y + 1:
                        line += "  "  # AI paddle
                    else:
                        line += " "  # Empty space

                # Ball
                if y == self.ball_y:
                    if 1 < self.ball_x < self.width - 2:
                        line += "●"
                    else:
                        line += " "
                else:
                    if 1 < self.ball_x < self.width - 2:
                        line += " "
                    else:
                        line += "|"

                # Right wall
                line += "|"

                print(line)

            # Draw bottom border
            print("+" + "-" * (self.width - 2) + "+")

            # Draw bottom info line
            if self.paused:
                print("\033[33mPAUSED - Press P to continue\033[0m")
            elif self.game_over:
                if self.winner == "Player":
                    print(f"\033[32mVICTORY! Player wins!\033[0m")
                else:
                    print(f"\033[31mDEFEAT! AI wins!\033[0m")
                print("\033[36mPress R to restart, Q to quit\033[0m")

            print(f"\033[37mW/S or Arrow Keys: Move paddle | P: Pause | R: Restart | Q: Quit\033[0m")

        finally:
            # Restore terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_char() -> str:
    """Get a single character from input.

    Returns:
        Input character.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
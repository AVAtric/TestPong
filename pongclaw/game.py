"""Main game logic and rendering."""

import curses
import time
from typing import Tuple

from .entities import Ball, Paddle


class PongGame:
    """Terminal Pong game with player vs AI."""

    WINNING_SCORE = 7
    PADDLE_HEIGHT = 5
    INITIAL_BALL_SPEED = 0.5

    def __init__(self, stdscr):
        """Initialize game with curses screen."""
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Initialize paddles
        self.player = Paddle(
            x=2,
            y=self.height // 2 - self.PADDLE_HEIGHT // 2,
            height=self.PADDLE_HEIGHT,
        )
        self.ai = Paddle(
            x=self.width - 3,
            y=self.height // 2 - self.PADDLE_HEIGHT // 2,
            height=self.PADDLE_HEIGHT,
        )
        
        # Initialize ball
        self.ball = Ball(
            x=float(self.width // 2),
            y=float(self.height // 2),
            dx=self.INITIAL_BALL_SPEED,
            dy=0.3,
        )
        
        # Scores
        self.player_score = 0
        self.ai_score = 0
        
        # Game state
        self.paused = False
        self.game_over = False
        
        # Curses settings
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(16)  # ~60 FPS

    def reset_ball(self, direction: int = 1) -> None:
        """Reset ball to center with given direction.
        
        Args:
            direction: 1 for right, -1 for left.
        """
        self.ball.reset(
            x=float(self.width // 2),
            y=float(self.height // 2),
            dx=self.INITIAL_BALL_SPEED * direction,
            dy=0.3,
        )

    def update_ai(self) -> None:
        """Simple AI that tracks ball with slight delay."""
        paddle_center = self.ai.y + self.ai.height // 2
        ball_y = int(self.ball.y)
        
        # AI has 70% chance to move correctly (makes it beatable)
        import random
        if random.random() < 0.7:
            if ball_y < paddle_center - 1:
                self.ai.move_up(self.height)
            elif ball_y > paddle_center + 1:
                self.ai.move_down(self.height)

    def handle_input(self) -> bool:
        """Handle keyboard input. Returns False to quit.
        
        Returns:
            False if quit requested, True otherwise.
        """
        try:
            key = self.stdscr.getch()
        except:
            return True
        
        if key == ord('q') or key == ord('Q'):
            return False
        
        if self.game_over:
            if key == ord('r') or key == ord('R'):
                self.restart()
            return True
        
        if key == ord('p') or key == ord('P'):
            self.paused = not self.paused
            return True
        
        if self.paused:
            return True
        
        # Player controls
        if key in (ord('w'), ord('W'), curses.KEY_UP):
            self.player.move_up(self.height)
        elif key in (ord('s'), ord('S'), curses.KEY_DOWN):
            self.player.move_down(self.height)
        
        return True

    def update_physics(self) -> None:
        """Update ball position and handle collisions."""
        if self.paused or self.game_over:
            return
        
        self.ball.move()
        ball_x = int(self.ball.x)
        ball_y = int(self.ball.y)
        
        # Top/bottom wall bounce
        if ball_y <= 0 or ball_y >= self.height - 1:
            self.ball.bounce_vertical()
            self.ball.y = max(0, min(self.height - 1, self.ball.y))
        
        # Player paddle collision
        if self.player.contains_point(ball_x, ball_y) and self.ball.dx < 0:
            self.ball.bounce_horizontal(self.player.y, self.player.height)
            self.ball.x = self.player.x + self.player.width
        
        # AI paddle collision
        if self.ai.contains_point(ball_x, ball_y) and self.ball.dx > 0:
            self.ball.bounce_horizontal(self.ai.y, self.ai.height)
            self.ball.x = self.ai.x - 1
        
        # Scoring
        if ball_x <= 0:
            self.ai_score += 1
            self.reset_ball(direction=1)
            if self.ai_score >= self.WINNING_SCORE:
                self.game_over = True
        elif ball_x >= self.width - 1:
            self.player_score += 1
            self.reset_ball(direction=-1)
            if self.player_score >= self.WINNING_SCORE:
                self.game_over = True
        
        # Update AI
        self.update_ai()

    def render(self) -> None:
        """Render the game state to the screen."""
        self.stdscr.clear()
        
        # Draw paddles
        for i in range(self.player.height):
            try:
                self.stdscr.addch(self.player.y + i, self.player.x, '█')
            except curses.error:
                pass
        
        for i in range(self.ai.height):
            try:
                self.stdscr.addch(self.ai.y + i, self.ai.x, '█')
            except curses.error:
                pass
        
        # Draw ball
        try:
            self.stdscr.addch(int(self.ball.y), int(self.ball.x), '●')
        except curses.error:
            pass
        
        # Draw center line
        for y in range(0, self.height, 2):
            try:
                self.stdscr.addch(y, self.width // 2, '┊')
            except curses.error:
                pass
        
        # Draw scores
        score_text = f"Player: {self.player_score}  AI: {self.ai_score}"
        try:
            self.stdscr.addstr(0, self.width // 2 - len(score_text) // 2, score_text)
        except curses.error:
            pass
        
        # Draw status messages
        if self.game_over:
            winner = "PLAYER" if self.player_score >= self.WINNING_SCORE else "AI"
            msg1 = f"{winner} WINS!"
            msg2 = "Press R to restart, Q to quit"
            try:
                self.stdscr.addstr(
                    self.height // 2 - 1,
                    self.width // 2 - len(msg1) // 2,
                    msg1,
                    curses.A_BOLD,
                )
                self.stdscr.addstr(
                    self.height // 2 + 1,
                    self.width // 2 - len(msg2) // 2,
                    msg2,
                )
            except curses.error:
                pass
        elif self.paused:
            msg = "PAUSED - Press P to continue"
            try:
                self.stdscr.addstr(
                    self.height // 2,
                    self.width // 2 - len(msg) // 2,
                    msg,
                    curses.A_BOLD,
                )
            except curses.error:
                pass
        
        self.stdscr.refresh()

    def restart(self) -> None:
        """Restart the game."""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.paused = False
        self.reset_ball()

    def run(self) -> None:
        """Main game loop."""
        while True:
            if not self.handle_input():
                break
            
            self.update_physics()
            self.render()
            
            time.sleep(0.016)  # ~60 FPS


def main() -> None:
    """Entry point for the game."""
    curses.wrapper(lambda stdscr: PongGame(stdscr).run())


if __name__ == "__main__":
    main()

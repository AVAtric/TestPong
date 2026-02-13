"""Game state dataclass."""

from dataclasses import dataclass


@dataclass
class GameState:
    """Game state for the Pong game."""
    player_y: int
    ai_y: int
    ball_x: int
    ball_y: int
    player_score: int
    ai_score: int
    paused: bool
    game_over: bool
    winner: str | None = None
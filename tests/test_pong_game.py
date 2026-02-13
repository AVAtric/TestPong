"""Tests for Pong game module."""

import pytest

from pongclaw.game_state import GameState
from pongclaw.pong_game import PongGame


def test_game_initialization():
    """Test game initialization."""
    game = PongGame()
    state = game.get_state()

    assert state.player_y == 9  # (24 - 6) // 2
    assert state.ai_y == 9
    assert state.ball_x == 40
    assert state.ball_y == 12
    assert state.player_score == 0
    assert state.ai_score == 0
    assert not state.paused
    assert not state.game_over


def test_wall_bounce():
    """Test ball bounce off top and bottom walls."""
    game = PongGame()
    game.ball_y = 1  # Near top

    game.update()
    state = game.get_state()

    # Ball should bounce
    assert state.ball_y > 1
    # Y direction should be negative (moving down)
    assert game.ball_dir_y > 0


def test_player_paddle_collision():
    """Test ball collision with player paddle."""
    game = PongGame()
    game.player_y = 9
    game.ball_x = 1.5  # Near left edge
    game.ball_dir_x = -0.15  # Moving left

    game.update()
    state = game.get_state()

    # Ball should bounce right
    assert state.ball_x > 0.5
    # X direction should be positive
    assert game.ball_dir_x > 0


def test_ai_paddle_collision():
    """Test ball collision with AI paddle."""
    game = PongGame()
    game.ai_y = 9
    game.ball_x = 78.5  # Near right edge
    game.ball_dir_x = 0.15  # Moving right

    game.update()
    state = game.get_state()

    # Ball should bounce left
    assert state.ball_x < 79.5
    # X direction should be negative
    assert game.ball_dir_x < 0


def test_score_tracking():
    """Test score tracking."""
    game = PongGame()

    # Ball goes past player (left edge)
    game.ball_x = -0.5
    game.update()

    state = game.get_state()
    assert state.ai_score == 1

    # Ball goes past AI (right edge)
    game.ball_x = 80.5
    game.update()

    state = game.get_state()
    assert state.player_score == 1


def test_paddle_bounds():
    """Test paddles stay within bounds."""
    game = PongGame()
    game.player_y = 0
    game.player_dir = 1

    # Move paddle down past bounds
    for _ in range(100):
        game.update()

    state = game.get_state()
    assert state.player_y >= 0

    game.ai_y = 18
    game.ai_dir = 1

    for _ in range(100):
        game.update()

    state = game.get_state()
    assert state.ai_y <= 18


def test_scoring_reset():
    """Test ball resets after scoring."""
    game = PongGame()
    game.ai_score = 1
    game.ball_x = -0.5
    game.update()

    state = game.get_state()
    assert state.ball_x == 40  # Reset to center


def test_win_condition():
    """Test game win condition."""
    game = PongGame()
    game.player_score = 7
    game.check_win()

    state = game.get_state()
    assert state.game_over
    assert state.winner == "Player"


def test_ai_movement():
    """Test AI paddle movement towards ball."""
    game = PongGame()
    game.ball_y = 5

    game.update()

    state = game.get_state()
    # AI should move towards ball
    assert state.ai_y >= 9 or state.ai_y <= 9


def test_game_over_controls():
    """Test game over screen controls."""
    game = PongGame()
    game.game_over = True
    game.winner = "AI"

    # Should handle quit
    with pytest.raises(SystemExit):
        game.process_input('q')
    # Q shouldn't crash (handled by SystemExit)

    # Restart should reset game
    game.process_input('r')
    state = game.get_state()
    assert not state.game_over
    assert state.player_score == 0


def test_pause_functionality():
    """Test pause functionality."""
    game = PongGame()
    game.process_input('p')

    state = game.get_state()
    assert state.paused

    game.process_input('p')
    state = game.get_state()
    assert not state.paused


def test_input_handling():
    """Test various input controls."""
    game = PongGame()
    initial_y = game.get_state().player_y

    # W key for up
    game.process_input('w')
    state = game.get_state()
    assert state.player_y < initial_y or state.player_y == initial_y

    # S key for down
    game.process_input('s')
    state = game.get_state()
    assert state.player_y > initial_y or state.player_y == initial_y

    # Arrow keys
    game.process_input('\x1b[A')  # Up
    state = game.get_state()
    assert state.player_y < initial_y or state.player_y == initial_y

    game.process_input('\x1b[B')  # Down
    state = game.get_state()
    assert state.player_y > initial_y or state.player_y == initial_y

    # Invalid input
    game.process_input('x')
    state = game.get_state()
    # Should stay in place
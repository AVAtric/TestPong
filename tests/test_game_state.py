"""Tests for game state module."""

import pytest

from pongclaw.game_state import GameState


def test_game_state_initialization():
    """Test GameState initialization."""
    state = GameState(
        player_y=5,
        ai_y=10,
        ball_x=40,
        ball_y=12,
        player_score=3,
        ai_score=2,
        paused=False,
        game_over=False,
        winner=None
    )

    assert state.player_y == 5
    assert state.ai_y == 10
    assert state.ball_x == 40
    assert state.ball_y == 12
    assert state.player_score == 3
    assert state.ai_score == 2
    assert not state.paused
    assert not state.game_over
    assert state.winner is None


def test_game_state_with_winner():
    """Test GameState with winner set."""
    state = GameState(
        player_y=5,
        ai_y=10,
        ball_x=40,
        ball_y=12,
        player_score=7,
        ai_score=5,
        paused=False,
        game_over=True,
        winner="Player"
    )

    assert state.winner == "Player"
    assert state.game_over
    assert state.player_score == 7
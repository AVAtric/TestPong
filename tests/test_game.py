"""Tests for PongClaw game logic."""

import pytest
from pongclaw.entities import Ball, Paddle


class TestPaddle:
    """Test Paddle class behavior."""

    def test_paddle_creation(self):
        """Test paddle initialization."""
        paddle = Paddle(x=5, y=10, height=5, width=1)
        assert paddle.x == 5
        assert paddle.y == 10
        assert paddle.height == 5
        assert paddle.width == 1

    def test_paddle_move_up(self):
        """Test paddle moves up correctly."""
        paddle = Paddle(x=5, y=10, height=5)
        paddle.move_up(screen_height=20)
        assert paddle.y == 9

    def test_paddle_move_down(self):
        """Test paddle moves down correctly."""
        paddle = Paddle(x=5, y=10, height=5)
        paddle.move_down(screen_height=20)
        assert paddle.y == 11

    def test_paddle_upper_bound(self):
        """Test paddle respects upper screen boundary."""
        paddle = Paddle(x=5, y=0, height=5)
        paddle.move_up(screen_height=20)
        assert paddle.y == 0  # Should not go below 0

    def test_paddle_lower_bound(self):
        """Test paddle respects lower screen boundary."""
        paddle = Paddle(x=5, y=15, height=5)
        paddle.move_down(screen_height=20)
        assert paddle.y == 15  # Should not exceed screen_height - height

    def test_paddle_collision_detection(self):
        """Test paddle collision detection."""
        paddle = Paddle(x=5, y=10, height=5, width=1)
        assert paddle.contains_point(5, 10) is True
        assert paddle.contains_point(5, 14) is True
        assert paddle.contains_point(5, 15) is False
        assert paddle.contains_point(4, 10) is False
        assert paddle.contains_point(6, 10) is False


class TestBall:
    """Test Ball class behavior."""

    def test_ball_creation(self):
        """Test ball initialization."""
        ball = Ball(x=10.0, y=20.0, dx=0.5, dy=0.3)
        assert ball.x == 10.0
        assert ball.y == 20.0
        assert ball.dx == 0.5
        assert ball.dy == 0.3

    def test_ball_movement(self):
        """Test ball moves correctly."""
        ball = Ball(x=10.0, y=20.0, dx=0.5, dy=0.3)
        ball.move()
        assert ball.x == 10.5
        assert ball.y == 20.3

    def test_ball_vertical_bounce(self):
        """Test ball bounces off horizontal walls."""
        ball = Ball(x=10.0, y=0.0, dx=0.5, dy=-0.3)
        ball.bounce_vertical()
        assert ball.dx == 0.5  # Horizontal velocity unchanged
        assert ball.dy == 0.3  # Vertical velocity reversed

    def test_ball_horizontal_bounce(self):
        """Test ball bounces off paddles."""
        ball = Ball(x=5.0, y=12.0, dx=0.5, dy=0.0)
        ball.bounce_horizontal(paddle_y=10, paddle_height=5)
        assert ball.dx == -0.5  # Horizontal velocity reversed
        # Vertical velocity should be adjusted based on hit position
        assert ball.dy != 0.0

    def test_ball_paddle_bounce_angle_top(self):
        """Test ball bounce angle when hitting top of paddle."""
        ball = Ball(x=5.0, y=10.0, dx=0.5, dy=0.0)
        ball.bounce_horizontal(paddle_y=10, paddle_height=5)
        assert ball.dx < 0  # Reversed
        assert ball.dy < 0  # Should angle upward (negative y)

    def test_ball_paddle_bounce_angle_center(self):
        """Test ball bounce angle when hitting center of paddle."""
        ball = Ball(x=5.0, y=12.5, dx=0.5, dy=0.0)
        ball.bounce_horizontal(paddle_y=10, paddle_height=5)
        assert ball.dx < 0  # Reversed
        assert abs(ball.dy) < 0.1  # Should be nearly straight

    def test_ball_paddle_bounce_angle_bottom(self):
        """Test ball bounce angle when hitting bottom of paddle."""
        ball = Ball(x=5.0, y=14.9, dx=0.5, dy=0.0)
        ball.bounce_horizontal(paddle_y=10, paddle_height=5)
        assert ball.dx < 0  # Reversed
        assert ball.dy > 0  # Should angle downward (positive y)

    def test_ball_reset(self):
        """Test ball resets to specified position and velocity."""
        ball = Ball(x=50.0, y=25.0, dx=1.0, dy=0.5)
        ball.reset(x=10.0, y=15.0, dx=0.5, dy=0.2)
        assert ball.x == 10.0
        assert ball.y == 15.0
        assert ball.dx == 0.5
        assert ball.dy == 0.2


class TestGameLogic:
    """Test game logic scenarios."""

    def test_scoring_reset(self):
        """Test that scoring resets ball position."""
        # This is a basic test of the concept
        ball = Ball(x=0.0, y=10.0, dx=-0.5, dy=0.0)
        # Simulate scoring (ball goes off screen)
        assert ball.x <= 0  # Ball is past left edge
        # Reset would be called
        ball.reset(x=40.0, y=20.0, dx=0.5, dy=0.3)
        assert ball.x == 40.0
        assert ball.dx > 0  # Ball now moving right

    def test_wall_bounce_maintains_speed(self):
        """Test that wall bounces maintain ball speed magnitude."""
        ball = Ball(x=10.0, y=0.0, dx=0.5, dy=-0.3)
        original_speed_y = abs(ball.dy)
        ball.bounce_vertical()
        assert abs(ball.dy) == original_speed_y
        assert ball.dy == 0.3  # Sign changed

    def test_paddle_collision_prevents_passthrough(self):
        """Test paddle collision detection works at boundaries."""
        paddle = Paddle(x=5, y=10, height=5)
        # Ball at exact paddle position
        assert paddle.contains_point(5, 10) is True
        # Ball just before paddle
        assert paddle.contains_point(4, 10) is False
        # Ball just after paddle
        assert paddle.contains_point(6, 10) is False

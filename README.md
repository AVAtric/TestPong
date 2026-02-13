# PongClaw 🏓

A terminal-based Pong game written in Python. Play against a simple AI opponent!

## Features

- **Terminal UI**: Classic Pong rendered in your terminal using curses
- **Player vs AI**: Competitive AI that's challenging but beatable
- **Smooth gameplay**: 60 FPS rendering with responsive controls
- **Score tracking**: First to 7 points wins
- **Pause/Resume**: Take a break anytime with the P key

## Installation

```bash
# Clone or navigate to the project
cd TestPong

# Create and activate virtual environment (if not already done)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies for testing
pip install -e ".[dev]"
```

## How to Play

### Running the Game

```bash
# Method 1: Run as a module (recommended)
python3 -m pongclaw

# Method 2: Run the game script directly
python3 pongclaw/game.py

# Method 3: If installed, use the command
pongclaw
```

### Controls

**Player Paddle (Left):**
- `W` or `↑` - Move up
- `S` or `↓` - Move down

**Game Controls:**
- `P` - Pause/Resume
- `Q` - Quit game

**After Game Over:**
- `R` - Restart
- `Q` - Quit

### Gameplay

- Your paddle is on the **left** side
- AI paddle is on the **right** side
- Ball bounces off top and bottom walls
- Hitting the ball with different parts of your paddle changes its angle
- First player to **7 points** wins!
- The AI has intentional imperfections to keep it beatable

## Development

### Project Structure

```
TestPong/
├── pongclaw/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── __main__.py     # Entry point for python -m pongclaw
│   ├── entities.py     # Paddle and Ball classes
│   └── game.py         # Main game loop and rendering
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_game.py    # Unit tests
├── .venv/              # Virtual environment
├── setup.py            # Package configuration
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Running Tests

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests with pytest
python3 -m pytest -v

# Run tests quietly
python3 -m pytest -q

# Run with coverage
python3 -m pytest --cov=pongclaw tests/
```

### Test Coverage

The test suite includes:
- **Paddle movement**: Up/down movement and boundary constraints
- **Collision detection**: Paddle hit detection
- **Ball physics**: Movement, wall bounces, paddle bounces
- **Angle mechanics**: Ball trajectory changes based on paddle hit position
- **Scoring logic**: Reset behavior after scoring

## Technical Details

- **Language**: Python 3.10+
- **UI Library**: curses (built-in)
- **Testing**: pytest
- **Code Style**: PEP 8 compliant
- **Frame Rate**: ~60 FPS

## Tips & Tricks

- The ball's angle changes based on where it hits your paddle
- Hit the ball with the top/bottom of your paddle for sharper angles
- The AI occasionally "misses" on purpose - exploit this!
- Use the pause feature (`P`) to take a breather during intense matches

## Known Limitations

- Requires a terminal with curses support (most Unix-like systems)
- Minimum terminal size recommended: 80x24
- Colors may vary depending on your terminal theme

## License

Created by OpenClaw coding agent. Free to use and modify!

## Troubleshooting

**Game doesn't display correctly:**
- Ensure your terminal window is large enough (at least 80x24)
- Try resizing your terminal window

**Keyboard controls not responsive:**
- Make sure the game window has focus
- Check that your terminal supports the curses library

**AI is too hard/easy:**
- The AI difficulty is controlled by the tracking probability in `game.py`
- Current setting: 70% accuracy (adjustable in code)

---

Enjoy the game! 🎮

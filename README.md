# TestPong - Terminal Pong Game

A classic Pong game implemented in Python with a terminal UI.

## Features

- Terminal-based graphics using ANSI escape codes
- Player paddle controls with W/S keys (Up/Down arrow keys also supported)
- Simple AI opponent that tracks the ball
- Ball physics with wall bounces and paddle deflections
- Score tracking with first to 7 wins
- Game states: playing, paused, and game over
- Restart and quit functionality

## Installation

1. Create and activate the virtual environment:
```bash
cd TestPong
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the package:
```bash
pip install -e .
```

## Controls

- **W / Up Arrow**: Move player paddle up
- **S / Down Arrow**: Move player paddle down
- **P**: Pause/Unpause game
- **R**: Restart game (after game over)
- **Q**: Quit game (after game over)

## Running the Game

### Using the module entry point:
```bash
python3 -m pongclaw
```

### Using the console script:
```bash
pongclaw
```

## Project Structure

```
TestPong/
├── pongclaw/          # Main package
│   ├── __init__.py
│   ├── __main__.py    # Entry point
│   ├── game_state.py  # Game state dataclass
│   └── pong_game.py   # Main game logic
├── tests/             # Test directory
├── .venv/            # Virtual environment
├── setup.py          # Package setup
└── README.md         # This file
```

## Testing

Run the test suite using pytest:

```bash
cd TestPong
source .venv/bin/activate
pytest tests/ -v
```

or with quiet mode:

```bash
pytest tests/ -q
```

## Game Rules

1. The ball bounces off the top and bottom walls
2. The ball bounces off player and AI paddles
3. Hitting the paddle changes the ball's angle slightly
4. The first player to reach 7 points wins
5. Game over screen allows restarting or quitting

## Technical Details

- Terminal resolution: 80x24 characters
- Paddle size: 2 columns wide, 6 rows high
- Ball speed increases slightly after each paddle hit
- AI has a slight delay for beatability
- Uses Python's `termios` and `tty` modules for terminal control
- ANSI escape codes for colors and cursor control
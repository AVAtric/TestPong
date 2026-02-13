"""Main entry point for running the Pong game."""

from .pong_game import PongGame, get_char


def main() -> None:
    """Run the Pong game."""
    print("\033[2J\033[H")  # Clear screen
    print("\033[36mWelcome to Terminal Pong!\033[0m")
    print("\033[37mControls: W/S or Arrow Keys to move | P to pause | R to restart | Q to quit\033[0m")
    print("\033[37mFirst to 7 points wins!\033[0m")
    print("\033[33mPress any key to start...\033[0m")

    # Wait for any key
    get_char()

    game = PongGame()

    while True:
        game.render()
        if not game.game_over and not game.paused:
            char = get_char()
            game.process_input(char)

        game.update()
        time.sleep(0.02)  # Control game speed


if __name__ == "__main__":
    main()
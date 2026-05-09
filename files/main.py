# main.py
# Entry point for the dungeon game.
# Creates the player and starts the game loop.

from player import create_player
from game import run_game


def main():
    player = create_player()
    run_game(player)


if __name__ == "__main__":
    main()

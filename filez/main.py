# main.py
from player import create_player
from game import run_game

if __name__ == "__main__":
    player = create_player()
    run_game(player)

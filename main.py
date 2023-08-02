import logging
from game_classes.player import Player
from game_classes.game import Game
from run_game import run_game

if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
        level=logging.DEBUG
    )

    player_1 = Player('Игрок 1')
    player_2 = Player('Игрок 2')
    game = Game([player_1, player_2])
    run_game(10, game)

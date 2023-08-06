import sys
import time

import pygame as pg

import config
from game_classes.game import Game
from events import click_react
from interface_classes.interface import Interface
from computer_player import autoturn
from events import make_turn


def run_game(size: int, game: Game) -> None:
    """
    Controls interface. Creates screen, board, menu and starts new game.
            Then runs events processing and refreshes the screen
    :param size: size of a board for start state
    :param game: Game object
    :return: None
    """
    pg.init()
    screen = pg.display.set_mode(config.screen_dim)
    pg.display.set_caption("Tic-Tac-Toe")

    interface = Interface(screen, ['Small game', 'Big game', 'Quit'], size)

    game.curr_turn = game.start_game(size, 5)
    interface.state_bar.update_state_bar('Big game started. Now turn of {name}'.format(
        name=game.players[game.curr_turn].name))

    screen.blits(interface.get_all_elements())
    pg.display.flip()

    while True:
        if game.curr_turn == 1 and game.state != 1:
            cell_name = autoturn(game.board, game.players)
            make_turn(interface, game, cell_name)
            pg.event.clear()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                click_react(mouse_pos, interface, game)



        screen.blits(interface.get_all_elements())

        pg.display.flip()

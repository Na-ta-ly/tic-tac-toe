import logging
from typing import Tuple
import sys

from game_classes.game import Game
import config
from interface_classes.interface import Interface


def click_react(mouse_pos: Tuple[int, int], interface: Interface, game: Game) -> None:
    """
    Reaction on the mouse click event. Processes manipulation with menu buttons, checks
            what board cell was chosen and runs appropriate operation
    :param mouse_pos: cursor position (x, y)
    :param interface: current Interface object
    :param game: current game
    """
    # ----- check for menu buttons
    for button in interface.menu.buttons:
        if interface.menu.buttons[button].rectangle.collidepoint(mouse_pos):
            logging.debug(' '.join(['Pressed', str(button), 'button']))
            if button.lower() == 'quit':
                sys.exit()

            elif button.lower() == 'small game':
                interface.board.draw_new_greed(config.small_game_size)
                game.curr_turn = game.start_game(config.small_game_size, 3)
                interface.state_bar.update_state_bar('Small game started. Now turn of {name}'.format(
                    name=game.players[game.curr_turn].name))

            elif button.lower() == 'big game':
                interface.board.draw_new_greed(config.big_game_size)
                game.curr_turn = game.start_game(config.big_game_size, 5)
                interface.state_bar.update_state_bar('Big game started. Now turn of {name}'.format(
                    name=game.players[game.curr_turn].name))
            return  # if object found

    # ----- check for cells
    size = int(len(interface.board.cells()) ** 0.5)
    for index_1 in range(size):
        for index_2 in range(size):
            cell_name = (index_1, index_2)
            cell = interface.board.cells()[cell_name]
            if cell.rectangle.collidepoint(mouse_pos):
                logging.debug(' '.join(['Click on', str(cell_name), 'cell']))

                if game.state != 1:  # if game is not over yet

                    if game.single_turn(game.players[game.curr_turn], cell_name):
                        interface.set_mark(cell_name, game.players[game.curr_turn].mark)
                        game.curr_turn = 1 - game.curr_turn
                        interface.state_bar.update_state_bar('Now turn of {name}'.format(
                            name=game.players[game.curr_turn].name))
                    result_check = game.board.check_win_combo(game.board.cells[cell_name])
                    if result_check[0]:
                        game.state = 1
                        winner = result_check[1]
                        if winner == '-':
                            tail = 'Drawn game!'
                        else:
                            tail = 'Win of {name}!'.format(name=game.players[1 - game.curr_turn].name)
                        interface.state_bar.update_state_bar(' '.join(['Game is over.', tail]))
                return  # if object found

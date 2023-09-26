import math
import re
from collections import Counter
from datetime import datetime
import logging
from random import randint
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

from game_classes.board import Board
from game_classes.cell import Cell
from game_classes.player import Player

game_results = {'x': 1, '-': 0, 'o': -1}


# Probably add func copying state from another board
def get_player(board: Board) -> str:
    """
    Returns mark, that should be put next
    :param board: board for analysis
    :return: mark 'x' or 'o' for the next player
    """
    cells = board.cells
    values = []
    for cell in cells.values():
        values.append(cell.get_mark())
    board_statistic = Counter(values)
    if board_statistic.get('x', 0) != board_statistic.get('o', 0):
        return 'o'
    return 'x'


def get_possible_combos(board: Board) -> List[Tuple[int, int]]:
    """
    Returns all combos for check
    :param board: current board
    :return: list of cell names
    """
    result = []
    max_distance = 1  # distance from already filled cells
    second_list = []
    list_contacts = []
    for cell in board.cells.values():
        cell_mark = cell.get_mark()
        if cell_mark != ' ':  # check if cell is filled
            has_contact = 1  # filled with the same mark cells near current
            temp_names = []
            just_filled_list = []  # list of empty cells among cell's neighbours

            for distance in range(1, max_distance + 1):  # add all cells in max_distance to temp_names
                temp_names.append((cell.name[0] - distance, cell.name[1]))
                temp_names.append((cell.name[0] + distance, cell.name[1]))
                temp_names.append((cell.name[0], cell.name[1] - distance))
                temp_names.append((cell.name[0], cell.name[1] + distance))
                temp_names.append((cell.name[0] - distance, cell.name[1] - distance))
                temp_names.append((cell.name[0] + distance, cell.name[1] + distance))
                temp_names.append((cell.name[0] + distance, cell.name[1] - distance))
                temp_names.append((cell.name[0] - distance, cell.name[1] + distance))

            for potential_name in temp_names:  # check temp cells if they have same mark or any mark
                potential_cell = board.cells.get(potential_name, None)
                if potential_cell is not None:  # if exists
                    if cell_mark == potential_cell.get_mark():
                        has_contact += 1  # cell with same mark
                    if potential_cell.get_mark() == ' ':
                        just_filled_list.append(potential_name)  # empty neighbours

            if has_contact >= 2:  # if many same marks around
                list_contacts.extend(just_filled_list)
            else:
                second_list.extend(just_filled_list)

    if len(list_contacts) >= 5:  # if list_contacts large
        result.extend(list_contacts)
    else:
        result.extend(list_contacts + second_list)

    result = list(set(result))

    if board.filled_cells < board.condition:
        result = [result[randint(0, len(result) - 1)]]
    # print(f'Sent {len(result)} combos')

    return result


def minimax(board: Board, player_1: Player, player_2: Player, depth: int = 0) -> float:
    current_state = board.check_win_combo()

    if current_state[0]:
        return game_results.get(current_state[1], 0)
    depth += 1
    if depth >= 4:
        return 0
    current_mark = get_player(board)
    if current_mark == player_1.mark:
        current_player = player_1
    else:
        current_player = player_2

    func = max if current_mark == 'x' else min

    value = -math.inf if current_mark == 'x' else math.inf
    initial_value = value
    for combo in get_possible_combos(board):
        new_board = board.copy()
        new_board.single_turn(current_player, combo)
        value = func(value, minimax(new_board, player_1, player_2, depth))

        # if value == -game_results.get(current_mark):
        #     print('pruning')
        #     return -game_results.get(current_mark)
        value += 1 * value
    return value

    # if get_player(board) == player_1.mark:
    #     value = 0
    #     for combo in get_possible_combos(board):
    #         new_board = board.copy()
    #         new_board.single_turn(player_1, combo)
    #         result = minimax(new_board, player_1, player_2, depth)
    #         value += 1 * result
    #         # if result == -1:
    #         #     print('pruning')
    #         #     return -1
    #     return value
    # if get_player(board) == player_2.mark:
    #     value = 0
    #     for combo in get_possible_combos(board):
    #         new_board = board.copy()
    #         new_board.single_turn(player_2, combo)
    #         result = minimax(new_board, player_1, player_2, depth)
    #         value += 1 * result
    #         # if result == 1:
    #         #     print('pruning')
    #         #     return 1
    #     return value


def autoturn(board: Board, players: List[Player]) -> Tuple[int, int]:
    start_time = datetime.now()
    if board.filled_cells == 0:
        return int((board.size - 1) / 2), int((board.size - 1) / 2)
    variation_list = get_possible_combos(board)

    queue = mp.Queue()
    processes = []
    for combo in variation_list:
        p = mp.Process(target=test, args=(board, players[0], players[1], combo, queue))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    results = []
    while not queue.empty():
        results.append(queue.get())

    for i in range(len(results)):
        print(results[i][0], ': ', results[i][1])
    current_player = get_player(board)
    func = max if current_player == 'x' else min

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    target_value = func([i[1] for i in results])
    same_results = [1 if item[1] == target_value else 0 for item in results]
    if sum(same_results) == len(results):
        print("Choose only 1 combo. ", sum(same_results))
        return results[randint(0, len(results) - 1)][0]

    for item in range(len(results)):
        if results[item][1] == target_value:
            return results[item][0]
    return 0, 0


    # maximum = []
    # for combo in variation_list:
    #     new_board = board.copy()
    #     new_board.single_turn(players[1], combo)
    #     maximum.append(minimax(new_board, players[0], players[1]))
    # for i in range(len(maximum)):
    #     print(variation_list[i], ': ', maximum[i])
    # func = max if players[1].mark == 'x' else min
    #
    # end_time = datetime.now()
    # print('Duration: {}'.format(end_time - start_time))
    #
    # if maximum.count(func(maximum)) == len(maximum):
    #     print("Choose only 1 combo. ", maximum.count(func(maximum)))
    #     return variation_list[randint(0, len(maximum) - 1)]
    # return variation_list[maximum.index(func(maximum))]


def test(board, players_1, players_2, combo, queue):
    new_board = board.copy()
    new_board.single_turn(players_2, combo)
    queue.put((combo, minimax(new_board, players_1, players_2)))


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
        level=logging.ERROR
    )
    board = Board(10, 5)
    player_1 = Player('Player')
    player_1.mark = 'o'
    player_2 = Player('Computer')
    player_2.mark = 'x'

    start_time = datetime.now()

    board.single_turn(player_2, (3, 2))
    board.single_turn(player_1, (2, 1))
    board.single_turn(player_2, (4, 2))
    board.single_turn(player_1, (2, 2))
    board.single_turn(player_2, (5, 3))
    board.single_turn(player_1, (2, 3))
    board.single_turn(player_2, (3, 3))
    board.single_turn(player_1, (1, 4))
    print(board)
    cell_name = autoturn(board, [player_1, player_2])
    print(cell_name)
    board.single_turn(player_2, cell_name)
    print(board)

    end_time = datetime.now()
    print('Total Duration: {}'.format(end_time - start_time))


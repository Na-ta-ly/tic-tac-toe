import math
import re
from collections import Counter
from datetime import datetime
import logging
from random import randint
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

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


def get_possible_combos(board: Board):
    unfilled_cells = []
    result = []
    max_distance = 1
    second_list = []
    list_contacts = []
    for cell in board.cells.values():
        cell_mark = cell.get_mark()
        if cell_mark != ' ':
            has_contact = 1
            temp_names = []
            just_filled_list = []
            # has_contact = False
            for distance in range(1, max_distance + 1):
                temp_names.append((cell.name[0] - distance, cell.name[1]))
                temp_names.append((cell.name[0] + distance, cell.name[1]))
                temp_names.append((cell.name[0], cell.name[1] - distance))
                temp_names.append((cell.name[0], cell.name[1] + distance))
                temp_names.append((cell.name[0] - distance, cell.name[1] - distance))
                temp_names.append((cell.name[0] + distance, cell.name[1] + distance))
                temp_names.append((cell.name[0] + distance, cell.name[1] - distance))
                temp_names.append((cell.name[0] - distance, cell.name[1] + distance))

            for potential_name in temp_names:
                potential_cell = board.cells.get(potential_name, None)
                if potential_cell is not None:
                    if cell_mark == potential_cell.get_mark():
                        has_contact += 1
                    if potential_cell.get_mark() == ' ':
                        just_filled_list.append(potential_name)
            if has_contact >= 2:
                list_contacts.extend(just_filled_list)
            else:
                second_list.extend(just_filled_list)
    if len(list_contacts) >= 5:
        result.extend(list_contacts)
        # print(list_contacts)
    else:
        result.extend(list_contacts + second_list)
        # print(list_contacts+second_list)
    # print(result)
    result = list(set(result))
    if board.filled_cells < board.condition:
        result = [result[randint(0, len(result) - 1)]]
    print(f'Sent {len(result)} combos')
    # names = []
    # for distance in range(1, max_distance + 1):
    #     names.append((cell.name[0] - distance, cell.name[1]))
    #     names.append((cell.name[0] + distance, cell.name[1]))
    #     names.append((cell.name[0], cell.name[1] - distance))
    #     names.append((cell.name[0], cell.name[1] + distance))
    #     names.append((cell.name[0] - distance, cell.name[1] - distance))
    #     names.append((cell.name[0] + distance, cell.name[1] + distance))
    #     names.append((cell.name[0] + distance, cell.name[1] - distance))
    #     names.append((cell.name[0] - distance, cell.name[1] + distance))
    # if board.filled_cells > 4:
    #     for potential_name in names:
    #         if cell_mark == board.cells[potential_name].get_mark():
    #             for name in names:
    #                 potential_cell = board.cells.get(name, None)
    #                 if potential_cell is not None and potential_cell.get_mark() == ' ':
    #                     unfilled_cells.append(name)
    #             break
    # else:
    #     for name in names:
    #         potential_cell = board.cells.get(name, None)
    #         if potential_cell is not None and potential_cell.get_mark() == ' ':
    #             unfilled_cells.append(name)
    # unfilled_cells = list(set(unfilled_cells))
    # print(unfilled_cells)
    # unfilled_cells = [cell.name for cell in board.cells.values() if cell.get_mark() == ' ']
    return result


def minimax(board, player_1, player_2, depth=0):
    # print("Current depth", depth)
    current_state = board.check_win_combo()

    if current_state[0]:
        # print('current_state:', current_state)
        return game_results.get(current_state[1], 0)
    # print(boards)
    depth += 1
    if depth >= 4:
        return 0
    if get_player(board) == player_1.mark:
        value = 0
        for combo in get_possible_combos(board):
            new_board = board.copy()
            new_board.single_turn(player_1, combo)
            result = minimax(new_board, player_1, player_2, depth)
            value += 0.99 * result
            if result == -1:
                print('pruning')
                return -1
        return value
    if get_player(board) == player_2.mark:
        value = 0
        for combo in get_possible_combos(board):
            new_board = board.copy()
            new_board.single_turn(player_2, combo)
            result = minimax(new_board, player_1, player_2, depth)
            value += 0.99 * result
            if result == 1:
                print('pruning')
                return 1
        return value


def autoturn(board, players):
    start_time = datetime.now()
    if board.filled_cells == 0:
        return int((board.size - 1) / 2), int((board.size - 1) / 2)
    variation_list = get_possible_combos(board)
    # print(variation_list)
    # combo_list = mp.Queue()
    # for i in variation_list:
    #     combo_list.put(i)

    maximum = mp.Queue()

    # combo = combo_list.get()[0]
    # print(combo)
    processes = []
    procs = len(variation_list) // 6 + 1
    # while not combo_list.empty():
    #     k = combo_list.get()
    #     print(k)
    # print('combo_list is empty')
    for combo in variation_list:
        # for proc in range(6):
        p = mp.Process(target=test, args=(board, players[0], players[1], combo, maximum))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # with ProcessPoolExecutor(max_workers=6) as executor:
    #     # Set all but one worker making salads
    #     for _ in range(6):
    #         executor.submit(test, board, players[0], players[1], combo_list, maximum)

    # for combo in variation_list:
    #     new_board = board.copy()
    #     new_board.single_turn(players[1], combo)
    #     maximum.append(minimax(new_board, players[0], players[1]))
    results = []
    while not maximum.empty():
        results.append(maximum.get())
    # maximum = [item[0] for item in maximum]
    print(results)
    for i in range(len(results)):
        print(variation_list[i], ': ', results[i])
    func = max if players[1].mark == 'x' else min

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    if results.count(func(results)) == len(results):
        print("Choose only 1 combo. ", results.count(func(results)))
        return variation_list[randint(0, len(results) - 1)]
    return variation_list[results.index(func(results))]
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


def test(board, players_1, players_2, combo, maximum):
    new_board = board.copy()
    new_board.single_turn(players_2, combo)
    maximum.put(minimax(new_board, players_1, players_2))


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
        level=logging.ERROR
    )
    board = Board(4, 3)
    player_1 = Player('Player')
    player_1.mark = 'x'
    player_2 = Player('Computer')
    player_2.mark = 'o'

    start_time = datetime.now()

    board.single_turn(player_2, (1, 0))
    board.single_turn(player_1, (0, 0))
    board.single_turn(player_2, (2, 2))
    board.single_turn(player_1, (2, 1))
    board.single_turn(player_2, (0, 1))
    print(board)
    cell_name = autoturn(board, [player_1, player_2])
    print(cell_name)
    board.single_turn(player_2, cell_name)
    print(board)
    # board.single_turn(player_2, (0, 1))
    board.single_turn(player_1, (2, 0))
    print(board)
    cell_name = autoturn(board, [player_1, player_2])
    print(cell_name)
    board.single_turn(player_2, cell_name)
    print(board)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    # board.single_turn(player_2, (1, 0))
    # board.single_turn(player_1, (0, 0))
    # board.single_turn(player_2, (2, 2))
    # board.single_turn(player_1, (2, 1))
    # while not board.check_win_combo()[0]:
    #     print(board)
    #     cell = tuple(int(item.strip()) for item in input("Player's turn: ").split(','))
    #     board.single_turn(player_1, cell)
    #     print(board)
    #     cell_name = autoturn(board, [player_1, player_2])
    #     print(cell_name)
    #     board.single_turn(player_2, cell_name)
    #     print(board)

    # maximum = - math.inf
    # variation_list = get_possible_combos(board)
    # print(variation_list)
    # maximum = []
    # for combo in variation_list:
    #     new_board = board.copy()
    #     new_board.single_turn(player_2, combo)
    #     maximum.append(minimax(new_board, player_1, player_2))
    # board.single_turn(player_2, (1, 2))
    # board.single_turn(player_1, (0, 2))
    # print(autoturn(board), )

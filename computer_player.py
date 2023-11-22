import math
import re
from collections import Counter
from datetime import datetime
from statistics import median, quantiles
import logging
from random import randint
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple
from numba import jit
from functools import lru_cache

from game_classes.board import Board
from game_classes.cell import Cell
from game_classes.player import Player

game_results = {'x': 1, '-': 0, 'o': -1}
c = dict()


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
    if board_statistic.get('x', 0) > board_statistic.get('o', 0):
        return 'o'
    return 'x'


def get_possible_combos(board: Board) -> List[Tuple[int, int]]:
    """
    Returns all combos for check
    :param board: current board
    :return: list of cell names
    """
    result = dict()
    empty_cells = []
    distance = 1
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    for cell in board.cells.values():  # built list of filled cells with same neighbours
        cell_mark = cell.get_mark()
        candidate = False
        potential = 0

        if cell_mark != ' ' and cell.name not in result.keys():  # if it's filled
            surrounding = dict()
            for key in neighbours:
                test_cell = board.cells.get((cell.name[0] + key[0] * distance, cell.name[1] + key[1] * distance), None)
                if test_cell is not None:
                    surrounding[key] = test_cell

            if ' ' in [item.get_mark() for item in surrounding.values()]:
                for name, value in surrounding.items():  # how many same neighbours has cell and if it has empty space near
                    i = 0
                    test_cell_mark = value.get_mark()
                    while test_cell_mark == cell_mark:
                        potential += 1
                        i += 1
                        new_cell_name = (cell.name[0] + i * name[0], cell.name[1] + i * name[1])
                        new_cell = board.cells.get(new_cell_name, None)
                        test_cell_mark = ' ' if new_cell is None else new_cell.get_mark()
                result[cell.name] = potential
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    # if len(result) > 5:
    #     limit = quantiles([item[1] for item in result], n=4)[-1]
    #     print([item[1] for item in result])
    #     print(quantiles([item[1] for item in result], n=4))
    # else:
    #     limit = 0
    # limit = limit if limit > 3 else 3
    limit = 3
    reduced_results = list(filter(lambda item: item[1] >= limit, result))

    reduced_results = reduced_results if len(reduced_results) > 5 else result[:5]
    # if len(reduced_results) > 10:
    #     reduced_results = reduced_results[:10]
    #     print('use reduced_results')
    # else:
    #     print('use full_results')
    for name, _ in reduced_results:
        for key in neighbours:
            test_cell = board.cells.get((name[0] + key[0] * distance, name[1] + key[1] * distance), None)
            if test_cell is not None and test_cell.get_mark() == ' ':
                empty_cells.append(test_cell.name)

    empty_cells = list(set(empty_cells))
    return empty_cells


@lru_cache(20000)
# @jit(nopython=True)
def minimax(cells, board_size, board_condition, player_1: Player, player_2: Player, depth: int = 0) -> float:
    cur_board = Board(board_size, board_condition)
    cur_board.fill_cells(cells)
    current_state = cur_board.check_win_combo()

    if current_state[0]:
        return game_results.get(current_state[1], 0)
    depth += 1
    if depth >= 4:
        return game_results.get('-', 0)
    current_mark = get_player(cur_board)
    if current_mark == player_1.mark:
        current_player = player_1
    else:
        current_player = player_2

    func = max if current_mark == 'x' else min

    value = -math.inf if current_mark == 'x' else math.inf
    for combo in get_possible_combos(cur_board):
        new_board = cur_board.copy()
        new_board.single_turn(current_player, combo)
        new_cells = str(new_board)
        turn_result = minimax(new_cells, cur_board.size, cur_board.condition, player_1, player_2, depth)

        result = func(value, turn_result)
        value = result
        # if depth >= 2 and turn_result == -game_results.get(current_mark):
        #     # print(new_board)
        #     print('opposite value')
        #     print(value)
            # value = turn_result
            # break
        # else:
        #     value = result

    return value


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


def test(board, players_1, players_2, combo, queue):
    new_board = board.copy()
    new_board.single_turn(players_2, combo)
    queue.put((combo, minimax(str(new_board), new_board.size, new_board.condition, players_1, players_2)))


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
        level=logging.ERROR
    )
    board = Board(10, 5)
    player_1 = Player('Player')
    player_1.mark = list(game_results.keys())[2]
    player_2 = Player('Computer')
    player_2.mark = list(game_results.keys())[0]

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

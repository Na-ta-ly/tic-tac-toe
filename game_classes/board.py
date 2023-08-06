import logging
import re
from typing import Dict, Tuple

from game_classes.cell import Cell
from game_classes.player import Player


class Board:
    """
    Class for a board, containing the bunch of cells
        :param size: size of a new board
        :param condition: win condition, number of consecutive cells
            one needs to mark

    :prop size: size of the board
    :prop condition: condition for win, number of consecutive cells
    :prop filled_cells: number of non-empty cells on the board
    :prop cells: dictionary of cells {(index_1, index_2): Cell}

    :method check_win_combo: check if any win combination appeared, or
            if the game is over because all cells are filled
    """

    def __init__(self, size: int, condition: int) -> None:
        self.size = size
        self.condition = condition
        self.filled_cells = 0
        self.__cells = dict()
        for index_1 in range(self.size):
            for index_2 in range(self.size):
                name = index_1, index_2
                self.__cells[name] = Cell(name)

    @property
    def size(self) -> int:
        """
        Getter for size property
        :return: size
        """
        return self.__size

    @size.setter
    def size(self, size: int):
        """
        Setter for size property, raises ValueError, if size is not positive int
        :param size: size of the board
        """
        if type(size) == int and size > 0:
            self.__size = size
        else:
            logging.error(' '.join(['Attempt to set', str(size), 'value to board.size']))
            raise ValueError('Board size must be a positive integer')

    @property
    def condition(self) -> int:
        """
        Getter for condition property
        :return: number of cells for victory
        """
        return self.__condition

    @condition.setter
    def condition(self, condition: int):
        """
        Setter for condition property, if condition inappropriate (not positive int)
            raises ValueError. If condition exceeds board size, then board size will
            be set as condition value
        :param condition: number of cells for win, positive int
        """
        if type(condition) != int or condition < 0:
            logging.error(' '.join(['Attempt to set', str(condition), 'value to board.condition']))
            raise ValueError('Win condition must be a positive integer')
        if self.size > condition:
            self.__condition = condition
        else:
            self.__condition = self.size
        self.__condition_exp = re.compile(''.join(['x{', str(condition), '}|o{', str(condition), '}']))
        logging.debug(' '.join(['Board.condition for win was set as', str(condition), 'cells']))

    @property
    def filled_cells(self) -> int:
        """
        Getter for filled_cells property
        :return: number of not empty cells on the board
        """
        return self.__filled_cells

    @filled_cells.setter
    def filled_cells(self, filled_cells: int) -> None:
        """
        Setter for filled_cells property, raises ValueError if the number of filled_cells
                is unsuitable for the current board
        :param filled_cells: number of not empty cells on the board
        """
        if filled_cells > self.size ** 2 or filled_cells < 0 or type(filled_cells) != int:
            logging.error(''.join(['Attempt to set ', str(filled_cells),
                                   ' as a number of filled cells on the board ', str(self.size), 'x', str(self.size)]))
            raise ValueError("Number of filled_cells must be int [0, board.size**2]")
        self.__filled_cells = filled_cells

    @property
    def cells(self) -> Dict:
        """
        Getter for property cells
        :return: dictionary of cells {name: Cell}
        """
        return self.__cells

    # @cells.setter
    # def cells(self, cell: Cell) -> None:
    #     """
    #     Setter for cells
    #     :param cell: new cell, that will be added to cells
    #     """
    #     self.__cells[cell.name] = cell

    # def check_win_combo(self, cell: Cell) -> Tuple[bool, str]:
    #     """
    #     Checks if there is a win combination on the board, or if all cells are filled.
    #     Looks only near given cell
    #     :param cell: last marked cell
    #     :return: True if the game is over and the winner as his mark. If it's drawn game,
    #     second value will be '-'
    #     """
    #     cell_name = cell.name
    #     mark = cell.get_mark()
    #     horizontal = vertical = 0
    #     diagonal_right = diagonal_left = 0
    #     delta = cell_name[1] - cell_name[0]
    #     sum_index = cell_name[0] + cell_name[1]
    #     for index_1 in range(self.size):
    #         if self.cells[cell_name[0], index_1].get_mark() == mark:
    #             horizontal += 1
    #         else:
    #             horizontal = 0
    #         if self.cells[index_1, cell_name[1]].get_mark() == mark:
    #             vertical += 1
    #         else:
    #             vertical = 0
    #         if (0 <= index_1 + delta < self.size) and (
    #                 self.cells[index_1, index_1 + delta].get_mark() == mark):
    #             diagonal_right += 1
    #         else:
    #             diagonal_right = 0
    #         if (0 <= sum_index - index_1 < self.size) and (
    #                 self.cells[index_1, sum_index - index_1].get_mark() == mark):
    #             diagonal_left += 1
    #         else:
    #             diagonal_left = 0
    #         if max(horizontal, vertical, diagonal_right, diagonal_left) >= self.condition:
    #             logging.debug(' '.join(['Win!',
    #                                     'horizontal', str(horizontal),
    #                                     'vertical', str(vertical),
    #                                     'diagonal_right', str(diagonal_right),
    #                                     'diagonal_left', str(diagonal_left)]))
    #             return True, mark
    #
    #     if self.filled_cells == len(self.cells):
    #         logging.debug(''.join(['Drawn game!']))
    #         return True, '-'
    #     return False, '-'

    def single_turn(self, player: Player, cell_name: Tuple[int, int]) -> bool:
        """
        If cell is empty sets mark
        :param player: player, who makes his move
        :param cell_name: tuple of indexes
        :return: True if mark was set successfully
        """
        cell = self.cells.get(cell_name, 0)
        if cell != 0 and cell.get_mark() == ' ':
            cell.set_mark(player.mark)
            self.filled_cells += 1
            logging.debug(' '.join([player.name, 'marked', str(cell_name)]))
            return True
        logging.debug(''.join([player.name, ' wanted to mark ', str(cell_name),
                               ", but the cell isn't empty"]))
        return False

    def check_win_combo(self) -> Tuple[bool, str]:
        """
        Checks if there is a win combination on the board, or if all cells are filled.
        Looks only near given cell
        :param cell: last marked cell
        :return: True if the game is over and the winner as his mark. If it's drawn game,
        second value will be '-'
        """
        results = []
        for index_1 in range(self.size):  # for strings
            main_diagonal = auxiliary_diagonal = ''
            if index_1 == 0:
                for index_2 in range(self.size):  # for rows
                    horizontal = vertical = main_diagonal = auxiliary_diagonal = ''
                    for inner_index in range(self.size):  # for strings inner
                        # for search on main diagonal and parallel
                        main_diagonal = ''.join([main_diagonal,
                                                 str(self.cells.get((inner_index,
                                                                     index_2 + inner_index), Cell((5, 5))).get_mark())])
                        # for auxiliary diagonal and parallel
                        auxiliary_diagonal = ''.join([auxiliary_diagonal,
                                                      str(self.cells.get((inner_index,
                                                                          self.size - inner_index - 1 - index_2),
                                                                         Cell((5, 5))).get_mark())])
                        horizontal = ''.join([horizontal,
                                              str(self.cells.get((index_2, inner_index), Cell((5, 5))).get_mark())])
                        vertical = ''.join([vertical,
                                            str(self.cells.get((inner_index, index_2), Cell((5, 5))).get_mark())])

                    results.append(self.__condition_exp.search(main_diagonal))
                    results.append(self.__condition_exp.search(auxiliary_diagonal))
                    results.append(self.__condition_exp.search(horizontal))
                    results.append(self.__condition_exp.search(vertical))

            else:
                for inner_index in range(self.size - index_1):  # for strings
                    main_diagonal = ''.join([main_diagonal,
                                             str(self.cells.get((inner_index + index_1,
                                                                 inner_index), Cell((5, 5))).get_mark())])
                    auxiliary_diagonal = ''.join([auxiliary_diagonal,
                                                  str(self.cells.get((inner_index + index_1,
                                                                      self.size - inner_index - 1),
                                                                     Cell((5, 5))).get_mark())])
                results.append(self.__condition_exp.search(main_diagonal))
                results.append(self.__condition_exp.search(auxiliary_diagonal))
        # print(results)
        for match in results:
            if match is not None:
                win_combo = match.group(0)
                logging.debug(' '.join([win_combo[0], 'wins!']))
                return True, win_combo[0]

        if self.filled_cells == len(self.cells):
            logging.debug(''.join(['Drawn game!']))
            return True, '-'
        return False, '-'

    def copy(self):
        new_board = Board(self.size, self.condition)
        new_board.filled_cells = self.filled_cells
        new_board.__cells = dict()
        for cell_name in self.__cells:
            new_board.__cells[cell_name] = Cell(cell_name)
            new_board.__cells[cell_name].set_mark(self.__cells[cell_name].get_mark())
        return new_board

    def __str__(self):
        string = ''
        for index in range(self.size):
            sub_string = ''
            for index_1 in range(self.size):
                sub_string = ' '.join([sub_string, self.cells[index, index_1].get_mark()])
            string = '\n'.join([string, sub_string])
        return string

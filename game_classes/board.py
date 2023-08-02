import logging
from typing import Dict, Tuple

from game_classes.cell import Cell


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
                self.cells = Cell(name)

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

    @cells.setter
    def cells(self, cell: Cell) -> None:
        """
        Setter for cells
        :param cell: new cell, that will be added to cells
        """
        self.__cells[cell.name] = cell

    def check_win_combo(self, cell: Cell) -> Tuple[bool, str]:
        """
        Checks if there is a win combination on the board, or if all cells are filled.
        Looks only near given cell
        :param cell: last marked cell
        :return: True if the game is over and the winner as his mark. If it's drawn game,
        second value will be '-'
        """
        cell_name = cell.name
        mark = cell.get_mark()
        horizontal = vertical = 0
        diagonal_right = diagonal_left = 0
        delta = cell_name[1] - cell_name[0]
        sum_index = cell_name[0] + cell_name[1]
        for index_1 in range(self.size):
            if self.cells[cell_name[0], index_1].get_mark() == mark:
                horizontal += 1
            else:
                horizontal = 0
            if self.cells[index_1, cell_name[1]].get_mark() == mark:
                vertical += 1
            else:
                vertical = 0
            if (0 <= index_1 + delta < self.size) and (
                    self.cells[index_1, index_1 + delta].get_mark() == mark):
                diagonal_right += 1
            else:
                diagonal_right = 0
            if (0 <= sum_index - index_1 < self.size) and (
                    self.cells[index_1, sum_index - index_1].get_mark() == mark):
                diagonal_left += 1
            else:
                diagonal_left = 0
            if max(horizontal, vertical, diagonal_right, diagonal_left) >= self.condition:
                logging.debug(' '.join(['Win!',
                                        'horizontal', str(horizontal),
                                        'vertical', str(vertical),
                                        'diagonal_right', str(diagonal_right),
                                        'diagonal_left', str(diagonal_left)]))
                return True, mark

        if self.filled_cells == len(self.cells):
            logging.debug(''.join(['Drawn game!']))
            return True, '-'
        return False, '-'

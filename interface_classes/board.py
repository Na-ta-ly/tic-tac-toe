from typing import Dict, Tuple
import logging
from math import ceil, floor
import pygame as pg

import config
from common_functions import tuple_verification, int_verification
from interface_classes.visual_object import VisualObject


class VisualBoard:
    """
    Class for visual board. Contains dictionary of calls {(cell index_1, cell index_2): VisualObject}.
            :param screen: pg.Surface, main screen object

    :prop size: the size of the board, as a number of cells on one side

    :method cells: Returns dictionary of cells {(cell index_1, cell index_2): VisualObject}
    :method draw_new_greed: Organizes the process of creation of a new board. Sets new size property,
        creates new set of cells and draws the greed
            :param greed_size: desirable number of elements on the one side of a new board
    """

    def __init__(self, screen: pg.Surface) -> None:
        self.__screen = screen
        self.__size = 0
        self.__cell_size = 0
        self.__field_size = (0, 0)  # size of the field without the menu (header) and the state bar (footer)
        self.__left_up_corner_coord = (0, 0)
        self.__relative_shift = (0, 0)  # coordinates of left upper corner of the board
        self.__cells = dict()

    def draw_new_greed(self, greed_size: int) -> None:
        """
        Organizes the process of creation of a new board. Sets new size property, creates new set of cells and
            draws the greed
        :param greed_size: desirable number of elements on the one side of a new board
        :return: None
        """
        self.__screen.fill(config.BACKGROUND)
        self.size = greed_size
        self._create_visual_board()

        shift = (self.__relative_shift[0] + self.__left_up_corner_coord[0],
                 self.__relative_shift[1] + self.__left_up_corner_coord[1])
        colour = config.GREEDCOLOUR
        if not tuple_verification(config.GREEDCOLOUR, 3, 255):
            logging.debug('Value GREEDCOLOUR in config.py is damaged. Using value (0, 0, 0)')
            colour = (0, 0, 0)
        for i in range(0, greed_size):
            horiz_line = self._get_line((shift[0], shift[1] + i * (self.__cell_size + config.line_thickness)),
                                        True)
            pg.draw.rect(self.__screen, colour, horiz_line)

            vert_line = self._get_line((shift[0] + i * (self.__cell_size + config.line_thickness), shift[1]))
            pg.draw.rect(self.__screen, colour, vert_line)
        last_horiz_line = self._get_line((shift[0], self.__field_size[0] - 2 * self.__relative_shift[0] + shift[1]
                                          + config.line_thickness), True)
        last_vert_line = self._get_line(
            (shift[0] + self.__field_size[0] - 2 * self.__relative_shift[0] + config.line_thickness,
             shift[1]))
        pg.draw.rect(self.__screen, colour, last_horiz_line)
        pg.draw.rect(self.__screen, colour, last_vert_line)

    def cells(self) -> Dict[Tuple[int, int], VisualObject]:
        """
        Getter for dictionary of cells of the current board
        :return: dictionary in format {(cell index_1, cell index_2): VisualObject}
        """
        return self.__cells

    def _get_centers(self) -> None:
        """
        Finds centers for cells on board and sets that values to cells objects
        :return: None
        """
        # --- Math part ___
        field_width, field_height = self.__field_size
        centers = []
        centers_line = []
        cell_number = min(field_width // self.__cell_size, field_height // self.__cell_size)
        shift = (self.__relative_shift[0] + self.__left_up_corner_coord[0] + config.line_thickness,
                 self.__relative_shift[1] + self.__left_up_corner_coord[1] + config.line_thickness)
        for index_1 in range(cell_number):
            for index_2 in range(cell_number):
                centers_line.append((shift[0] + (self.__cell_size + config.line_thickness)
                                     * index_2 + self.__cell_size // 2,
                                     shift[1] + (self.__cell_size + config.line_thickness)
                                     * index_1 + self.__cell_size // 2))
            centers.append(centers_line)
            centers_line = []

        # --- Values initialization ___
        for index in self.__cells.keys():
            self.__cells[index].rectangle.center = centers[index[0]][index[1]]

    def _create_visual_board(self) -> None:
        """
        Initializes visual board as a dictionary of cells and sets all cells in their centers
        :return: None
        """
        self.__cells = dict()
        for index_1 in range(self.__size):
            for index_2 in range(self.__size):
                name = index_1, index_2
                self.__cells[name] = VisualObject((self.__cell_size, self.__cell_size), colour=config.CELLCOLOUR)
        logging.debug('Visual cells were created')
        self._get_centers()

    def _get_line(self, position: Tuple[int, int], is_horiz: bool = False):
        """
        Gets coordinates for a line for the greed
        :param position: coordinates of a left upper corner of the line
        :param is_horiz: True for horizontal line
        :return: pg.Rect for the line
        """
        if int_verification(config.line_thickness):
            width = config.line_thickness
        else:
            width = 1
            logging.debug('Value line_thickness in config.py is damaged. Using value 1')
        height = self.__field_size[0] - 2 * self.__relative_shift[0] + config.line_thickness
        if is_horiz:
            width = self.__field_size[1] - 2 * self.__relative_shift[1] + config.line_thickness
            height = config.line_thickness
        line = pg.Rect(*position, width, height)
        return line

    @property
    def size(self) -> int:
        """
        Getter for size property
        :return: size: int, number of cells in one side of the board
        """
        return self.__size

    @size.setter
    def size(self, size: int) -> None:
        """
        Setter for the size property. If size is non-negative or not int, sets 0.
            Then initialize all other sizes of a board
        :param size: int, number of cells in one side of the board
         """
        self.__size = size if int_verification(size) else 0
        self._get_sizes()

    def _get_sizes(self) -> None:
        """
        Calculates base points for greed drawing and sets this values in instance. If size is not set yet,
            does nothing.
        """
        if self.__size == 0:
            logging.error(''.join(['The size of the board is not set yet']))
            return
        line_thickness = config.line_thickness
        header = ceil(self.__screen.get_height() * config.menu_height)

        height = floor((1 - config.footer_height - config.menu_height) * self.__screen.get_height())
        width = self.__screen.get_width()

        field_size = (width, height)

        left_up_field = (0, header)

        cell_width = ceil((field_size[0] - (self.__size - 2) * line_thickness) // self.__size)
        cell_height = ceil((field_size[1] - (self.__size - 2) * line_thickness) // self.__size)
        cell_size = (min(cell_width, cell_height))

        relative_shift = (ceil((field_size[0] - min(field_size[0], field_size[1])) // 2),
                          ceil((field_size[1] - min(field_size[0], field_size[1])) // 2))

        logging.debug(''.join(['cell_size: ', str(cell_size), ', ',
                               'field_size: ', str(field_size), ', ',
                               'left_up_field: ', str(left_up_field), ', ',
                               'relative_shift: ', str(relative_shift)]))
        self.__cell_size = cell_size if int_verification(cell_size) else 0
        self.__field_size = field_size if tuple_verification(field_size) else (0, 0)
        self.__left_up_corner_coord = left_up_field if tuple_verification(left_up_field) else (0, 0)
        self.__relative_shift = relative_shift if tuple_verification(relative_shift) else (0, 0)

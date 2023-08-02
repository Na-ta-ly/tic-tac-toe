import logging
from typing import List, Tuple
import pygame as pg

import config
from common_functions import tuple_verification
from interface_classes.state_bar import StateBar
from interface_classes.board import VisualBoard
from interface_classes.menu import Menu


class Interface:
    """
    Class for all interactive elements of the game interface
        :param screen: pg.Surface, main screen object
        :param button_names: list of names as strings
        :param board_size: size for a start game

    :prop state_bar: informational bar at the bottom of the screen
    :prop board: gaming board with all cells as dict {(cell index_1, cell index_2): VisualObject}
    :prop menu: main menu with all buttons as dict {'name': VisualObject}

    :method set_mark: Draws mark ('x' or 'o') in the given cell
    :method get_all_elements: Prepares elements of interface for drawing them on the screen
    """
    def __init__(self, screen: pg.Surface, button_names: List[str], board_size: int = 10) -> None:
        self.state_bar = StateBar(screen)

        self.board = VisualBoard(screen)
        self.board.draw_new_greed(board_size)

        self.menu = Menu(screen, button_names)

    def get_all_elements(self) -> List[Tuple[pg.Surface, pg.Rect]]:
        """
        Prepares elements of interface for drawing them on the screen
        :return: list of tuples (pg.Surface, pg.Rect)
        """
        data = [(self.state_bar.surface, self.state_bar.rectangle)]
        for item in list(self.menu.buttons.values()) + list(self.board.cells().values()):
            data.append((item.surface, item.rectangle))
        return data

    def set_mark(self, cell_name: Tuple[int, int], mark: str) -> None:
        """
        Draws mark ('x' or 'o') in the given cell. If given cell_name is not a tuple of 2 ints,
                does nothing
        :param cell_name: name of a cell as tuple (index_1, index_2)
        :param mark: 'x' or 'o'
        :return: None
        """
        if tuple_verification(cell_name, 2):
            cell = self.board.cells()[cell_name]
            cell_surface = cell.surface
            cell_size = cell_surface.get_height()

            mark_surface = pg.Surface((cell_size, cell_size))
            mark_surface.fill(config.CELLCOLOUR)

            if mark == 'o':
                pg.draw.circle(mark_surface, config.GREEDCOLOUR,
                               (int(cell_size / 2), int(cell_size / 2)),
                               cell_size / 2 * config.marks_size - config.line_thickness, config.line_thickness)
            elif mark == 'x':
                points = self._get_end_points(cell_size)
                pg.draw.polygon(mark_surface, config.GREEDCOLOUR, points[0])
                pg.draw.polygon(mark_surface, config.GREEDCOLOUR, points[1])
            cell_surface.blit(mark_surface, (0, 0))
        else:
            logging.error("Attempt to use value wrong cell name")

    @staticmethod
    def _get_end_points(cell_size: int) -> Tuple[
        Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]], Tuple[
            Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
        """
        Counts coordinates for 2 lines of 'x' mark
        :param cell_size: size of a cell in the game
        :return: tuple of coordinates for 2 lines, each has form for polygon objects
                (start_point_1, start_point_2, end_point_1, end_point_2)
        """
        relative_size = config.marks_size
        circle_radius = cell_size / 2 * relative_size
        line_thickness = round(config.line_thickness // 2)
        start_point_1 = (int(-round(circle_radius * 2 ** 0.5) + 2 * circle_radius + line_thickness),
                         int(-round(circle_radius * 2 ** 0.5) + 2 * circle_radius - line_thickness))
        start_point_2 = (int(-round(circle_radius * 2 ** 0.5) + 2 * circle_radius - line_thickness),
                         int(-round(circle_radius * 2 ** 0.5) + 2 * circle_radius + line_thickness))
        end_point_1 = (cell_size - start_point_1[0], cell_size - start_point_1[1])
        end_point_2 = (cell_size - start_point_2[0], cell_size - start_point_2[1])

        start_point_1_1 = (end_point_1[0], start_point_1[1])
        start_point_2_1 = (end_point_2[0], start_point_2[1])
        end_point_1_1 = (start_point_1[0], end_point_1[1])
        end_point_2_1 = (start_point_2[0], end_point_2[1])

        return (start_point_1, start_point_2, end_point_1, end_point_2), \
            (start_point_1_1, start_point_2_1, end_point_1_1, end_point_2_1)

import logging
from math import ceil, floor
import pygame as pg

import config
from interface_classes.visual_object import VisualObject


class StateBar:
    """
    VisualObject for showing information at the bottom of the screen.
        :param screen: pg.Surface, main screen object


    :method update_state_bar: Changes the text on the state bar
        :param state: text of message
    """
    def __init__(self, screen: pg.Surface) -> None:
        size = (screen.get_width(), floor(screen.get_height() * config.footer_height - config.line_thickness))
        self.__state_bar = VisualObject(size, (0, screen.get_rect().bottomleft[1] + 2 * config.line_thickness
                                               - ceil(screen.get_size()[1] * config.footer_height)),
                                        colour=config.BACKGROUND)

    @property
    def surface(self) -> pg.Surface:
        """
        Getter for the object itself
        :return: VisualObject of state bar
        """
        return self.__state_bar.surface

    @property
    def rectangle(self) -> pg.Rect:
        """
        Getter for the object itself
        :return: VisualObject of state bar
        """
        return self.__state_bar.rectangle

    def update_state_bar(self, state: str) -> None:
        """
        Changes the text on the state bar
        :param state: text of message
        :return: None
        """
        self.__state_bar.update_state(config.BACKGROUND, text=state, text_size=config.state_bar_font_size,
                                      text_alignment='lc')
        logging.debug(' '.join(['State bar was updated. Now its state', state]))

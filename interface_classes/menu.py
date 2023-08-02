import logging
from typing import Dict, List
from math import ceil
import pygame as pg

import config
from interface_classes.visual_object import VisualObject


class Menu:
    """
    Class for menu. Creates a dictionary of buttons {'name': VisualObject}
        :param screen: pg.Surface
        :param button_names: list of names for buttons

    :prop buttons: dictionary of buttons as VisualObjects {'name': VisualObject} (only for read)
    """
    def __init__(self, screen: pg.Surface, button_names: List[str]) -> None:
        border = 3
        height = ceil(screen.get_height() * config.menu_height)
        width = screen.get_width()
        size = (ceil((width - (border * (len(button_names) + 1))) / len(button_names)), height - 2 * border)
        logging.debug(' '.join(['Size of 1 button is', str(size)]))

        self.__buttons = dict()
        for index, name in enumerate(button_names):
            self.__buttons[name] = VisualObject(size, (ceil(border + index * (size[0] + border)), border),
                                                colour=config.BUTTONCOLOUR,
                                                text=name, text_size=config.menu_font_size, text_alignment='c'
                                                )

    @property
    def buttons(self) -> Dict[str, VisualObject]:
        """
        Getter for menu buttons
        :return:
        """
        return self.__buttons

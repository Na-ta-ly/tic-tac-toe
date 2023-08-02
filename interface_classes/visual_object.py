from abc import ABC
from typing import Optional, Tuple
import logging
from math import ceil
import config
import pygame as pg
from common_functions import tuple_verification, int_verification


class VisualObject:
    """
    Basic class for all interactive visual elements.
    For control via pygame, has pg.Surface and pg.Rect. For init can take:
        :param size: element size (obligatory)
        :param position: coordinates for the left upper corner of the element (optional)
        :param text: caption for the button (optional)
        :param text_size: font size for a caption on the element (optional)
        :param text_alignment: string of desirable alignment of the capture (optional):
                    'c' - centered
                    'lc' - left, centered on height
                    If parameter is inappropriate sets centered
        :param colour: colour for the element (optional)


    :prop rectangle: pg.Rect, corresponding this element.
            Needed for control of its position

    :prop surface: pg.Surface, corresponding this element.
            Needed for control of its content and embedding it in the main screen.

    :method update_state: Refreshes the element if its general features changed
        :param colour: colour for element, tuple (R, G, B) (obligatory)
        :param position: position of the left upper corner of the element
        :param text: caption, that should be written on the element
        :param text_size: font size for the caption
        :param text_alignment: string of desirable alignment of the capture:
                'c' - centered
                'lc' - left, centered on height
                If parameter is inappropriate sets centered
    """

    def __init__(self, size: Tuple[int, int], position: Optional[Tuple[int, int]] = None,
                 colour: Optional[Tuple[int, int, int]] = None,
                 text: Optional[str] = None, text_size: Optional[int] = None,
                 text_alignment: Optional[str] = None):
        self.surface, self.rectangle = self._get_new_element(size)
        self.update_state(colour=colour, position=position, text=text, text_size=text_size,
                          text_alignment=text_alignment)

    @staticmethod
    def _get_new_element(size: Tuple[int, int]) -> Tuple[pg.Surface, pg.Rect]:
        """
        Generates a visual element. If size looks wrong, raises ValueError
        :param size: element size
        :return: tuple (surface, rectangle)
        """
        if not tuple_verification(size, 2):
            logging.error(' '.join(['Attempt to use value', str(size), 'as size for visual element']))
            raise ValueError('size value must be a tuple of 2 non-negative integers')
        surface = pg.Surface(size)
        rectangle = surface.get_rect()
        return surface, rectangle

    def update_state(self, colour: Tuple[int, int, int], position: Optional[Tuple[int, int]] = None,
                     text: Optional[str] = None, text_size: Optional[int] = None,
                     text_alignment: Optional[str] = None) -> None:
        """
        Refreshes the element if its general features changed
        :param colour: colour for element, tuple (R, G, B)
        :param position: position of the left upper corner of the element
        :param text: caption, that should be written on the element
        :param text_size: font size for the caption
        :param text_alignment: string of desirable alignment of the capture:
                'c' - centered
                'lc' - left, centered on height
                If parameter is inappropriate sets centered
        """
        self._set_colour(colour)
        self._set_position(position)
        self._set_capture(text, text_size, text_alignment)

    def _set_colour(self, colour: Tuple[int, int, int]) -> None:
        """
        Sets colour for the object's surface. Previously checking it, if it has a (R, G, B) format,
                otherwise raises ValueError
        :param colour: a tuple in (R, G, B) format
        :return: None
        """
        if colour is None or not tuple_verification(colour, 3, 255):
            logging.debug(' '.join(['Attempt to use value inappropriate value as a colour for visual',
                                    'element. Colour will be replaced to default BACKGROUND from config']))
            if not tuple_verification(config.BACKGROUND, 3, 255):
                logging.error(' '.join(['Attempt to use value', str(config.BACKGROUND),
                                        'as a colour for visual element']))
                raise ValueError('colour value must be a tuple of 3 non-negative integers not greater than 255')
            colour = config.BACKGROUND
        self.surface.fill(colour)

    def _set_position(self, position: Tuple[int, int]) -> None:
        """
        Sets position for a given pg.Rect object. Before it checks, if a position has an appropriate format,
                otherwise raises ValueError
        :param position: a tuple of 2 integers
        :return: None
        """
        if position is not None:
            if not tuple_verification(position, 2):
                logging.error(' '.join(['Attempt to use value', str(position),
                                        'as position for visual element']))
                raise ValueError('position value must be a tuple of 2 non-negative integers')
            self.rectangle.topleft = position

    def _set_capture(self, text: Optional[str], text_size: Optional[int],
                     text_alignment: Optional[str]) -> None:
        """
        Draws a capture on a Visual object. Before checks if all values are suitable.
                If colour is unsuitable, tries to use config.TEXTCOLOUR. If with that value problem,
                raises ValueError.
                If no text_size was given, uses 20. If given text_size value is not a non-negative integer,
                raises ValueError.
        :param text: caption for the button
        :param text_size: font size for a caption on the element
        :param text_alignment: string of desirable alignment of the capture:
                'c' - centered
                'lc' - left, centered on height
                If parameter is inappropriate sets centered
        :return: None
        """
        if text is not None:
            if text_size is None:
                text_size = 20
                logging.debug(' '.join(['No value for text_size was given. Set to 20']))
            if not int_verification(text_size) or not tuple_verification(config.TEXTCOLOUR, 3, 255):
                logging.error(' '.join(['Attempt to use values', str(config.TEXTCOLOUR), 'and',
                                        str(text_size), 'as a colour and font size for visual element']))
                raise ValueError('text_size value must be a non-negative integer or TEXTCOLOUR in config.py is broken')
            size = self.surface.get_size()
            font = pg.font.SysFont("monospace", text_size)
            caption = font.render(text, True, config.TEXTCOLOUR)
            caption_size = caption.get_size()
            if text_alignment == 'lc':
                shift = (10, ceil((size[1] - caption_size[1]) / 2))
            else:
                shift = ((size[0] - caption_size[0]) / 2, (size[1] - caption_size[1]) / 2)
            self.surface.blit(caption, shift)

    @property
    def rectangle(self) -> pg.Rect:
        """
        Getter for rectangle property
        :return: rectangle for the VisualObject
        """
        return self.__rectangle

    @rectangle.setter
    def rectangle(self, rect: pg.Rect) -> None:
        """
        Setter for rectangle property, raises ValueError, if given
                rect value is not pg.Rect
        :param rect: rectangle for the VisualObject
        :return: None
        """
        if type(rect) != pg.Rect:
            logging.error(' '.join(['Attempt to set', str(type(rect)),
                                    'as a rectangle property for', str(self.__class__),
                                    'object']))
            raise ValueError('Rectangle property should be only a pg.Rect values')
        self.__rectangle = rect

    @property
    def surface(self) -> pg.Surface:
        """
        Getter for surface property
        :return: surface for the VisualObject
        """
        return self.__surface

    @surface.setter
    def surface(self, surface: pg.Surface) -> None:
        """
        Setter for surface property, raises ValueError, if given
                surface value is not pg.Surface
        :param surface: surface for the VisualObject
        :return: None
        """
        if type(surface) != pg.Surface:
            logging.error(' '.join(['Attempt to set', str(type(surface)),
                                    'as a rectangle property for', str(self.__class__),
                                    'object']))
            raise ValueError('Rectangle property should be only a pg.Surface values')
        self.__surface = surface

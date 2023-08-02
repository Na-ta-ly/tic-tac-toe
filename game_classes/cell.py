import logging
from typing import TypeVar, Tuple

mark_type = TypeVar('mark_type', str, None)


class Cell:
    """
    Class for a single cell.
        :param name: name for a new cell tuple(index_1, index_2)

    :prop name: cell name, tuple(index_1, index_2)

    :method set_mark: sets a mark (str) in the empty cell, or None for empty.
            If try to set a new mark in not empty cell, then returns False

    :method get_mark: returns mark, placed into cell; or ' ' if the cell is empty
    """

    def __init__(self, name: Tuple[int, int]) -> None:
        self.name = name
        self.set_mark(None)

    @property
    def name(self) -> Tuple[int, int]:
        """
        Getter for name property
        :return: name of a cell as Tuple[int, int]
        """
        return self.__name

    @name.setter
    def name(self, name: Tuple[int, int]) -> None:
        """
        Setter for name property, raises ValueError, if name has inappropriate value
        :param name: name of a cell as Tuple[int, int]
        :return: None
        """
        for item in name:
            if type(item) != int or len(name) != 2 or type(name) != tuple:
                logging.error(' '.join(['Attempt to set', str(name),
                                        'as a cell name']))
                raise ValueError('Cell name should be a tuple with 2 int values')
        self.__name = name

    def set_mark(self, mark: mark_type) -> bool:
        """
        Setter for mark property
        :param mark: mark, that will be set
        :return: True, if mark was set successfully
        """
        if mark is None or self.get_mark() == ' ':  # None for init
            self.__mark = mark
            if mark is not None:
                logging.info(' '.join(['Mark', self.get_mark(), 'set in cell', str(self.name)]))
            return True
        else:
            logging.info(' '.join(['In cell', str(self.name),
                                   'there is already', self.get_mark()]))
            return False

    def get_mark(self) -> str:
        """
        Getter for mark property
        :return: mark, ' ' if there's no mark yet
        """
        if self.__mark is None:
            return ' '
        else:
            return self.__mark

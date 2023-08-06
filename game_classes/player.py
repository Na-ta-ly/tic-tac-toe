import logging

from game_classes.cell import Cell


class Player:
    """
    Class for a player
        :param name: name for a new player

    :prop name: player's name
    :prop mark: mark assigned to the player

    :method put_mark: sets player's mark in the given cell
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.mark = None

    @property
    def name(self) -> str:
        """
        Getter for property name
        :return: player's name
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Setter for property name, if name is not str, raises ValueError
        :param name: player's name
        """
        if type(name) != str:
            logging.error(' '.join(['Attempt to set', str(type(name)),
                                    "as a player's name"]))
            raise ValueError("Name must be a str value")
        self.__name = name

    # def put_mark(self, cell: Cell) -> bool:
    #     """
    #     Assigns player's mark to the cell
    #     :param cell: cell, chosen by player
    #     :return: True, if mark is set successfully
    #     """
    #     return cell.set_mark(self.mark)

    @property
    def mark(self) -> str:
        """
        Getter for mark property of Player class
        :return: mark, assigned to the player
        """
        return self.__mark

    @mark.setter
    def mark(self, mark: str) -> None:
        """
        Setter for the mark property, if mark is not str, raises ValueError
        :param mark: mark, that will be assigned to the player
        :return: None
        """
        if type(mark) != str and mark is not None:
            logging.error(' '.join(['Attempt to set', str(type(mark)),
                                    "as a player's mark"]))
            raise ValueError("Mark must be a str value")
        self.__mark = mark

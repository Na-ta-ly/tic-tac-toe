import logging
import random
from typing import List, Tuple

from game_classes.board import Board
from game_classes.player import Player


class Game:
    """
    Class for a game
        :param players: list of players for a new game

    :prop board: a board, assigned to the game
    :prop state: current state [0 - the game can continue,
                1 - if there is a win combination on the board and game is stopped]
    :prop curr_turn: index of a player, whose makes a move now
    :prop players: list of players for the game

    :method create_board: creates a new board of given size
    :method single_turn: checks if the cell is empty and makes a move by given player
    :method start_game: creates new board, zeroes game state, randomly assigns marks
                to players and returns index of a first one
    """

    def __init__(self, players: List[Player]) -> None:
        self.board = None
        self.state = 0
        self.players = players
        self.curr_turn = None

    @property
    def board(self) -> Board:
        """
        Getter for board property
        :return: Board object
        """
        return self.__board

    @board.setter
    def board(self, board: Board) -> None:
        """
        Setter for board property
        :param board: Board object
        :return: None
        """
        self.__board = board

    @property
    def state(self) -> int:
        """
        Getter for state property
        :return: int [0 - the game can continue,
                1 - end of the game state]
        """
        return self.__state

    @state.setter
    def state(self, state: int) -> None:
        """
        Setter for state property, if state is inappropriate raises ValueError
        :param state: game state [0 - the game can continue,
                1 - end of the game state]
        """
        if state not in (1, 0):
            logging.debug(' '.join(['Attempt to set', str(state), 'value to game.state']))
            raise ValueError('Game state must be 1 or 0')
        self.__state = state

    @property
    def players(self) -> List[Player]:
        """
        Getter for players property
        :return: players list
        """
        return self.__players

    @players.setter
    def players(self, players: List[Player]) -> None:
        """
        Setter for players property
        :param players: list of players
        :return: None
        """
        if len(players) != 2:
            logging.error(' '.join(['Attempt to create game for', str(len(players)),
                                    'players']))
            raise ValueError('Game can be created only for 2 players')
        for item in players:
            if type(item) != Player:
                logging.error(' '.join(['List of players contains', str(type(item)),
                                        'type']))
                raise ValueError('Players list should contain only values of Player class')
        self.__players = players

    @property
    def curr_turn(self) -> int:
        """
        Getter for current_turn property
        :return: index of a player, whose turn is now
        """
        return self.__curr_turn

    @curr_turn.setter
    def curr_turn(self, curr_turn: int) -> None:
        """
        Setter for current_turn property, raises ValueError if curr_turn not in players' indexes
        :param curr_turn: index of a player, whose turn is now
        """
        if curr_turn not in range(2) and curr_turn is not None:
            logging.error(' '.join(['Given player index', str(curr_turn),
                                    'is not in range of players indexes']))
            raise ValueError('Index of next player is not in players list')
        self.__curr_turn = curr_turn

    def create_board(self, size: int = 0, condition: int = 0) -> None:
        """
        Creates new board, if size is smaller than condition, condition = size
        :param size: size of a new board
        :param condition: max sequence of elements for win
        :return: None
        """
        if condition < size:
            self.board = Board(size, condition)
        else:
            condition = size
            self.board = Board(size, size)
        logging.debug(''.join(['Created new board ', str(size), 'x', str(size),
                               ' with win condition ', str(condition)]))

    def single_turn(self, player: Player, cell_name: Tuple[int, int]) -> bool:
        """
        If cell is empty sets mark
        :param player: player, who makes his move
        :param cell_name: tuple of indexes
        :return: True if mark was set successfully
        """
        cell = self.board.cells.get(cell_name, 0)
        if cell != 0 and cell.get_mark() == ' ':
            player.put_mark(cell)
            self.board.filled_cells += 1
            logging.debug(' '.join([player.name, 'marked', str(cell_name)]))
            return True
        logging.debug(''.join([player.name, ' wanted to mark ', str(cell_name),
                               ", but the cell isn't empty"]))
        return False

    def start_game(self, size: int, condition: int) -> int:
        """
        Creates new game and chooses a player, who first makes a move
        :param size: size of a new board
        :param condition: max sequence of elements for win
        :return: first player index
        """
        self.create_board(size, condition)
        self.state = 0
        first_player = random.randint(0, 1)
        self.players[first_player].mark = 'x'
        self.players[1 - first_player].mark = 'o'
        current_player_index = first_player
        return current_player_index

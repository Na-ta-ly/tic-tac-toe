import logging
from typing import Tuple, List

import arcade
import arcade.gui

import config
from common_functions import tuple_verification

from game_classes.player import Player
from game_classes.game import Game


class Interface(arcade.Window):
    """
    Main interface class.
    """
    def __init__(self, game_name: str) -> None:
        """
        Creates main interface for a game window
        :param game_name: name for window
        :return: None
        """
        # ------ All constants set
        self.click = arcade.load_sound("images/rockHit2.wav")
        self.colours = dict()
        self._all_config_values_verification()

        # ------ Main window
        super().__init__(config.screen_dim[0], config.screen_dim[1], game_name)
        arcade.set_background_color(self.colours['back'])

        # ------ Game
        player_1 = Player('Player 1')
        player_2 = Player('Player 2')
        self.game = Game([player_1, player_2])

        # ------ Status bar
        self.state_bar = arcade.Text('Board created', 5, 5, self.colours['text'])

        # ------ Playing field
        # Playing field constant properties
        self.cell_margin = config.line_thickness
        height = int((1 - config.footer_height - config.menu_height) * config.screen_dim[1])
        width = config.screen_dim[0]
        self.field_size = min(width, height)
        self.bottom_left_board = (round(config.screen_dim[0] / 2 - self.field_size / 2),
                                  round(config.screen_dim[1] / 2 - self.field_size / 2))

        # Playing field chainable properties
        self.grid_sprite_list = arcade.SpriteList()  # for cells drawing
        self.grid_sprites = []  # for cells changing
        self.board_sprites = arcade.SpriteList()  # just cells background
        self.grid_size = 0
        self.cell_side = 0

        # ------ Main menu
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.buttons = arcade.gui.UIBoxLayout(vertical=False)

        button_width = config.button_width
        button_space = config.button_space

        small_game_button = arcade.gui.UIFlatButton(text=config.BUTTONS_NAMES[0], width=button_width,
                                                    style=config.style)
        big_game_button = arcade.gui.UIFlatButton(text=config.BUTTONS_NAMES[1], width=button_width,
                                                  style=config.style)
        quit_button = arcade.gui.UIFlatButton(text=config.BUTTONS_NAMES[2], width=button_width,
                                              style=config.style)

        self.buttons.add(small_game_button.with_space_around(left=button_space, right=button_space))
        self.buttons.add(big_game_button.with_space_around(left=button_space, right=button_space))
        self.buttons.add(quit_button.with_space_around(left=button_space, right=button_space))

        @small_game_button.event("on_click")
        def on_click_small_game(event):
            logging.debug(' '.join(['Pressed small_game button']))
            self.setup(config.small_game_size)
            self.game.curr_turn = self.game.start_game(config.small_game_size, 3)
            self.state_bar.text = 'Small game started. Now turn of {name}'.format(
                name=self.game.players[self.game.curr_turn].name)

        @big_game_button.event("on_click")
        def on_click_big_game(event):
            logging.debug(' '.join(['Pressed big_game button']))
            self.setup(config.big_game_size)
            self.game.curr_turn = self.game.start_game(config.big_game_size, 5)
            self.state_bar.text = 'Big game started. Now turn of {name}'.format(
                name=self.game.players[self.game.curr_turn].name)

        @quit_button.event("on_click")
        def on_click_quit(event):
            logging.debug(' '.join(['Pressed quit_game button']))
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=-5,
                child=self.buttons)
        )

    def setup(self, game_size: int, condition: int = 5) -> None:
        """
        Set up the game here. Call this function to restart the game.
        :param game_size: size of the game
        :param condition: win combination
        :return: None
        """
        # ------ Game start section
        self.game.curr_turn = self.game.start_game(game_size, condition)

        # ------ Interface section
        self.grid_size = game_size
        self.grid_sprite_list, self.grid_sprites, self.board_sprites = self.draw_new_board()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        Mouse click event (not in main menu)
        :return: None
        """
        arcade.play_sound(self.click)

        column = int((x - self.bottom_left_board[0]) // (self.cell_side + self.cell_margin))
        row = int((y - self.bottom_left_board[1]) // (self.cell_side + self.cell_margin))
        raw_cell_name = (row, column)
        cell_name = self._cell_name_convert(raw_cell_name)

        if row >= self.grid_size or column >= self.grid_size:
            logging.debug(' '.join([f'Click coordinates: ({x}, {y}). Out of grid']))
            return

        if self.game.state != 1:  # if game is not over yet
            if self.game.single_turn(self.game.players[self.game.curr_turn], cell_name):

                logging.debug(
                    ' '.join([f'Click coordinates: ({x}, {y}). Grid coordinates: ({cell_name[0]}, {cell_name[1]})']))
                self.game.curr_turn = 1 - self.game.curr_turn
                self.state_bar.text = 'Now turn of {name}'.format(name=self.game.players[self.game.curr_turn].name)

                # HERE NEED RAW_CELL_NAME!!!
                self._set_mark(raw_cell_name, self.game.players[self.game.curr_turn].mark)

                result_check = self.game.board.check_win_combo(self.game.board.cells[cell_name])
                if result_check[0]:
                    self.game.state = 1
                    winner = result_check[1]
                    if winner == '-':
                        tail = 'Drawn game!'
                    else:
                        tail = 'Win of {name}!'.format(name=self.game.players[1 - self.game.curr_turn].name)
                    self.state_bar.text = ' '.join(['Game is over.', tail])

    def on_draw(self) -> None:
        """
        Render the screen.
        :return: None
        """
        self.clear()
        self.state_bar.draw()
        self.manager.draw()

        self.board_sprites.draw()
        self.grid_sprite_list.draw()

    def _cell_name_convert(self, name: Tuple[int, int]) -> Tuple[int, int]:
        """
        Converts cell coordinates from bottom left corner to upper left
        :param name: coordinates of cell
        :return: coordinates from upper left
        """
        return self.grid_size - name[0] - 1, name[1]

    def _set_mark(self, cell: Tuple[int, int], mark: str) -> None:
        """
        Changes texture of the sprite, given by its address
        :param cell: address of the sprite in grid_sprites list
        :param mark: string with mark. If it's 'o', sets texture 0,
            else - texture 1
        :return: None
        """
        row, column = cell
        if mark == 'o':
            self.grid_sprites[row][column].set_texture(0)
        else:
            self.grid_sprites[row][column].set_texture(1)

    def draw_new_board(self) -> Tuple[arcade.SpriteList, List[List[arcade.Sprite]], arcade.SpriteList]:
        """
        Generates sprite lists for a new board
        :return: grid_sprite_list, grid_sprites, board_sprites
        """
        grid_sprite_list = arcade.SpriteList()
        grid_sprites = []
        board_sprites = arcade.SpriteList()

        self.cell_side = round((self.field_size - (self.grid_size + 2) * self.cell_margin) // self.grid_size)

        x_text = arcade.load_texture(config.x_pic, can_cache=True)
        o_text = arcade.load_texture(config.o_pic, can_cache=True)
        scale = self.cell_side / max(x_text.size)

        # for grid
        base_size = (self.grid_size + 2) * self.cell_margin + self.grid_size * self.cell_side
        board_sprites.append(arcade.Sprite(center_x=round(self.bottom_left_board[0] + base_size / 2),
                                           center_y=round(self.bottom_left_board[1] + base_size / 2),
                                           texture=arcade.Texture.create_filled('grid_background',
                                                                                (base_size,
                                                                                 base_size),
                                                                                self.colours['grid'])))

        for row in range(self.grid_size):
            grid_sprites.append([])
            for column in range(self.grid_size):
                x = (column * (self.cell_side + self.cell_margin) + (self.cell_side / 2 + self.cell_margin)
                     + self.bottom_left_board[0] + self.cell_margin)
                y = (row * (self.cell_side + self.cell_margin) + (self.cell_side / 2 + self.cell_margin)
                     + self.bottom_left_board[1] + self.cell_margin)
                sprite = arcade.Sprite(image_x=max(x_text.size),
                                       image_y=max(x_text.size),
                                       scale=scale,
                                       texture=arcade.Texture.create_empty('empty',
                                                                           (max(x_text.size), max(x_text.size))))
                sprite.append_texture(x_text)
                sprite.append_texture(o_text)
                sprite.center_x = x
                sprite.center_y = y
                grid_sprite_list.append(sprite)
                grid_sprites[row].append(sprite)

                # for cells background
                board_sprites.append(arcade.Sprite(image_x=max(x_text.size),
                                                   image_y=max(x_text.size),
                                                   scale=scale,
                                                   center_x=x,
                                                   center_y=y,
                                                   texture=arcade.Texture.create_filled('cell_background',
                                                                                        (max(x_text.size),
                                                                                         max(x_text.size)),
                                                                                        self.colours['cell'])))
        return grid_sprite_list, grid_sprites, board_sprites

    def _all_config_values_verification(self):
        """

        :return:
        """
        default_values = {config.GRIDCOLOUR: {'name': 'GRIDCOLOUR',
                                              'default': (0, 0, 0),
                                              'small_name': 'grid'},
                          config.TEXTCOLOUR: {'name': 'TEXTCOLOUR',
                                              'default': (0, 0, 0),
                                              'small_name': 'text'},
                          config.CELLCOLOUR: {'name': 'CELLCOLOUR',
                                              'default': (220, 220, 220),
                                              'small_name': 'cell'},
                          config.BACKGROUND: {'name': 'BACKGROUND',
                                              'default': (),
                                              'small_name': 'back'},
                          config.BUTTONCOLOUR: {'name': 'BUTTONCOLOUR',
                                                'default': (180, 180, 180),
                                                'small_name': 'button'},
                          }
        for colour in default_values.keys():
            if not tuple_verification(colour, 3, 255):
                colour = default_values[colour]['default']
                logging.debug(f"Value {default_values[colour]['name']} in config.py is damaged. Using value ()")
            self.colours[default_values[colour]['small_name']] = colour

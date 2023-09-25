import logging
import arcade
from interface_classes.interface import Interface


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
        level=logging.INFO
    )

    interface = Interface("Tic-Tac-Toe")
    interface.setup(10)
    arcade.run()

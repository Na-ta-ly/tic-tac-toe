import logging
from typing import Optional


def tuple_verification(value: tuple, length: int = 2, max_value: Optional[int] = None) -> bool:
    """
    Returns True if the value is a tuple of pointed number of ints. Also, can be checked,
        if all int are not greater than max value
    :param value: tuple for check
    :param length: number of int, that needs to be in the tuple
    :param max_value: max value for each component
    :return: True if the value is a tuple (int, int)
    """
    flag = True
    if not isinstance(value, tuple) or len(value) != length:
        flag = False
    for item in value:
        if not int_verification(item, max_value):
            flag = False
    if not flag:
        logging.error(' '.join(['Attempt to use value', str(value),
                                'as tuple of', str(length), 'ints']))
    return flag


def int_verification(value: int, max_value: Optional[int] = None) -> bool:
    """
    Returns True if the value is a non-negative int.  Also, can be checked,
        if given value is not greater than max value
    :param value: int value for test
    :param max_value: max value for check
    :return: True if the value is a non-negative integer
    """
    flag = True
    tail = ''
    if not isinstance(value, int) or value < 0:
        flag = False
    if max_value is not None and value > max_value:
        flag = False
        tail = ' '.join(['with max value', str(max_value)])
    if not flag:
        logging.error(' '.join(['Attempt to use value', str(value), 'as positive int', tail]))
    return flag

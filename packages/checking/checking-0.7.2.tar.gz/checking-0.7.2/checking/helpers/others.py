import glob
from typing import Any
from datetime import datetime


def short(obj: Any, width: int = 45) -> str:
    """
    Reduces the string representation to a specific length, replacing all characters after the specified length with
    three dots ([...]) plus symbols count to end.
    If the string representation is shorter than the specified length, it returns it unchanged.
    :param obj: String or object[Any]
    :param width: Maximum string representation length
    :return: shortened string
    """
    str_ = str(obj)
    len_ = len(str_) - width
    if len_ > 0:
        return str_[:width] + f'[...+{len_}]'
    return str_


def print_splitter_line():
    """
    Displays a dash separator in the form of a 10 dash (for separating test results)
    :return: None
    """
    print('-' * 10)


def is_file_exists(file_name: str) -> bool:
    """
    Tells, if the file with name exists
    :return: True, if the file exists
    """
    return len(glob.glob(file_name)) == 1


def str_date_time():
    """
    Generates current date and time for using at file names
    :return: str like 2020-02-22_12_58_58
    """
    return datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')


def fake(*args):
    """
    Stub function that does nothing
    :param args: ignored params
    :return: None
    """
    pass


def format_seconds(seconds: float) -> str:
    """
    Creates string representation of seconds count, which format it to hours and/or minutes if possible
    :param seconds: amount of seconds
    :return: str
    """
    if not seconds // 60:
        return f'{seconds:.2f} seconds'
    hours = ''
    if seconds // 3600:
        hours = f'{int(seconds // 3600)} hour(s) '
        seconds = seconds - ((seconds // 3600) * 3600)
    minutes = int(seconds // 60)
    seconds = seconds - minutes * 60
    return f'{hours}{minutes} minute(s) and {seconds:.2f} seconds'


if __name__ == '__main__':
    print(format_seconds(4135))

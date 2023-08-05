import time
import re


class Flag:
    def __init__(self, name, func, cmd: str) -> None:
        self.name = name
        self.cmd: str = cmd
        self.func = func
        self.re: str = get_regular(cmd)
        self.args: list = get_args(self.cmd)
        self.doc = func.__doc__

    def run(self, *args) -> None:
        self.func(*args)


def get_args(cmd: str) -> list:
    found_args = re.findall('<\\w+:\\w+>', cmd)
    args_list = [(re.findall('<\\w+:', arg)[0][1:-1],
                  re.findall(':\\w+>', arg)[0][1:-1])
                  for arg in found_args if found_args]

    return args_list


def get_regular(cmd: str) -> str:
    found_args = re.findall('<\\w+:\\w+>', cmd)

    for arg in found_args:
        cmd = cmd.replace(arg, '\\w+')

    return cmd


def await_(logger, second) -> None:
    """Set the waiting time before starting"""

    color = 'cyan'
    msg = f'The command from the case will be launched {second} second'
    logger.info(msg, color=color)

    time.sleep(second)
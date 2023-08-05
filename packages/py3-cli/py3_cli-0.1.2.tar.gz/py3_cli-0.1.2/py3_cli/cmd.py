import re

from .error import CmdError, TypeArgumentError

types: list = ['int', 'float', 'str', 'bytes', 'bool']


class Cmd:
    def __init__(self, func, cmd_func: str, color: str = 'white',
                 prefix: str = 'INFO', debug: bool = False) -> None:
        self.cmd_func: str = cmd_func
        self.prefix: str = prefix
        self.color: str = color
        self.debug: bool = debug
        self.func = func

        self.cmd_args_inline: list = get_args_inline(self.cmd_func)
        self.cmd_args: list = get_args(self.cmd_func)
        self.cmd_re: str = get_regular(self.cmd_func)
        self.doc: str = func.__doc__
        try:
            self.name: str = func.__name__
        except AttributeError:
            msg: str = 'Only one command can be assigned to a single function'
            raise CmdError(msg)

    def run(self, **kwargs):
        return self.func(**kwargs)


def get_regular(cmd_func: str) -> str:
    """Получение регулярного выражения команды"""

    found_args: list = re.findall('<\\w+:\\w+>', cmd_func)
    found_args_inline: list = re.findall('<\\w+:\\w+:\\w+>', cmd_func)

    for arg in found_args:
        cmd_func: str = cmd_func.replace(arg, '\\w+')

    for arg in found_args_inline:
        cmd_func: str = cmd_func.replace(' ' + arg, '')

    return cmd_func


def get_args(cmd_func: str) -> list:
    """Получение аргументов команды"""

    found_args_inline: list = re.findall('<\\w+:\\w+:\\w+>', cmd_func)
    for arg in found_args_inline:
        cmd_func: str = cmd_func.replace(f' {arg}', '')

    cmd: list = cmd_func.split()
    found_args: list = re.findall('<\\w+:\\w+>', cmd_func)
    args_list: list = [(re.findall('<\\w+:', arg)[0][1:-1],
                        re.findall(':\\w+>', arg)[0][1:-1] if re.findall(':\\w+>', arg)[0][1:-1] in types else type_error(),
                        cmd.index(arg)) for arg in found_args if found_args]
    return args_list


def type_error() -> None:
    msg: str = 'Invalid argument type'
    raise TypeArgumentError(msg)

def get_args_inline(cmd_func: str) -> list:
    """Получение inline аргументов команды"""

    found_args: list = re.findall('<\\w+:\\w+:inline>', cmd_func)
    args_list: list = [(re.findall('<\\w+:', arg)[0][1:-1],
                        re.findall(':\\w+:', arg)[0][1:-1] if re.findall(':\\w+:', arg)[0][1:-1] in types else type_error(),
                        'inline') for arg in found_args if found_args]

    return args_list

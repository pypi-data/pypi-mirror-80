import datetime

from termcolor import colored

from .flag import Flag, await_
from .handler import Handler
from .error import CmdError
from .cmd import Cmd


class CLI:
    def __init__(self) -> None:
        self.__cmd_list_name: list = ['help', 'exit', 'clear' 'quit', 'flags', 'colors', 'copyright', 'version',
                                      'case create <name:str>', 'case run <name:str>', 'case list',
                                      'case end']  # Список стандартых команд для проверки
        self.__msg_input: colored = colored('$', 'blue')  # Текст для ввода
        self.__cmd_list_for_check: list = []  # Список команд для проверки
        self.__case_list_create: list = []  # Список кейсов для создаания при запуске
        self.__flag_list: list = []  # Список флагов
        self.__cmd_list: list = []  # Список команд (экземпляров класса CMD)
        self.__last_cmd: str = ''  # Последняя команла
        self.config = Config()  # Настройки
        self.__Handler = None  # Обработчик
        self.Logger = None  # Логгер

    def cmd(self, command: str, color: str = 'white',
            prefix: str = 'INFO', debug: bool = False):
        def wrapper(func):
            if command in self.__cmd_list_name:
                msg: str = 'This command belongs to the list of standard commands'
                raise CmdError(msg)
            else:
                cmd: Cmd = Cmd(func, command, color, prefix, debug)
                if self.config.debug and debug:
                    if command in self.__cmd_list_for_check:
                        msg: str = 'The command already exists'
                        raise CmdError(msg)
                    else:
                        self.__cmd_list_for_check.append(command)
                        self.__cmd_list.append(cmd)
                elif not self.config.debug and not debug:
                    if command in self.__cmd_list_for_check:
                        msg: str = f'The command {command} already exists'
                        raise CmdError(msg)
                    else:
                        self.__cmd_list_for_check.append(command)
                        self.__cmd_list.append(cmd)
        return wrapper

    def run(self) -> None:
        self.Logger: Logger = Logger(self.config.time)
        self.__Handler: Handler = Handler(self.__cmd_list, self.__cmd_list_for_check, self.__flag_list, self.config.full_log, self.config.printlog,
                                          self.config.time, self.config.copyright, self.Logger)

        self.__Handler.clear()
        self.__case_create()
        self.__cmd_create()
        self.__flag_create()

        if self.config.preRun:
            self.config.preRun()

        if self.config.copyright:
            print(self.config.copyright if self.config.copyright else 'Copyright is empty', end='\n\n')

        while True:
            command: str = input(self.__msg_input)

            if command:
                self.__Handler.handle(command, self.config.preCmd, self.config.postCmd)
                self.__last_cmd: str = command

    def __cmd_create(self) -> None:
        cmd_standart: dict = {
            'help': {
                'func': self.__Handler.help,
                'command': 'help'},
            'exit': {
                'func': self.__Handler.exit,
                'command': 'exit'},
            'clear': {
                'func': self.__Handler.clear,
                'command': 'clear'},
            'quit': {
                'func': self.__Handler.quit,
                'command': 'quit'},
            'flags': {
                'func': self.__Handler.flags,
                'command': 'flags'},
            'colors': {
                'func': self.__Handler.color,
                'command': 'colors'},
            'copyright': {
                'func': self.__Handler.copyright,
                'command': 'copyright'},
            'version': {
                'func': self.__Handler.version,
                'command': 'version'},
            'case create': {
                'func': self.__Handler.case_create,
                'command': 'case create <name:str>'},
            'case run': {
                'func': self.__Handler.case_run,
                'command': 'case run <name:str>'},
            'case list': {
                'func': self.__Handler.case_list,
                'command': 'case list'}
        }

        for cmd in cmd_standart:
            if cmd not in self.config.turnOffCommand:
                command: Cmd = Cmd(cmd_standart[cmd]['func'], cmd_standart[cmd]['command'])
                self.__cmd_list.append(command)

    def __flag_create(self) -> None:
        flag_standart: dict = {
            'await': {
                'func': await_,
                'command': '--await:<second:int>',
                'name': 'await'}
        }

        for flag in flag_standart:
            fl: Flag = Flag(flag_standart[flag]['name'], flag_standart[flag]['func'], flag_standart[flag]['command'])
            self.__flag_list.append(fl)

    def __case_create(self):
        for case in self.__case_list_create:
            self.__Handler.case_create(**case)

    def case_create(self, name: str, cmd_list: list):
        self.__case_list_create.append({'name': name, 'cmd_list': cmd_list})

class Config:
    def __init__(self):
        self.turnOffCommand: list = []  # Список отключенных команд
        self.full_log: bool = False  # Полное отображение лога
        self.printlog: bool = False  # Вывод print в лог
        self.debug: bool = False  # Режим дебага
        self.time: bool = False  # Отображение времени в логе
        self.copyright: str = ''  # Copyright
        self.postCmd = None  # Функция, которая будет вызвана после вызова каждой команды
        self.preCmd = None  # Функция, которая будет вызвана перед вызовом каждой команды
        self.preRun = None  # Функция, которая будет вызвана перед запуском CLI


class Logger:
    def __init__(self, time: bool) -> None:
        self.builtins: dict = globals()["__builtins__"]
        self.builtin_print = self.builtins["print"]
        self.full_log_color: str = 'cyan'
        self.info_color: str = 'white'
        self.warning_color: str = 'yellow'
        self.error_color: str = 'red'
        self.time: bool = time

    def info(self, msg: str, color: str = 'white', prefix: str = 'INFO') -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date: datetime = datetime.datetime.now()
            msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
            print(colored(msg, color))
        else:
            msg: str = colored(f'{prefix}: {msg}', color)
            print(msg)

    def warning(self, msg: str) -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date: datetime = datetime.datetime.now()
            msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] WARNING: {msg}'
            print(colored(msg, self.warning_color))
        else:
            msg: str = colored(f'WARNING: {msg}', self.warning_color)
            print(msg)

    def error(self, msg: str) -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date: datetime = datetime.datetime.now()
            msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] ERROR: {msg}'
            print(colored(msg, self.error_color))
        else:
            msg: str = colored(f'ERROR: {msg}', self.error_color)
            print(msg)

    def print(self, *args) -> None:
        self.builtins["print"] = self.builtin_print
        prefix: str = 'PRINT'
        color: str = 'white'

        if self.time:
            date: datetime = datetime.datetime.now()
            msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {args[0]}'
            print(colored(msg, color))
        else:
            msg: str = colored(f'{prefix}: {args[0]}', color)
            print(msg)

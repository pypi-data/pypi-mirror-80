import datetime
import re
import os

from termcolor import colored

from .case import Case
from .error import TypeArgumentError


class Handler:
    def __init__(self, cmd_list: list, cmd_list_for_check: list, flag_list: list, full_log: bool, print_log: bool, time: bool, copyright: str, logger) -> None:
        self.colors: tuple = ('grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
        self.cmd_list_for_check: list = cmd_list_for_check
        self.builtins: dict = globals()["__builtins__"]
        self.builtin_print = self.builtins["print"]
        self.flag_list: list = flag_list
        self.copyright_: str = copyright
        self.print_log: bool = print_log
        self.full_log: bool = full_log
        self.cmd_list: list = cmd_list
        self.case_list_name: list = []
        self.version_: str = '0.1.2'
        self.case_list_: list = []
        self.time: bool = time
        self.Logger = logger

    def handle(self, command: str, preCmd = None, postCmd = None) -> None:
        flag_list: list = []

        for flag in self.flag_list:
            fl: list = re.findall(flag.re, command)
            if len(fl) == 1:
                fl: str = fl[0]
                command: str = command.replace(f' {fl}', '').replace(f'{fl} ', '')
                arg: str = re.findall(':\\w+', fl)[0][1:]
                fl_arg = eval(f'{flag.args[0][1]}({arg})')
                flag_list.append((flag.func, {flag.args[0][0]: fl_arg, 'logger': self.Logger}))
            elif len(fl) > 1:
                msg = 'One flag can only be used once'
                self.Logger.warning(msg)

        res: tuple = self.found_cmd(command)
        if res:
            found_cmd, kwargs = res

            if flag_list:
                for flag in flag_list:
                    flag[0](**flag[1])

            if preCmd:
                preCmd()

            if found_cmd.cmd_args_inline:
                for arg in found_cmd.cmd_args_inline:
                    color = 'magenta'
                    if self.time:
                        date = datetime.datetime.now()
                        kwargs.update({arg[0]: analis(input(colored(f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] INPUT: {arg[0]} - ', color)), arg[1])})
                    else:
                        kwargs.update({arg[0]: analis(input(colored(f'INPUT: {arg[0]} - ', color)), arg[1])})

            if self.full_log:
                color: str = 'cyan'
                msg: str = f'Command is running'
                self.Logger.info(msg, color=color)

            if self.print_log:
                self.builtins["print"]: dict = self.Logger.print

            result = found_cmd.run(**kwargs)

            if self.print_log:
                self.builtins["print"]: dict = self.builtin_print

            if result and self.full_log:
                color: str = 'yellow'
                prefix: str = 'RETURN'
                self.Logger.info(result, color=color, prefix=prefix)

            if self.full_log:
                color: str = 'cyan'
                msg: str = f'Command is completed'
                self.Logger.info(msg, color=color)

            if postCmd:
                postCmd()
        else:
            msg: str = f'Command \"{command}\" not found'
            self.Logger.warning(msg)

    def found_cmd(self, command) -> tuple:
        for cmd in self.cmd_list:
            res: list = re.findall(cmd.cmd_re, command)
            if res:
                res: list = res[0].split()
                kwargs: dict = {}
                if cmd.cmd_args:
                    for index in range(len(cmd.cmd_args)):
                        kwargs.update({cmd.cmd_args[index][0]: analis(res[cmd.cmd_args[index][2]],
                                                                                cmd.cmd_args[index][1])})

                return cmd, kwargs

    def help(self) -> None:
        """Help for commands"""

        self.builtins["print"]: dict = self.builtin_print
        prefix: str = 'HELP'
        color: str = 'green'
        tb: int = 111
        msg: str = f'"function name" {" "*6}|  "command"{tb*" "}  |  "documentation for the function"'
        self.Logger.info(msg, prefix=prefix, color=color)

        for cmd in self.cmd_list:
            tb_cmd: int = 120 - len(cmd.cmd_func)
            tb_name: int = 20 - len(cmd.name)
            msg: str = f'{cmd.name}{tb_name*" "}  |  {cmd.cmd_func}{tb_cmd*" "}  |  {cmd.func.__doc__}'
            self.Logger.info(msg, prefix=prefix, color=color)

    def flags(self) -> None:
        """Flags for commands"""

        self.builtins["print"]: dict = self.builtin_print
        prefix: str = 'FLAG'
        color: str = 'green'
        msg: str = f'"flag name" | "command" | "documentation for the function"'
        self.Logger.info(msg, prefix=prefix, color=color)

        for flag in self.flag_list:
            msg: str = f'"{flag.name}" | {flag.cmd} |' \
                  f' ({flag.args}) |' \
                  f' {flag.doc}'
            self.Logger.info(msg, prefix=prefix, color=color)

    def color(self) -> None:
        """A list of available colors for the output"""

        self.builtins["print"]: dict = self.builtin_print
        for color in self.colors:
            msg: str = f'name - {color}'
            prefix: str = 'COLOR'
            self.Logger.info(msg, prefix=prefix, color=color)

    def exit(self) -> None:
        """Exit"""

        self.builtins["print"]: dict = self.builtin_print
        color: str = 'cyan'
        if self.full_log:
            msg: str = f'Completion of work'
            self.Logger.info(msg, color=color)

        exit()

    def quit(self) -> None:
        """Quit"""

        self.builtins["print"]: dict = self.builtin_print
        color: str = 'cyan'
        if self.full_log:
            msg: str = f'Completion of work'
            self.Logger.info(msg, color=color)

        quit()

    def clear(self) -> None:
        """Clearing the terminal"""

        os.system('cls||clear')

    def copyright(self) -> None:
        """Output copyright"""

        self.builtins["print"]: dict = self.builtin_print
        if self.copyright_:
            print(self.copyright_, end='\n\n')
        else:
            msg: str = 'Copyright is empty'
            self.Logger.warning(msg)

    def version(self) -> None:
        """Displays the used version of the framework"""

        self.builtins["print"]: dict = self.builtin_print
        msg: str = f'py3_cli version {self.version_}'
        color: str = 'cyan'
        self.Logger.info(msg, color=color)

    def case_create(self, name: str, cmd_list: list = []) -> None:
        """Case create"""

        self.builtins["print"]: dict = self.builtin_print
        if name not in self.case_list_name:
            case: list = []
            prefix: str = 'CASE'
            color: str = 'cyan'

            if cmd_list:
                self.case_list_.append(Case(name, cmd_list))
                self.case_list_name.append(name)

                if self.full_log:
                    prefix: str = 'CASE'
                    color: str = 'cyan'
                    msg: str = f'Case \"{name}\" closed'
                    if self.time:
                        date: datetime = datetime.datetime.now()
                        msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                        self.Logger.info(msg, prefix=prefix, color=color)
                    else:
                        self.Logger.info(msg, prefix=prefix, color=color)
            else:
                if self.full_log:
                    msg: str = f'Case "{name}" created'

                    if self.time:
                        date: datetime = datetime.datetime.now()
                        msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                        self.Logger.info(msg, prefix=prefix, color=color)
                    else:
                        self.Logger.info(msg, prefix=prefix, color=color)

                msg: str = f'To close the case enter "case end"'

                if self.time:
                    date: datetime = datetime.datetime.now()
                    msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                    self.Logger.info(msg, prefix=prefix, color=color)
                else:
                    self.Logger.info(msg, prefix=prefix, color=color)


                while True:
                    color: str = 'magenta'
                    if self.time:
                        date: datetime = datetime.datetime.now()
                        command: str = input(colored(f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] INPUT: ', color))
                    else:
                        command: str = input(colored(f'INPUT: ', color))

                    if 'case create' in command:
                        msg: str = "You can't add a command 'case create' in a case"
                        self.Logger.warning(msg)
                    else:
                        if command == 'case end':
                            if case:
                                self.case_list_.append(Case(name, case))
                                self.case_list_name.append(name)

                                if self.full_log:
                                    prefix: str = 'CASE'
                                    color: str = 'cyan'
                                    msg: str = f'Case \"{name}\" closed'
                                    if self.time:
                                        date: datetime = datetime.datetime.now()
                                        msg: str = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                                        self.Logger.info(msg, prefix=prefix, color=color)
                                    else:
                                        self.Logger.info(msg, prefix=prefix, color=color)
                                return
                        else:
                            case.append(command)
        else:
            msg: str = 'A case with the same name already exists'
            self.Logger.warning(msg)

    def case_list(self) -> None:
        """List cases"""

        self.builtins["print"]: dict = self.builtin_print
        prefix: str = 'CASE'
        color: str = 'green'
        if self.case_list_:
            for case in self.case_list_:
                msg: str = f'{case.name} - {case.commands}'
                self.Logger.info(msg, prefix=prefix, color=color)
        else:
            msg: str = 'Case list is empty'
            self.Logger.info(msg, prefix=prefix, color=color)

    def case_run(self, name) -> None:
        """Run case"""

        self.builtins["print"]: dict = self.builtin_print
        for case in self.case_list_:
            if case.name == name:
                for cmd in case.run():
                    self.handle(cmd)
                    return

        msg = f'Case {name} not found'
        self.Logger.warning(msg)


def analis(arg, type_):
    types: list = ['int', 'float', 'str', 'bytes', 'bool']

    if type_ == 'str':
        return arg
    elif type_ in types:
        return eval(f'{type_}({arg})')
    else:
        msg: str = 'Invalid argument type'
        raise TypeArgumentError(msg)

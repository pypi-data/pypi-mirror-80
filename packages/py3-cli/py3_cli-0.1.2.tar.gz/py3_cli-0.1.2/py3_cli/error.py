class CmdError(Exception):
    def __init__(self, text: str) -> None:
        self.text: str = text


class TypeArgumentError(Exception):
    def __init__(self, text: str) -> None:
        self.text: str = text
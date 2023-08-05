class Case:
    def __init__(self, name, command: list) -> None:
        self.commands: list = command
        self.name: str = name

    def run(self) -> list:
        return self.commands
import readline
from pprint import pprint
from typing import Callable


class Pymand:
    commands: dict[str, Callable] = {}
    running: bool = True

    def __init__(self, commands: list[Callable]) -> None:
        for command in commands:
            self.commands[command.__name__] = command
        self.commands["quit"] = self.stop
        pass

    def listCommands(self):
        return [
            f"{name}{command.__code__.co_varnames}"
            for name, command in self.commands.items()
        ]

    def stop(self):
        self.running = False

    def prompt(self):
        return f"\n{self.listCommands()}\n\nCommand> "

    def run(self):
        while self.running:
            try:
                input_str = input(self.prompt())
                if not input_str:
                    continue
                [name, *args] = input_str.split(",")
                command = self.commands[name]
                args_dict = {k: v for k, v in map(lambda x: x.split("="), args)}
                command(**args_dict)
            except Exception as error:
                pprint(error)

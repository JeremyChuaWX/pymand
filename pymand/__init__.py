import readline
from pprint import pprint
from typing import Callable


class Pymand:
    commands: dict[str, Callable] = {}
    running: bool = True

    def __init__(self, *commands: Callable) -> None:
        for command in commands:
            self.commands[command.__name__] = command
        self.commands["quit"] = self.stop
        self.commands["help"] = self.help
        pass

    def stop(self):
        self.running = False
        return

    def help(self):
        print("<command name>[,<argument name>=<argument value>,...]")

    def format_command(self, name: str):
        command = self.commands[name]
        args = command.__code__.co_varnames
        if len(args) > 0 and args[0] == "self":
            args = args[1:]
            # TODO: parent = ???
            return f"self.{name}{args}"
        else:
            return f"{name}{args}"

    def list_commands(self):
        return [self.format_command(name) for name in self.commands.keys()]

    def format_prompt(self):
        return f"\n{self.list_commands()}\n\nCommand> "

    def run(self):
        while self.running:
            input_str = input(self.format_prompt())
            if not input_str:
                continue
            try:
                [name, *args] = input_str.split(",")
                command = self.commands[name]
                args_dict = {k: v for k, v in map(lambda x: x.split("="), args)}
                command(**args_dict)
            except Exception as error:
                pprint(error)

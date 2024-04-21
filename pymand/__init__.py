import readline
from pprint import pprint
from typing import Callable


class Pymand:
    context: dict[str, str]
    commands: dict[str, Callable] = {}
    running: bool = True

    def __init__(self, context: dict[str, str], *commands: Callable):
        self.context = context
        for command in commands:
            self.commands[command.__name__] = command
        self.commands["quit"] = self.stop
        self.commands["help"] = self.help
        return

    def run_command(self, command: Callable, args_dict: dict[str, str]):
        args = command.__code__.co_varnames
        args = args[1:] if len(args) > 0 and args[0] == "self" else args
        final_args = {k: v for k, v in self.context if k in args}
        for key, value in args_dict.items():
            final_args[key] = value
        return command(**final_args)

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

    def stop(self):
        self.running = False
        return

    def help(self):
        print("<command name>[,<argument name>=<argument value>,...]")

    def run(self):
        while self.running:
            input_str = input(self.format_prompt())
            if not input_str:
                continue
            try:
                [name, *args] = input_str.split(",")
                command = self.commands[name]
                args_dict = {k: v for k, v in map(lambda x: x.split("="), args)}
                res = self.run_command(command, args_dict)
                pprint(res)
            except Exception as error:
                pprint(error)

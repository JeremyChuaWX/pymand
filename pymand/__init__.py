import readline
from typing import Callable


class Pymand:
    context: dict[str, str]
    commands: dict[str, Callable] = {}
    running: bool = True
    prompt: str

    def __init__(self, context: dict[str, str], *commands: Callable):
        self.context = context

        self.commands["quit"] = self.stop
        self.commands["help"] = self.help

        for command in commands:
            self.commands[command.__name__] = command

        def format_command(name: str, command: Callable):
            arg_list = get_command_arg_list(command)
            return f"{name}{arg_list}"

        self.prompt = f"\n{[format_command(name, command) for name, command in self.commands.items()]}\nCommand> "

        return

    def run_command(self, command: Callable, args_dict: dict[str, str]):
        arg_list = get_command_arg_list(command)
        # pick arg values from context
        args = {k: v for k, v in self.context.items() if k in arg_list}
        for key, value in args_dict.items():
            args[key] = value
        return command(**args)

    def stop(self):
        self.running = False
        return

    @staticmethod
    def help():
        print("<command name>[,<argument name>=<argument value>,...]")
        return

    def run(self):
        while self.running:
            input_str = input(self.prompt)
            if not input_str:
                continue
            try:
                [name, *args] = input_str.split(",")
                command = self.commands[name]
                args_dict = {k: v for k, v in map(lambda x: x.split("="), args)}
                res = self.run_command(command, args_dict)
                print(res)
            except Exception as error:
                print(error)


def get_command_arg_list(command: Callable):
    args = command.__code__.co_varnames
    # remove `self` parameter
    return args[1:] if len(args) > 0 and args[0] == "self" else args

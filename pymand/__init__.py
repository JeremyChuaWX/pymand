from pprint import pprint
import readline


class Pymand:
    def __init__(self, commands) -> None:
        self.commands = commands


def main():
    commands = get_commands()
    print("available commands:")
    pprint(commands)

    while True:
        user_input = input("enter command: ")
        [command, *args] = user_input.split(" ")
        if command in commands:
            command_function = getattr(Pymand, command)
            command_function(*args)
        else:
            print("invalid command")

import sys

sys.path.append(".")

from pymand import Pymand


def fib(num: str) -> int:
    num = int(num)
    if num <= 2:
        return 1
    return fib(num - 1) + fib(num - 2)


def main():
    pymand = Pymand({}, fib)
    pymand.run()


if __name__ == "__main__":
    main()

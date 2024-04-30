import sys

sys.path.append(".")

from pymand import Pymand
from math import sqrt


def fib(num: str) -> int:
    num = int(num)
    if num <= 2:
        return 1
    return fib(num - 1) + fib(num - 2)


def is_prime(num: str) -> int:
    num = int(num)
    candidate_divisors = sqrt(num)
    for divisor in range(2, int(candidate_divisors) + 1):
        result = num / divisor
        if result == int(result):
            return False
    return True


def main():
    pymand = Pymand({}, fib, is_prime)
    pymand.run()


if __name__ == "__main__":
    main()

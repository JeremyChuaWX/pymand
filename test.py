from pymand import Pymand


def square(text: str):
    print("testing", text)


def main():
    pymand = Pymand(
        [
            square,
        ]
    )
    pymand.run()
    pass


if __name__ == "__main__":
    main()

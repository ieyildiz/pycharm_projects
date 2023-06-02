from sqlite3 import SQLITE_UPDATE


def main():
    x = int(input("What is x?"))
    print("x squared is", square(x))


def square(n):
    return n + n # pow or n * 2

if __name__ == "__main__":
    main()

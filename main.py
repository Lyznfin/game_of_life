def random_state(width: int, height: int, /):
    pass

def dead_state(width: int, height: int, /) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]

def main():
    print(dead_state(5, 5))

if __name__ == "__main__":
    main()
import random

def random_cell() -> int:
    random_number = random.random()
    if random_number >= 0.5:
        return 1
    else:
        return 0

def random_state(height: int, width: int, /):
    state = dead_state(height, width)
    for i in range(len(state)):
        for j in range(len(state[i])): 
            cell_state = random_cell()
            state[i][j] = cell_state
    print(state)

def dead_state(height: int, width: int, /) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]

def main():
    random_state(5, 5)

if __name__ == "__main__":
    main()
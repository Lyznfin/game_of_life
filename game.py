import random
import time
import os

from colorama import Fore, Style

class Game:
    def __init__(self, height: int, width: int, /, *, state: list[list[int]] = None) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        if not state is None:
            self.state = state
        else:
            self.__initialize_random_state()

    def __random_cell(self) -> int:
        random_number = random.random()
        return 1 if random_number >= 0.8 else 0

    def __initialize_random_state(self) -> None:
        self.state = self.__dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                cell_state = self.__random_cell()
                self.state[i][j] = cell_state

    def __dead_state(self) -> list[list[int]]:
        return [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
    
    def __next_cell_state(self, row: int, column:int) -> int:
        live_neighbors = 0
        for i in range((row-1), (row+1)+1):
            if i < 0 or i >= self.HEIGHT:
                continue
            for j in range((column-1), (column+1)+1):
                if j < 0 or j >= self.WIDTH:
                    continue
                if i == row and j == column:
                    continue
                if self.state[i][j] == 1:
                    live_neighbors += 1

        live_state = [2, 3]
        if self.state[row][column] == 1:
            if live_neighbors in live_state:
                return 1
            else:
                return 0
        else:
            if live_neighbors == 3:
                return 1
            else:
                return 0

    def __next_board_state(self) -> None:
        new_state = self.__dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                new_cell_state = self.__next_cell_state(i, j)
                new_state[i][j] = new_cell_state
        self.state = new_state
        
    def __render(self) -> None:
        display_as = {
            0: Fore.BLACK + u"\u2588",
            1: Fore.WHITE + u"\u2588"
        }
        lines = []
        for i in range(self.HEIGHT):
            line = ''
            for j in range(self.WIDTH):
                line += display_as[self.state[i][j]] * 2
            lines.append(line)
        print("\n".join(lines))
        print(Style.RESET_ALL)

    def start(self) -> None:
        while True:
            self.__render()
            self.__next_board_state()
            time.sleep(0.5)
            os.system('cls')
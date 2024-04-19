import random
from colorama import Fore, Style
import time

class Game:
    def __init__(self, height: int, width: int, /) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.__initialize_random_state()
        # self.state = [
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 1, 1, 0],
        #     [0, 1, 1, 1, 0, 0],
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0]
        # ]

    def __random_cell(self) -> int:
        random_number = random.random()
        return 1 if random_number >= 0.9 else 0

    def __initialize_random_state(self):
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

    def __next_board_state(self) -> bool:
        new_state = self.__dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                new_cell_state = self.__next_cell_state(i, j)
                new_state[i][j] = new_cell_state
        if self.state == new_state:
            return False
        self.state = new_state
        return True

    def start(self):
        while True:
            self.render()
            state = self.__next_board_state()
            if not state:
                break
            time.sleep(0.3)

        
    def render(self) -> None:
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
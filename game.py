import random
import time
import os

from colorama import Fore, Style

class Game:
    def __init__(self, height: int = 0, width: int = 0, /, *, soup_path: str = None, moore: bool = True, zombie: bool = False) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.MOORE = moore
        self.ZOMBIE = zombie
        if soup_path is not None:
            self.__load_soup(soup_path)
        else:
            self.__initialize_random_state()

    def __initialize_dead_state(self) -> list[list[int]]:
        return [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

    def __load_soup(self, soup_path: str, /) -> None:
        with open(soup_path, "r") as soup:
            self.state = []
            for line in soup:
                row = []
                for letter in line.strip():
                    row.append(int(letter))
                self.state.append(row)

        self.HEIGHT = len(self.state)
        self.WIDTH = len(self.state[0])

    def __random_cell(self) -> int:
        random_number = random.random()
        return 1 if random_number >= 0.8 else 0
    
    def __random_zombie_cell(self) -> int:
        random_number = random.random()
        if random_number <= 0.6:
            return 1
        elif random_number > 0.6 and random_number < 0.7:
            return 2
        else:
            return 0

    def __initialize_random_state(self) -> None:
        self.state = self.__initialize_dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                cell_state = self.__random_cell() if not self.ZOMBIE else self.__random_zombie_cell()
                self.state[i][j] = cell_state

    def __cell_state(self, live_neighbors: int, row: int, column:int, /) -> int:
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
            
    def __zombie_cell_state(self, live_neighbors: int, zombie_neighbors: int, row: int, column:int, /) -> int:
        random_number = random.random()
        live = [2, 3]
        if self.state[row][column] == 1:
            if live_neighbors in live:
                return 1 if random_number > 0.01 else 2
            elif zombie_neighbors > live_neighbors:
                return 2
            else:
                return 0 if random_number > 0.1 else 2
        if self.state[row][column] == 2:
            return 0
        else:
            if zombie_neighbors > 3:
                return 2
            elif live_neighbors == 3:
                return 1
            else:
                return 0 if random_number > 0.05 else 2
    
    def __moore_next_cell_state(self, row: int, column:int, /) -> int:
        live_neighbors = 0
        zombie_neighbors = 0
        for i in range(row-1, row+2):
            if i < 0 or i >= self.HEIGHT:
                continue
            for j in range(column-1, column+2):
                if j < 0 or j >= self.WIDTH:
                    continue
                if i == row and j == column:
                    continue
                if self.state[i][j] == 1:
                    live_neighbors += 1
                if self.state[i][j] == 2:
                    zombie_neighbors += 1
        
        return self.__cell_state(live_neighbors, row, column) if not self.ZOMBIE else self.__zombie_cell_state(live_neighbors, zombie_neighbors, row, column)
            
    def __neumann_next_cell_state(self, row: int, column:int, /) -> int:
        live_neighbors = 0
        zombie_neighbors = 0
        for i in range(row-2, row+3):
            if i < 0 or i >= self.HEIGHT:
                continue
            if i == row:
                continue
            if self.state[i][column] == 1:
                live_neighbors += 1
            if self.state[i][column] == 2:
                zombie_neighbors += 1
            
        for j in range(column-2, column+3):
            if j < 0 or j >= self.WIDTH:
                continue
            if j == column:
                continue
            if self.state[row][j] == 1:
                live_neighbors += 1
            if self.state[row][j] == 2:
                zombie_neighbors += 1
        
        return self.__cell_state(live_neighbors, row, column) if not self.ZOMBIE else self.__zombie_cell_state(live_neighbors, zombie_neighbors, row, column)

    def __next_board_state(self) -> None:
        new_state = self.__initialize_dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                new_cell_state = self.__moore_next_cell_state(i, j) if self.MOORE else self.__neumann_next_cell_state(i, j)
                new_state[i][j] = new_cell_state
        self.state = new_state
        
    def __render(self) -> None:
        display_as = {
            0: Fore.BLACK + u"\u2588",
            1: Fore.WHITE + u"\u2588",
            2: Fore.GREEN + u"\u2588"
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
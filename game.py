import random
import time
import os

from colorama import Fore

class Game:
    def __init__(self, height: int = 0, width: int = 0, /, *, soup_path: str = None, state_mode: str = "moore", cell_mode: str = "moore") -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.STATE_MODE = self.__validate_mode(state_mode)
        self.CELL_MODE = self.__validate_mode(cell_mode)
        if soup_path is not None:
            self.__load_soup(soup_path)
        else:
            self.__initialize_random_state()

    def __validate_mode(self, mode: str, /) -> str:
        valid_modes = ["moore", "neumann", "zombie", "brians"]
        if mode not in valid_modes:
            raise ValueError
        return mode

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
        if random_number <= 0.7:
            return 1
        elif random_number > 0.7 and random_number < 0.8:
            return -1
        else:
            return 0

    def __initialize_random_state(self) -> None:
        self.state = self.__initialize_dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                cell_state = self.__random_cell() if not self.STATE_MODE == "zombie" else self.__random_zombie_cell()
                self.state[i][j] = cell_state

    def __cell_state(self, live_neighbors: int, row: int, column:int, /) -> int:
        live_state = [2, 3]
        match self.state[row][column]:
            case 0:
                if live_neighbors == 3:
                    return 1
                else:
                    return 0
            case 1:
                if live_neighbors in live_state:
                    return 1
                else:
                    return 0
            
    def __zombie_cell_state(self, live_neighbors: int, zombie_neighbors: int, row: int, column:int, /) -> int:
        live = [2, 3]
        random_number = random.random()
        match self.state[row][column]:
            case 0:
                if zombie_neighbors > 3:
                    return 2
                elif live_neighbors == 3:
                    return 1
                else:
                    return 0 if random_number > 0.05 else 2
            case 1:
                if live_neighbors in live:
                    return 1 if random_number > 0.01 else 2
                elif zombie_neighbors > live_neighbors:
                    return 2
                else:
                    return 0 if random_number > 0.1 else 2
            case 2:
                return 0
            
    def __brians_brain_cell_state(self, live_neighbors: int,row: int, column:int, /) -> int:
        match self.state[row][column]:
            case 0:
                if live_neighbors == 2:
                    return 1
                else:
                    return 0
            case 1:
                return -1
            case -1:
                return 0
    
    def __moore_next_cell_state(self, row: int, column:int, /) -> int:
        live_neighbors = 0
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
        
        return self.__brians_brain_cell_state(live_neighbors, row, column) if self.CELL_MODE == "brians" else self.__cell_state(live_neighbors, row, column)

    def __neumann_next_cell_state(self, row: int, column:int, /) -> int:
        live_neighbors = 0
        for i in range(row-2, row+3):
            if i < 0 or i >= self.HEIGHT:
                continue
            if i == row:
                continue
            if self.state[i][column] == 1:
                live_neighbors += 1
            
        for j in range(column-2, column+3):
            if j < 0 or j >= self.WIDTH:
                continue
            if j == column:
                continue
            if self.state[row][j] == 1:
                live_neighbors += 1
        
        return self.__cell_state(live_neighbors, row, column)
    
    def __zombie_next_cell_state(self, row: int, column:int, /) -> int:
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

        return self.__zombie_cell_state(live_neighbors, zombie_neighbors, row, column)

    def __next_cell_state(self, row: int, column:int, /) -> int:
        match self.STATE_MODE:
            case "moore":
                return self.__moore_next_cell_state(row, column)
            case "neumann":
                return self.__neumann_next_cell_state(row, column)
            case "zombie":
                return self.__zombie_next_cell_state(row, column)

    def __next_board_state(self) -> None:
        new_state = self.__initialize_dead_state()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                new_cell_state = self.__next_cell_state(i, j)
                new_state[i][j] = new_cell_state
        self.state = new_state
        
    def __render(self) -> None:
        display_as = {
            0: Fore.BLACK + u"\u2588",
            1: Fore.WHITE + u"\u2588",
            2: Fore.GREEN + u"\u2588",
            -1: Fore.BLUE + u"\u2588",
        }
        lines = []
        for i in range(self.HEIGHT):
            line = ' '
            for j in range(self.WIDTH):
                line += display_as[self.state[i][j]] * 2
            lines.append(line)
        print("\n".join(lines))

    def start(self) -> None:
        while True:
            self.__render()
            self.__next_board_state()
            time.sleep(0.5)
            os.system('cls')
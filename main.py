from game import Game

def main() -> None:
    game = Game(40, 80, state_mode="moore", cell_mode="brians")
    game.start()

if __name__ == "__main__":
    main()
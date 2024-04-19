from game import Game

def main() -> None:
    # game = Game(soup_path="soups/glider.txt")
    game = Game(40, 40, zombie=True, moore=True)
    game.start()

if __name__ == "__main__":
    main()
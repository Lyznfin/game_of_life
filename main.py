from game import Game

def main() -> None:
    game = Game(soup_path="soups/glider.txt")
    game.start()

if __name__ == "__main__":
    main()
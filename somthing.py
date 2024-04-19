soup_path = "soups/toad.txt"

with open(soup_path, "r") as soup:
    print(len(soup.readline()) - 1)
    print(len(soup.readlines()) + 1)
    # for line in soup:
    #     print(len(line))
    #     for letter in line:
    #         print(letter)
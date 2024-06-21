from autoanki.fc import load, genanki
import sys


if __name__ == "__main__":
    package_path = sys.argv[1]
    decks = []
    for path in sys.argv[2:]:
        if path[-3:] != ".fc":
            continue
        name = path.split("/")[-1][:-3]
        print(f"Processing [{name}]@[{path}]", end="")
        decks.append((name, load(path)))
        print(f"| {len(decks[-1][1])} cards loaded")
    genanki(decks, package_path)

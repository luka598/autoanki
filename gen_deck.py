from autoanki.fc import load, genanki
import sys


if __name__ == "__main__":
    print(sys.argv)
    path_base = sys.argv[1]
    name = sys.argv[1].split("/")[-1]
    fcs = load(f"{path_base}.fc")
    genanki(name, fcs, path=f"{path_base}.apkg")

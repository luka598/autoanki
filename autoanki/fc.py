import dataclasses as dc
import typing as T
import genanki as _genanki
import random


@dc.dataclass
class Flashcard:
    front: str
    back: str


def loads(s: str):
    flashcards = []
    for fc in s.split("\n\n"):
        if fc == "":
            continue
        if fc[0] == "#":
            continue

        front, back = fc.split("\n")[:2]
        flashcards.append(Flashcard(front[7:], back[6:]))
    return flashcards


def load(filename: str):
    with open(filename, "r") as f:
        return loads(f.read())


def dumps(flashcards: T.List[Flashcard]) -> str:
    s = ""
    for fc in flashcards:
        s += f"FRONT: {fc.front}\n"
        s += f"BACK: {fc.back}\n"
        s += "\n"
    return s


def dump(filename: str, flashcards: T.List[Flashcard]):
    with open(filename, "w") as f:
        return f.write(dumps(flashcards))


def genanki(decks_t: T.List[T.Tuple[str, T.List[Flashcard]]], package_path: str):
    model = _genanki.Model(
        random.randint(1000000000, 9999999999),
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<i>{{Deck}}<br></i>{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )

    decks = []

    for name, flashcards in decks_t:
        deck = _genanki.Deck(hash(name) % 10000000000, name)
        for fc in flashcards:
            deck.add_note(_genanki.Note(model=model, fields=[fc.front, fc.back]))
        decks.append(deck)

    print(decks)
    package = _genanki.Package(decks)
    package.write_to_file(package_path)

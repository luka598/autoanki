from autoanki.fc import load, genanki

fcs = load("deck.fc")
genanki("hrv", fcs)

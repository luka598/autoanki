from autoanki.gpt import send, Request, Message, TextContent, ImageUrlContent
from autoanki.img import get_image
from autoanki.fc import loads

PROMPT = """\
Please create 5-20 concise question type Anki flashcards based on the most important information for a high-school student from the provided lecture. Use the following three examples as general guidelines for the desired format:

FRONT: For what sense is olfactory nerve responsible?
BACK: Smell; It is the 1st cranial nerve.

FRONT: What are chromosomes and in what are they found in?
BACK: Chromosomes are organized structures of DNA and proteins found in the nucleus; They contain many genes, regulatory elements, and intervening sequences.

FRONT: Na koja područja se dijeli teorija književnosti?
BACK: Stilistika, verzifikacija (znanost o stihu), klasifikacija književnosti.

On the back of each flashcard, if relevant, feel free to use a semicolon and then include any relevant supplementary information (such as definitions, visual aids, high-yield facts, correlations, mnemonics or other relevant information). Flashcards must be in Croatian.
"""

messages = [
    Message("system", TextContent(PROMPT)),
]

while input("end? (y/N): ") != "y":
    img = get_image(False)
    if not img:
        print("No image, exiting!")
        exit()

    if input("detail (L/h): ") != "h":
        detail = "low"
    else:
        detail = "high"

    messages.append(
        Message("user", ImageUrlContent.from_image(img, "png", detail)),
    )


print("Sending request")
r = send(
    Request(
        "gpt-4o",
        messages,
        max_tokens=1000,
    ),
)

print(r)

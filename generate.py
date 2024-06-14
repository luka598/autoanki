from autoanki.gpt import send, Request, Message, TextContent, ImageUrlContent
from autoanki.img import get_image

PROMPT = """\
Please create 10-20 concise cloze deletion Anki flashcards based on the most important information for a high-school student from the provided lecture. Use the following two examples as general guidelines for the desired format:

The {{c1::olfactory nerve}} is responsible for the sense of {{c2::smell}}; It is the 1st cranial nerve.

{{c1::Chromosomes}} are organized structures of DNA and proteins found in the {{c2::nucleus}}; They contain many genes, regulatory elements, and intervening sequences.

Teorija književnosti dijeli se na nekoliko područja: {{c1::stilistika}}, {{c2::verzifikacija}} (znanost o stihu), {{c3::klasifikacija književnosti}}.

After each flashcard, if relevant, feel free to use a semicolon and then include any relevant supplementary information (such as definitions, visual aids, high-yield facts, correlations, mnemonics or other relevant information) without using cloze deletion. Flashcards must be in Croatian. Make sure that all key information from the flashcards are cloze deleted.
"""

img = get_image()
if not img:
    print("No image, exiting!")
    exit()

print("Sending request")
r = send(
    Request(
        "gpt-4o",
        [
            Message("system", TextContent(PROMPT)),
            Message("user", ImageUrlContent.from_image(img, "png", "high")),
        ],
        max_tokens=1000,
    ),
)

print(r)

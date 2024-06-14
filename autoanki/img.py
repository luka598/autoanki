import subprocess
from PIL import Image
import io


def display_image(data):
    image = Image.open(io.BytesIO(data))
    image.show()


def get_image(confirm: bool = True) -> bytes:
    process = subprocess.Popen(
        ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
        stdout=subprocess.PIPE,
    )
    data, _ = process.communicate()

    if not data:
        return b""

    if confirm:
        display_image(data)
        if input("Is this the correct image (y/*): ") != "y":
            return b""

    return data

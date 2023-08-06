import base64
from PIL import Image
import io

with open("soter_logo.png", "rb") as image:
    image_co = image.read()
    print(image_co[:100])

with open("soter_logo.jpeg", "rb") as image:
    image_co = image.read()
    print(image_co[:100])

with open("test.pdf", "rb") as image:
    image_co = image.read()
    print(image_co[:100])

with open("test.txt", "rb") as image:
    image_co = image.read()
    print(image_co[:100])

with open("test.xlsx", "rb") as image:
    image_co = image.read()
    print(image_co[:100])
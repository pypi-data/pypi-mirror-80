import base64
with open("soter_logo.jpeg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string.decode('utf-8') + "ds")
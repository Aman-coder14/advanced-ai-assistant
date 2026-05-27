from PIL import Image


def open_image(uploaded_file):

    image = Image.open(uploaded_file)

    return image
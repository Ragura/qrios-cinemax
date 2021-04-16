import requests
import io
# from tkinter import Tk
from PIL import Image
from PIL.ImageTk import PhotoImage

# root = Tk()


def get_img_data(file, maxsize=(1200, 850), first=False, local=False):
    """Generate image data using PIL"""
    if not local:
        img = Image.open(requests.get(file, stream=True).raw)
    else:
        img = Image.open(file)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return PhotoImage(img)

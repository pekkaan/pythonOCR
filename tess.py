from PIL import Image, ImageGrab
import pytesseract
import keyboard
import mouse
import os
import pdf2image
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
"""
coords = []

keyboard.wait("ctrl+shift")
def add_coords():
    coords.append(mouse.get_position())
mouse.on_click(add_coords)
keyboard.wait("ctrl+shift")

img = ImageGrab.grab(bbox=(coords[0][0], coords[0][1], coords[1][0], coords[1][1]))  # Unfortunately ImageGrab seems to create blurry images
img.save("temp_pic.png", "png")
"""
imgs_path = os.path.join(os.getcwd(), "images")
print("converting pdf to images...")
imgs = pdf2image.convert_from_path("1055_RK-B101.pdf", output_folder=imgs_path, poppler_path="C:\\Users\\tommi\\miniconda3\\pkgs\\poppler-0.89.0-h0cd1227_0\\Library\\bin")
print("converted, trying to find text...")
for img in imgs:
    img_txt = pytesseract.image_to_string((img), lang="fin")
    #img_box = pytesseract.image_to_boxes((img), lang="fin")  # massively impacts performance (from 14s to 26s)
    if "KOKONAISMITTA" in img_txt:
        print("found")
        print(img_txt)
        arr = img_txt.split(" ")  # Here we use space for now
        for x in arr:
            if "KOKONAISMITTA" in x:
                print(x)
    else:
        print("not found")
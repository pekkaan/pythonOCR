# pythonOCR

Library for finding and locating words in PDF or image files.

## Prerequisites

PythonOCR utilizes Tesseract OCR to recognize text in image files. pdf2image is used to convert PDF files into images. pyautogui is used for taking screenshots and mouse controls.

### Python

Install Python (3.5+) and include pip with the installation. **Add Python to PATH.**

Download Python: https://www.python.org/downloads/

### pdf2image

Install pdf2image using pip:

```
pip install pdf2image
```

More information at: https://pypi.org/project/pdf2image/

_NOTE:_ poppler will be included with PythonOCR, in the /bin directory.

### pyautogui

Install pyautogui using pip:

```
pip install pyautogui
```

More information at: https://pypi.org/project/PyAutoGUI/

### Tesseract OCR

Install Tesseract OCR and include Finnish. **Add Tesseract-OCR to PATH.**

Download Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

More information at: https://github.com/tesseract-ocr/tessdoc

### pytesseract

Install pytesseract using pip:

```
pip install pytesseract
```

More infromation at: https://pypi.org/project/pytesseract/

## Installing

WIP Download/Copy pythonOCR directory and add it to your project directory.

## Usage

Add pythonOCR directory to your project directory.

Include PythonOCR class in your code:

```
from pythonOCR.python_ocr import PythonOCR
```

Create a PythonOCR class object:

```
my_object = PythonOCR()
```

The class object can use PythonOCR functions:

```
my_object.click_word(<word>)

my_object.find_words(<word>, <file path>)

my_object.find_coordinates(<word>, <file path>)

my_object.verify_word(<word>, <file path>)
```

## Functions

Main functions of pythonOCR library are click_word(), find_word(), find_coordinates(), verify_word(). Other functions in python_ocr.py file are used by these main functions.

### click_word()

Function takes a screenshot of the screen and locates a specified word in it. If the word is found, moves mouse to the coordinates of the word and clicks the location. If multiple instances of the word are found, raises an error.

Arguments:

```
click_word(word)
```

```word```: The specified word. Required. Upper and lowercase sensitive!

Example:

```
my_object.click_word("Python")
```

### find_words()

Function finds all instances of a specific word in PDF or image file. Converts a PDF file to image(s) in order to locate instances of the word. Able to handle .pdf, .jpg, .jpeg, and .png -files.

Arguments:

```
find_words(word, file_path, output_path)
```

```word```: The specified word. Required. Upper and lowercase sensitive!

```file_path```: PDF or image file path as string. Path can be absolute or relative to pythonOCR directory. Required.

```output_path```: Output directory for image files converted from PDF file. Path can be absolute or relative to pythonOCR directory. By default pythonOCR directory.

Returns:

A list of found instances of the word as a list of tuples, consisting of: (found text, page number).

Example:

```
print(
  my_object.find_words("Python", "my_file.pdf")
  )
```

### find_coordinates()

Function finds all instances of a specified word and it's coordinates in PDF or image file. Converts PDF file to image(s) in order to locate instances of the word. Able to handle .pdf, .jpg, .jpeg, and .png -files.

Arguments:

```
find_coordinates(word, file_path, output_path)
```

```word```: The specified word. Required. Upper and lowercase sensitive!

```file_path```: PDF or image file path as string. Path can be absolute or relative to pythonOCR directory. Required.

```output_path```: Output directory for image files converted from PDF file. Path can be absolute or relative to pythonOCR directory. By default pythonOCR directory.

Returns:

A list of found instances of the word and their coordinates as a list of tuples, consisitng of: (found text, left coordinates, top coordinates, text width, text height, page number)

Example:

```
print(
  my_object.find_coordinates("Python", "my_file.pdf")
  )
```

### verify_word()

Function searches for any instance of a specified word in image file. Able to handle .jpg, .jpeg, and .png -files.

Arguments:

```
verify_word(word, image_path)
```

```word```: The specified word. Required. Upper and lowercase sensitive!

```image_path```: Image file path, can be absolute or relative to pythonOCR directory. Required.

Returns:

True if found at least one instance of the word, False if none.

Example:

```
print(
  my_object.find_words("Python", "my_image.jpg")
  )
```

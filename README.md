# PythonOCR

PythonOCR module for finding and locating words on screen, in image files or PDF files.

## Prerequisites

PythonOCR utilizes the following modules:

**pyautogui** for taking screenshots and mouse controls.

**pdf2image** to convert PDF files to image files. pdf2image is a wrapper around poppler.

    **poppler** to read, render and modify PDF files.

**pytesseract** to recognize text in image files. pytesseract requires Tesseract OCR in order to function.

### Python

Install Python (3.5+) and include pip with the installation. **Add Python to PATH.**

Download Python: https://www.python.org/downloads/

### pyautogui

Install pyautogui using pip:

```
pip install pyautogui
```

More information at: https://pypi.org/project/PyAutoGUI/

### poppler

Download the latest poppler release (.zip file) from: https://github.com/oschwartz10612/poppler-windows/releases/

More information at: https://github.com/oschwartz10612/poppler-windows

1. Unzip the poppler release.

2. Add the poppler folder ('poppler-xx') to your local Python library's site packages.

On Windows, local Python site packages may be located at:

```C:\Users\<User name>\AppData\Local\Programs\Python\<Python 3 version>\Lib\site-packages```

_NOTE:_ As Python and its libraries were added to PATH, there is no need to add poppler separately to PATH.

### pdf2image

Install pdf2image using pip:

```
pip install pdf2image
```

More information at: https://pypi.org/project/pdf2image/ and https://github.com/Belval/pdf2image

### Tesseract OCR

Install Tesseract OCR and include Finnish. **Add Tesseract-OCR to PATH.**

Download Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

More information at: https://github.com/tesseract-ocr/tessdoc

### pytesseract

Install pytesseract using pip:

```
pip install pytesseract
```

More information at: https://pypi.org/project/pytesseract/

## Installing

Download 'pythonocr.py' module and add it to your project directory.

## Usage

Add 'pythonocr.py' module to your project directory.

Import 'pythonocr.py' module to your code:

```
import pythonocr
```

Alternatively, 'pythonocr.py' module can be located in a subdirectory under the project directory. Importing 'pythonocr.py' from a relative subdirectory (<folder>) to your code is done as follows:

```
from <folder> import pythonocr
```

PythonOCR library functions can then be used as follows:

```
pythonocr.click_word(<word>)

pythonocr.find_words(<word>, <file path>)

pythonocr.find_coordinates(<word>, <file path>)

pythonocr.verify_word(<word>, <file path>)
```

Detailed examples of how to use each of these functions are provided in **Functions** section.

### Usage in QAutoRobot

Work in progress...

## Functions

Main functions of PythonOCR library are: click_word(), find_word(), find_coordinates(), verify_word().

_NOTE:_ Provide file paths and directory paths in string format to function parameters. Include file type endings, such as '.jpg' or '.png', when providing file paths.

### Function: click_word()

Function takes a screenshot of the screen and searches for a specified word in it. If a single instance of the word is found, moves cursor to the coordinates of the word and clicks the location. Optionally, screenshot can be saved as a file.

If multiple instances of the word are found, a specific one can be selected by index to be clicked. By default, does not click any found word, if multiple instances are found.

**Parameters:** ```click_word(word, save_screenshot_as, index)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```save_screenshot_as```: Optional. File name in string format for saving the screenshot. MUST include valid file type ending, such as '.jpg' or '.png'. In addition, may include absolute path or relative directory path to current project folder, where the screenshot is saved at. By default, or if empty, screenshot is not saved.

```index```: Optional. Index of the specific found word, in integer format. First found instance of the word is at position 0 (zero). By default, or if less than 0, no instance will be chosen and none of the multiple found words will be clicked.

**Examples:**

```pythonocr.click_word("Python")``` Searches for word 'Python' on screen and if a single instance is found, clicks its location. Screenshot is not saved.

```pythonocr.click_word("Python", "screenshot.png")``` As above, but the screenshot is saved to the current project directory as 'screenshot.png'.

```pythonocr.click_word("Python", "./screenshots/screenshot.png")``` As above, but the screenshot is saved to 'screenshots' folder in the current project directory.

```pythonocr.click_word("Python", "C:/project_folder/screenshots/screenshot.png")``` As above, but the screenshot is saved to the specific directory.

```pythonocr.click_word("Python", index=0)``` Searches for the word on screen and if finds multiple instances of the word, clicks the first found instance (at index position 0 (zero)). Screenshot is not saved.

### Function: find_words()

Function searches for all instances of a specific word in image or PDF file. Converts a PDF file to image(s) in order to locate the instances of the word. Able to handle '.jpg', '.jpeg', '.png', and '.pdf' files.

**Parameters:** ```find_words(word, file_path, output_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```file_path```: Required. Image or PDF file path in string format. Can be absolute or relative to the current project directory.

```output_path```: Output directory in string format for image files converted from the PDF file. Not required if processing image files. By default, current project directory.

**Returns:**

A list of found instances of the word as a list of tuples, each element consisting of: (found text, page number).

**Examples:**

```pythonocr.find_words("Python", "image_file.png")``` Returns all found instances of the word 'Python' in 'image_file.png'.

```results_list = pythonocr.find_words("Python", "image_file.png")``` As above, but the results are assigned to 'results_list' variable.

```print(pythonocr.find_words("Python", "image_file.png"))``` As above, but the results are printed to console.

```pythonocr.find_words("Python", "./project_files/image_file.png")``` Returns all found instances of the word in 'image_file.png' located in 'project_files' folder in the current project directory.

```pythonocr.find_words("Python", "pdf_file.pdf")``` Returns all found instances of the word 'Python' in 'pdf_file.pdf'. Images converted from the PDF file are saved to the current project directory.

```pythonocr.find_words("Python", "pdf_file.pdf", "./output")``` As above, but images are saved to 'output' folder in the current project directory.

```pythonocr.find_words("Python", "C:/projet_folder/pdf_file.pdf", "C:/project_folder/output")``` As above, but file path and output folder for images are provided as absolute file paths.

### Function: find_coordinates()

Function searches for all instances of a specified word and their coordinates in image or PDF file. Converts PDF file to image(s) in order to locate instances of the word. Able to handle '.jpg', '.jpeg', '.png', and '.pdf' files.

**Parameters:** ```find_coordinates(word, file_path, output_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```file_path```: Required. Image or PDF file path in string format. Can be absolute or relative to the current project directory.

```output_path```: Output directory in string format for image files converted from the PDF file. Not required if processing image files. By default, current project directory.

**Returns:**

A list of found instances of the word and their coordinates as a list of tuples, each element consisting of: (found text, left coordinates, top coordinates, text width, text height, page number).

**Examples:**

```pythonocr.find_coordinates("Python", "image_file.png")``` Returns all instances of the word 'Python' and their coordinates in 'image_file.png'.

```results_list = pythonocr.find_coordinates("Python", "image_file.png")``` As above, but the results are assigned to 'results_list' variable.

```print(pythonocr.find_coordinates("Python", "image_file.png"))``` As above, but the results are printed to console.

```pythonocr.find_coordinates("Python", "./project_files/image_file.png")``` Returns all found instances of the word and their coordinates in 'image_file.png' located in 'project_files' folder in the current project directory.

```pythonocr.find_coordinates("Python", "pdf_file.pdf")``` Returns all found instances of the word 'Python' and their coordinates in 'pdf_file.pdf'. Images converted from the PDF file are saved to the current project directory.

```pythonocr.find_coordinates("Python", "pdf_file.pdf", "./output")``` As above, but images are saved to 'output' folder in the current project directory.

```pythonocr.find_coordinates("Python", "C:/projet_folder/pdf_file.pdf", "C:/project_folder/output")``` As above, but file path and output folder for images are provided as absolute file paths.

### Function: verify_word()

Function searches for any instances of a specified word in image file. Able to handle '.jpg', '.jpeg', and '.png' files.

**Parameters:** ```verify_word(word, image_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```image_path```: Required. Image file path in string format. Can be absolute or relative to the current project directory.

**Returns:**

Bool: True if found at least one instance of the specified word, False if none.

**Examples:**

```pythonocr.verify_word("Python", "image_file.png")``` Returns True or False if finds any instances of the word 'Python' in 'image_file.png'.

```found_word = pythonocr.verify_word("Python", "image_file.png")``` As above, but the result is assigned to 'found_word' variable.

```print(pythonocr.verify_word("Python", "image_file.png"))``` As above, but the result is printed to console.

```pythonocr.verify_word("Python", "./project_files/image_file.png")``` Returns the result regarding the 'image_file.png' located in 'project_files' folder in the current project directory.

```pythonocr.verify_word("Python", "C:/project_folder/project_files/image_file.png")``` As above, but the file path is provided as an absolute path.

# PythonOCR

PythonOCR module for finding and locating words on screen, in image files or PDF files.

**NOTE:** PythonOCR is unreliable at best when finding words in files, and should only be used as an assistance to process files. Usage of other confirmation methods (such as manual labor) is adviced, when processing important files!

## Prerequisites

PythonOCR utilizes the following modules:

**pyautogui** for taking screenshots and mouse controls.

**poppler** to read, render and modify PDF files.

**pdf2image** to convert PDF files to image files. pdf2image is a wrapper around poppler.

**pytesseract** to recognize text in image files. pytesseract requires Tesseract OCR in order to function.

### Python

Install Python (3.7+) and include pip with the installation. **Add Python to PATH.**

Download Python: https://www.python.org/downloads/

### pyautogui

Install pyautogui using pip:

```
pip install pyautogui
```

More information at: https://pypi.org/project/PyAutoGUI/

### poppler

**Windows:**

Download the latest poppler release (.zip file) from: https://github.com/oschwartz10612/poppler-windows/releases/

More information at: https://github.com/oschwartz10612/poppler-windows

1. Unzip the poppler release file.

2. Add the poppler folder ('poppler-xx') to your Program Files. (For example, to: ```C:\Program Files (x86)\Poppler\ ```.)

3. Include the 'poppler-xx\bin' folder as a SYSTEM PATH environment variable. (For example, add: ```C:\Program Files (x86)\Poppler\poppler-0.90.1\bin``` to PATH.)

**Linux:**

**NOTE:** Installing poppler is not be neccessarily needed, if ```pdftoppm``` and ```pdftocairo``` are installed.

To install poppler on Ubuntu:

```
sudo apt install poppler-utils
```

More information at: https://pdf2image.readthedocs.io/en/latest/installation.html

### pdf2image

**NOTE:** Install poppler before installing pdf2image!

Install pdf2image using pip:

```
pip install pdf2image
```

More information at: https://pypi.org/project/pdf2image/ and https://github.com/Belval/pdf2image

### Tesseract OCR

More information at: https://github.com/tesseract-ocr/tessdoc

**Windows:**

Install Google Tesseract OCR and include Finnish. **Add Tesseract-OCR to PATH.**

Download Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

**Linux:**

Install Tesseract OCR using the command:

```
sudo apt install tesseract-ocr
```

### pytesseract

**NOTE:** Install Tesseract OCR before installing pytesseract!

Install pytesseract using pip:

```
pip install pytesseract
```

More information at: https://pypi.org/project/pytesseract/

**Permission Error (Linux):**

If the attempt to install pytesseract on Linux resulted in Permission error, you can attempt to install pytesseract on access-level where you have persmissions.

To install to a user-specific directory, use ```--user``` flag. For example, to install pytesseract to user-specific directory as Python 3.7 module:

```
python3.7 -m pip install --user pytesseract
```

## Installing

Install QAutoLibrary containing PythonOCR.py module.

QAutoLibrary download and installation instructions: https://github.com/QAutofamily/QAutoLibrary

## Usage

Import PythonOCR module from QAutoLibrary to your code:

```
from QAutoLibrary import PythonOCR
```

PythonOCR functions can then be used as follows:

```
PythonOCR.click_word(<word>)

PythonOCR.find_words(<word>, <file path>)

PythonOCR.find_coordinates(<word>, <file path>)

PythonOCR.verify_word(<word>, <file path>)
```

Detailed examples of how to use each of these functions are provided in **Functions** section.

### Usage in QAutoRobot

Work in progress...

## Functions

Main functions of PythonOCR library are: click_word(), find_word(), find_coordinates(), verify_word().

**NOTE:** Provide file paths and directory paths in string format to function parameters. Include file type endings, such as '.jpg' or '.png', when providing file paths.

### Function: click_word()

Function takes a screenshot of the screen and searches for a specified word in it. If a single instance of the word is found, moves cursor to the coordinates of the word and clicks the location. Optionally, screenshot can be saved as a file.

If multiple instances of the word are found, a specific one can be selected by index to be clicked. By default, does not click any found word, if multiple instances are found.

**NOTE:** When using this function as a keyword in Robot, providing a value for parameter ```index``` is recommended!

**Parameters:** ```click_word(word, save_screenshot_as, index)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```save_screenshot_as```: Optional. File name in string format for saving the screenshot. MUST include valid file type ending, such as '.jpg' or '.png'. In addition, may include absolute path or relative directory path to current project folder, where the screenshot is saved at. By default, or if empty, screenshot is not saved.

```index```: Optional. Index of the specific found word, in integer format. First found instance of the word is at position 0 (zero). By default, or if less than 0, no instance will be chosen and none of the multiple found words will be clicked.

**Examples:**

```PythonOCR.click_word("Python")``` Searches for word 'Python' on screen and if a single instance is found, clicks its location. Screenshot is not saved.

```PythonOCR.click_word("Python", "screenshot.png")``` As above, but the screenshot is saved to the current project directory as 'screenshot.png'.

```PythonOCR.click_word("Python", "./screenshots/screenshot.png")``` As above, but the screenshot is saved to 'screenshots' folder in the current project directory.

```PythonOCR.click_word("Python", "C:/project_folder/screenshots/screenshot.png")``` As above, but the screenshot is saved to the specific directory.

```PythonOCR.click_word("Python", index=0)``` Searches for the word on screen and if finds multiple instances of the word, clicks the first found instance (at index position 0 (zero)). Screenshot is not saved.

### Function: find_words()

Function searches for all instances of a specific word in image or PDF file. Converts a PDF file to image(s) in order to locate the instances of the word. Able to handle '.jpg', '.jpeg', '.png', and '.pdf' files.

**Parameters:** ```find_words(word, file_path, output_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```file_path```: Required. Image or PDF file path in string format. Can be absolute or relative to the current project directory.

```output_path```: Output directory in string format for image files converted from the PDF file. Not required if processing image files. By default, current project directory.

**Returns:**

A list of found instances of the word as a list of dictionaries. Each dictionary consisting of: {"text": found text, "page": page number}.

**Examples:**

```PythonOCR.find_words("Python", "image_file.png")``` Returns all found instances of the word 'Python' in 'image_file.png'.

```results_list = PythonOCR.find_words("Python", "image_file.png")``` As above, but the results are assigned to 'results_list' variable.

```print(PythonOCR.find_words("Python", "image_file.png"))``` As above, but the results are printed to console.

```PythonOCR.find_words("Python", "./project_files/image_file.png")``` Returns all found instances of the word in 'image_file.png' located in 'project_files' folder in the current project directory.

```PythonOCR.find_words("Python", "pdf_file.pdf")``` Returns all found instances of the word 'Python' in 'pdf_file.pdf'. Images converted from the PDF file are saved to the current project directory.

```PythonOCR.find_words("Python", "pdf_file.pdf", "./output")``` As above, but images are saved to 'output' folder in the current project directory.

```PythonOCR.find_words("Python", "C:/projet_folder/pdf_file.pdf", "C:/project_folder/output")``` As above, but file path and output folder for images are provided as absolute file paths.

### Function: find_coordinates()

Function searches for all instances of a specified word and their coordinates in image or PDF file. Converts PDF file to image(s) in order to locate instances of the word. Able to handle '.jpg', '.jpeg', '.png', and '.pdf' files.

**Parameters:** ```find_coordinates(word, file_path, output_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```file_path```: Required. Image or PDF file path in string format. Can be absolute or relative to the current project directory.

```output_path```: Output directory in string format for image files converted from the PDF file. Not required if processing image files. By default, current project directory.

**Returns:**

A list of found instances of the word and their coordinates as a list of dictionaries. Each dictionary consisting of: {"text": found text, "left": left coordinates, "top": top coordinates, "width": text width, "height": text height, "page": page number}.

**Examples:**

```PythonOCR.find_coordinates("Python", "image_file.png")``` Returns all instances of the word 'Python' and their coordinates in 'image_file.png'.

```results_list = PythonOCR.find_coordinates("Python", "image_file.png")``` As above, but the results are assigned to 'results_list' variable.

```print(PythonOCR.find_coordinates("Python", "image_file.png"))``` As above, but the results are printed to console.

```PythonOCR.find_coordinates("Python", "./project_files/image_file.png")``` Returns all found instances of the word and their coordinates in 'image_file.png' located in 'project_files' folder in the current project directory.

```PythonOCR.find_coordinates("Python", "pdf_file.pdf")``` Returns all found instances of the word 'Python' and their coordinates in 'pdf_file.pdf'. Images converted from the PDF file are saved to the current project directory.

```PythonOCR.find_coordinates("Python", "pdf_file.pdf", "./output")``` As above, but images are saved to 'output' folder in the current project directory.

```PythonOCR.find_coordinates("Python", "C:/projet_folder/pdf_file.pdf", "C:/project_folder/output")``` As above, but file path and output folder for images are provided as absolute file paths.

### Function: verify_word()

Function searches for any instances of a specified word in image file. Able to handle '.jpg', '.jpeg', and '.png' files.

**Parameters:** ```verify_word(word, image_path)```

```word```: Required. The specified word in string format. Upper and lowercase sensitive!

```image_path```: Required. Image file path in string format. Can be absolute or relative to the current project directory.

**Returns:**

Bool: True if found at least one instance of the specified word, False if none.

**Examples:**

```PythonOCR.verify_word("Python", "image_file.png")``` Returns True or False if finds any instances of the word 'Python' in 'image_file.png'.

```found_word = PythonOCR.verify_word("Python", "image_file.png")``` As above, but the result is assigned to 'found_word' variable.

```print(PythonOCR.verify_word("Python", "image_file.png"))``` As above, but the result is printed to console.

```PythonOCR.verify_word("Python", "./project_files/image_file.png")``` Returns the result regarding the 'image_file.png' located in 'project_files' folder in the current project directory.

```PythonOCR.verify_word("Python", "C:/project_folder/project_files/image_file.png")``` As above, but the file path is provided as an absolute path.

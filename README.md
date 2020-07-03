# pythonOCR

Library for finding and locating words in PDF or image files.

## Prerequisites

PythonOCR utilizes Tesseract OCR to recognize text in image files. pdf2image is used to convert PDF files into images.

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

### Tesseract OCR

Install Tesseract OCR and include Finnish. Add it to PATH.

Download Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

More information at: https://github.com/tesseract-ocr/tessdoc

### pytesseract

Install pytesseract using pip:

```
pip install pytesseract
```

More infromation at: https://pypi.org/project/pytesseract/

## Installing

WIP Download pythonOCR.

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
my_object.find_words(<word>, <file path>)

my_object.find_coordinates(<word>, <file path>)

my_object.verify_word(<word>, <file path>)
```

Example:

```
print(
  my_object.find_words("Example", "my_file.pdf")
  )
```

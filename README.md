# pythonOCR

Requirements:

-pytesseract https://pypi.org/project/pytesseract/

-pdf2image https://pypi.org/project/pdf2image/

-Tesseract https://github.com/UB-Mannheim/tesseract/wiki (Windows 64-bit)

-Poppler for Windows (included in bin directory)

When installing Tesseract, include Finnish.

Add Tesseract to PATH (Usually C:\Users\<User>\AppData\Local\Tesseract-OCR)

# pythonOCR

Description. ...for finding and locating words in PDF or image files.


### Prerequisites

**Python**

Install Python (3.5+), add it to PATH and include pip with the installation.

https://www.python.org/downloads/

pip

**pdf2image**

Install pdf2image using pip:

```
pip install pdf2image
```

https://pypi.org/project/pdf2image/

_NOTE:_ poppler will be included in the /bin directory.

**Google Tesseract OCR**

Install Tesseract OCR and include Finnish. Add it to PATH.

**pytesseract**

Install pytesseract using pip:

```
pip install pytesseract
```

https://pypi.org/project/pytesseract/


### Installing


## Usage

In your code, create a class object:

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
my_object.find_words("", "my_file.pdf")
```

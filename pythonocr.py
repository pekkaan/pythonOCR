"""
PythonOCR contains functions for finding and locating words on screen, in image files or PDF files.

Main functions:

    click_word(): Searches for a word on screen and clicks its location.

    find_words(): Searches for all instances of a word in image or PDF file.

    find_coordinates(): Searches for all instances of a word and their coordinates in image or PDF file.

    verify_word(): Verifies, if image file contains any instance of a word.

"""

import warnings

import pyautogui

import pytesseract
from pytesseract import Output

import pdf2image
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

"""
FOR DEVELOPERS:

PythonOCR internal functions are located at the beginning of this file (below), and main functions are located
after them. PythonOCR exceptions are located at the end of this file.

When applying changes to this file, remember to update the documentation accordingly! Update function descriptions
in this file (file description and function descriptions), and update the README file in git (pythonOCR and
QAutoLibrary).

Internal functions:

    _get_word_coordinate_from_data(): Retrieves the data of found instances of a word and their coordinates
                                      from image data.

    _is_valid_image(): Checks if given file is a valid image file.

    _is_valid_pdf(): Checks if given file is a PDF file.

    _validate_file(): Verifies that a given file is image or PDF file, converts PDF file to image(s)
                      and returns image files.

    _click_coordinates(): Moves mouse cursor on screen to the provided coordinates, and clicks the location.

Exceptions:

    PythonOCRError: Base error class for PythonOCR errors.

    InvalidFileTypeError: Error raised when given file is not a valid image nor PDF file.

    InvalidImageTypeError: Error raised when given file is not a valid image file.

"""


# INTERNAL FUNCTIONS:
def _get_word_coordinates_from_data(word, image_data, page_number=0):
    """
    Internal function. Retrieves the data of found instances of a specified word and their coordinates from given data.

    :param word: Required. The specified word.
    :param image_data: Required. Given image data, such as data retrieved by pytesseract.
                       Must be a dictionary of lists.
    :param page_number: Optional. Page number to be included with the returned data. If 0 (zero) or less,
                        page number is not included in the returned data. By default, 0.
    :return: Found instances of the word and their coordinates in image.
             A list of tuples, each element consisting of: (found text, left coordinates (X), top coordinates (Y),
             text width, text height, page number (Optional)).
    """
    results = []
    # 'image_data' is a dictionary of lists.
    # Accessing specific data list in dictionary:  image_data[<dictionary_key>]
    # Accessing specific data in a list, by index: image_data[<dictionary_key>][<index>]
    number_of_items = len(image_data["level"])
    for index in range(number_of_items):
        text = image_data["text"][index]

        if word in text:
            x_coord = image_data["left"][index]
            y_coord = image_data["top"][index]
            width = image_data["width"][index]
            height = image_data["height"][index]

            if page_number <= 0:
                results.append((text, x_coord, y_coord, width, height))
            elif page_number > 0:
                results.append((text, x_coord, y_coord, width, height, page_number))
    return results


def _is_valid_image(file_path):
    """
    Internal function. Checks if given file is .jpg, .jpeg or .png file.
    """
    if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        return True
    else:
        return False


def _is_valid_pdf(file_path):
    """
    Internal function. Checks if given file is .pdf file.
    """
    if file_path.endswith(".pdf"):
        return True
    else:
        return False


def _validate_file(file_path, output_path):
    """
    Internal function. Verifies that a given file is a valid image file or PDF file. Converts a PDF file to images:
    each page into its own image file. Returns image(s).

    :return: A list of image files.
    """
    image_list = []
    if _is_valid_image(file_path):
        image_list.append(file_path)
    elif _is_valid_pdf(file_path):
        image_list = pdf2image.convert_from_path(file_path, fmt="jpeg", output_folder=output_path)
    else:
        raise InvalidFileTypeError("Could not recognize '{file}' as a .jpg, .jpeg, .png nor .pdf file!"
                                   .format(file=file_path))
    return image_list


def _click_coordinates(data_list, element_index=0):
    """
    Internal function. Moves mouse cursor on screen to coordinates retrieved from data, and clicks the location.
    If data contains multiple elements and their coordinates, specific coordinates can be chosen by index.

    :param data_list: Required. Data as a list of tuples. Elements must consist of: (found text, left coordinates (X),
                      top coordinates (Y), text width, text height)
    :type data_list: list
    :param element_index: Optional. Index of the data element. By default, 0 (zero; first element).
    :type element_index: int
    """
    # Element in 'data_list' consists of: (text, left coordinates (X), top coordinates (Y), text width, text height)
    x_coordinate = data_list[element_index][1] + data_list[element_index][3] / 2
    y_coordinate = data_list[element_index][2] + data_list[element_index][4] / 2
    pyautogui.moveTo(x_coordinate, y_coordinate, duration=0)
    pyautogui.click()


# MAIN FUNCTIONS:
def click_word(word, save_screenshot_as="", index=-1):
    """
    Searches for a specified word on screen and clicks the word's location. Takes a screenshot using pyautogui
    and recognizes text in it with pytesseract. Optionally, can save screenshot as a specified image file.

    If able to find a single instance of the word, retrieves its coordinates and clicks the location with mouse,
    using pyautogui. If multiple instances of the word are found, a specific one can be selected to be clicked by
    its index. By default, does not click any found word, if multiple instances are found.

    :param word: Required. The specified word. Upper and lowercase sensitive!
    :type word: str
    :param save_screenshot_as: Optional. File name for saved screenshot. File type, such as .jog or .png, MUST be
                               included in the file name! Argument can include absolute path or relative directory
                               path to current project folder, where screenshot is saved at, in addition to the
                               file name. By default, or if empty, screenshot is not saved.
    :type save_screenshot_as: str
    :param index: Optional. Index of a specific found word. First found instance of the word is at position 0 (zero).
                  By default, or if less than 0, no instance will be chosen and none of the multiple found words will
                  be clicked.
    :type index: int

    ----------

    Examples:

    click_word("Python") - Searches and clicks the word 'Python' on screen.

    click_word("Python", "./screenshots/screenshot.png") - Searches and clicks the word, and saves the
    screenshot as 'screenshot.png' to the folder 'screenshots' in the project directory.

    click_word("Python", index=0) - Searches and clicks the first instance of the word 'Python' on screen.
    """
    screenshot = pyautogui.screenshot()
    if save_screenshot_as:
        # PyAutoGUI uses Pillow (or PIL) module for image-related features, such as saving an image.
        screenshot.save(save_screenshot_as)

    image_data = pytesseract.image_to_data(screenshot, lang="eng+fin", output_type=Output.DICT)

    results = _get_word_coordinates_from_data(word, image_data)

    if len(results) == 1:
        _click_coordinates(results)

    elif len(results) > 1:
        if index > -1:
            _click_coordinates(results, index)

        warning_message = "pythonocr.click_word({param}): Found multiple instances ({amount}) of the word '{param}' " \
                          "on screen!".format(param=word, amount=len(results))
        warnings.warn(warning_message, RuntimeWarning)

    else:
        print("pythonocr.click_word({param}): Found no instances of the word '{param}' on screen."
              .format(param=word))


def find_words(word, file_path, output_path="./"):
    """
    Searches for all instances of a specified word in image or PDF file.
    Converts a PDF file to image(s), and recognizes the text in image(s) with pytesseract.

    :param word: Required. The specified word. Upper and lowercase sensitive!
    :type word: str
    :param file_path: Required. Image or PDF file path. Can be absolute or relative to the current project directory.
    :type file_path: str
    :param output_path: Output directory for image files converted from the PDF file. Not required if processing
                        image files. By default, current project directory.
    :type output_path: str
    :return: A list of found instances of the specified word.
             A list of tuples, each element consisting of: (found text, page number).
    :rtype: list

    ----------

    Examples:

    find_words("Python", "image_file.png") - Returns the found instances of the word 'Python' from the file
    'image_file.png'.

    find_words("Python", "./project_files/pdf_file.pdf", "./output_folder") - Returns the found instances of the word
    from file 'pdf_file.pdf' located in the folder 'project_files' in the project directory.  Converted images are
    saved to the folder 'output_folder'.
    """
    image_list = _validate_file(file_path, output_path)
    results = []
    page_number = 1

    for image in image_list:
        text_in_image = pytesseract.image_to_string(image, lang="eng+fin")

        # In order to find multiple instances of the word in text,
        # "if word in text_in_image:" is not sufficient.
        text_array = text_in_image.splitlines()
        for line in text_array:
            if word in line:
                results.append((line, page_number))
        page_number += 1
    return results


def find_coordinates(word, file_path, output_path="./"):
    """
    Searches for all instances of a specified word and their coordinates in image or PDF file.
    Converts a PDF file to image(s), and recognizes the text in image(s) with pytesseract.

    :param word: Required. The specified word. Upper and lowercase sensitive!
    :type word: str
    :param file_path: Required. Image or PDF file path. Can be absolute or relative to the current project directory.
    :type file_path: str
    :param output_path: Optional. Output directory for image files converted from the PDF file.
                        By default, current project directory.
    :type output_path: str
    :return: Found instances of the word and their coordinates in image.
             A list of tuples, each element consisting of: (found text, left coordinates (X), top coordinates (Y),
             text width, text height, page number).
    :rtype: list

    ----------

    Examples:

    find_coordinates("Python", "image_file.png") - Returns the found instances of the word 'Python' and their
    coordinates from the file 'image_file.png'.

    find_coordinates("Python", "./project_files/pdf_file.pdf", "./output_folder") - Returns the found instances
    of the word and their coordinates from file 'pdf_file.pdf' located in the folder 'project_files' in the
    project directory. Converted images are saved to the folder 'output_folder'.
    """
    image_list = _validate_file(file_path, output_path)
    results = []
    page_number = 1

    for image in image_list:
        image_data = pytesseract.image_to_data(image, lang="eng+fin", output_type=Output.DICT)

        results.extend(_get_word_coordinates_from_data(word, image_data, page_number))
        page_number += 1
    return results


def verify_word(word, image_path):
    """
    Searches for any instance of a specified word in image file. Recognizes the text in image with pytesseract.

    :param word: Required. The specified word. Upper and lowercase sensitive!
    :type word: str
    :param image_path: Required. Image file path. Can be absolute or relative to the current project directory.
    :type image_path: str
    :return: Returns True if found at least one instance of the specified word in image, False if none.
    :rtype: bool

    ----------

    Examples:

    verify_word("Python", "image_file.png") - Returns whether or not the word 'Python' was found from file
    'image_file.png'.

    verify_word("Python", "./project_files/image_file.png") - Returns whether or not the word was found from file
    'image_file.png' in the folder 'project_files' in the project directory.
    """
    if not _is_valid_image(image_path):
        raise InvalidImageTypeError("Could not recognize '{file}' as a .jpg, .jpeg nor .png image file!"
                                    .format(file=image_path))

    text_in_image = pytesseract.image_to_string(image_path, lang="eng+fin")
    if word in text_in_image:
        return True
    else:
        return False


# EXCEPTIONS:
class PythonOCRError(Exception):
    """Base error class for PythonOCR errors."""
    def __init__(self, message):
        super().__init__(message)


class InvalidFileTypeError(PythonOCRError):
    """Error raised when given file is not a valid image nor PDF file."""
    pass


class InvalidImageTypeError(InvalidFileTypeError):
    """Error raised when given file is not a valid image file."""
    pass

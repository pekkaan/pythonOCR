"""
PythonOCR contains functions for finding and locating words on screen, in image files or PDF files.

Main functions:

    click_word(): Searches for a word on screen and clicks it's location.

    find_words(): Searches for all instances of a word in image or PDF file.

    find_coordinates(): Searches for all instances of a word and their coordinates in image or PDF file.

    verify_word(): Verifies, if image file contains any instance of a word.

"""

import inspect
import os.path

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

Python OCR main functions can be found at the end of this file, internal functions are located before them.

Internal functions:

    _get_word_coordinate_from_data(): Retrieves the data of found instances of a word and their coordinates
                                      from image data.

    _get_poppler_path(): Returns directory path of poppler files.

    _is_image(): Checks if given file is valid image file.

    _validate_file(): Verifies that a given file is image or PDF file, converts PDF file to image(s)
                      and returns image files.

"""


def _get_word_coordinates_from_data(word, image_data, page_number=0):
    """
    Internal function. Retrieves the data of found instances of a specified word and their coordinates from given data.

    :param word: The specified word. Required.
    :param image_data: Given image data, such as data retrieved by pytesseract. Required.
                       Must be a dictionary of lists.
    :param page_number: Page number to be included with the returned data. Optional. If 0 (zero) or less,
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


def _get_poppler_path():
    """
    Internal function. Returns directory path of poppler files, should be: .../pythonocr/bin
    """
    this_file = inspect.getframeinfo(inspect.currentframe()).filename
    this_path = os.path.dirname(os.path.abspath(this_file))
    return os.path.join(this_path, "bin")


def _is_image(file_path):
    """
    Internal function. Checks if given file is .jpg, .jpeg or .png file.
    """
    if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        return True
    else:
        return False


def _validate_file(file_path, output_path):
    """
    Internal function. Verifies that a given file is .jpg, .jpeg, .png or .pdf file, and returns valid image files.
    Converts a PDF file to images: each page into its own image file.

    :return: A list of image files. Returns None if file is not .jpg, .jpeg, .png nor .pdf file.
    """
    image_list = []
    if _is_image(file_path):
        image_list.append(file_path)
    elif file_path.endswith(".pdf"):
        image_list = pdf2image.convert_from_path(file_path, fmt="jpeg",
                                                 output_folder=output_path,
                                                 poppler_path=_get_poppler_path())
    else:
        return None
    return image_list


# MAIN FUNCTIONS:
def click_word(word, save_screenshot_as=""):
    """
    Searches for a specified word on screen and clicks the word's location. Takes a screenshot using pyautogui
    and recognizes text in it with pytesseract. Optionally, can save screenshot as a specified .png file.

    If able to find a single instance of the word, retrieves it's coordinates and clicks the location with mouse,
    using pyautogui. Unable to click the word's location if multiple instances of the word are found on screen!

    :param word: The specified word. Required. Upper and lowercase sensitive!
    :type word: str
    :param save_screenshot_as: File name for saved screenshot. Optional. File type, such as .jog or .png, MUST be
                               included in the file name! Parameter can include absolute path or relative directory
                               path to current project folder, where screenshot is saved at, in addition to the
                               file name. By default, or if empty, screenshot is not saved.
    :type save_screenshot_as: str
    """
    screenshot = pyautogui.screenshot()
    if save_screenshot_as:
        # PyAutoGUI uses Pillow (or PIL) module for image-related features, such as saving an image.
        screenshot.save(save_screenshot_as)

    image_data = pytesseract.image_to_data(screenshot, lang="eng+fin", output_type=Output.DICT)

    results = _get_word_coordinates_from_data(word, image_data)

    if len(results) == 1:
        # Element in 'results' consists of: (text, left coordinates (X), top coordinates (Y), text width, text height)
        x_coordinate = results[0][1] + results[0][3]/2
        y_coordinate = results[0][2] + results[0][4]/2
        pyautogui.moveTo(x_coordinate, y_coordinate, duration=0)
        pyautogui.click()

    elif len(results) > 1:
        print("pythonocr.click_word({param}): Found multiple instances of the word '{param}' on screen!"
              .format(param=word))

    else:
        print("pythonocr.click_word({param}): Found no instances of the word '{param}' on screen."
              .format(param=word))


def find_words(word, file_path, output_path="./"):
    """
    Searches for all instances of a specified word in image or PDF file.
    Converts a PDF file to image(s), and recognizes the text in image(s) with pytesseract.

    :param word: The specified word. Required. Upper and lowercase sensitive!
    :type word: str
    :param file_path: Image or PDF file path. Required. Can be absolute or relative to the current project directory.
    :type file_path: str
    :param output_path: Output directory for image files converted from the PDF file. Not required if processing
                        image files. By default, current project directory.
    :type output_path: str
    :return: A list of found instances of the specified word.
             A list of tuples, each element consisting of: (found text, page number).
             Returns None if file is not .pdf, .jpg, .jpeg nor .png file.
    :rtype: list
    """
    image_list = _validate_file(file_path, output_path)
    if not image_list:
        return None

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

    :param word: The specified word. Required. Upper and lowercase sensitive!
    :type word: str
    :param file_path: Image or PDF file path. Required. Can be absolute or relative to the current project directory.
    :type file_path: str
    :param output_path: Output directory for image files converted from the PDF file.
                        By default, current project directory.
    :type output_path: str
    :return: Found instances of the word and their coordinates in image.
             A list of tuples, each element consisting of: (found text, left coordinates (X), top coordinates (Y),
             text width, text height, page number).
             Returns None if file is not .pdf, .jpg, .jpeg nor .png file.
    :rtype: list
    """
    image_list = _validate_file(file_path, output_path)
    if not image_list:
        return None

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

    :param word: The specified word. Required. Upper and lowercase sensitive!
    :type word: str
    :param image_path: Image file path. Required. Can be absolute or relative to the current project directory.
    :type image_path: str
    :return: Returns True if found at least one instance of the specified word in image, False if none.
             Returns None if image is not .jpg, .jpeg nor .png file.
    :rtype: bool
    """
    if not _is_image(image_path):
        return None
    text_in_image = pytesseract.image_to_string(image_path, lang="eng+fin")
    if word in text_in_image:
        return True
    else:
        return False

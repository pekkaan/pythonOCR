import inspect
import os.path
import pdf2image
import pyautogui
import pytesseract
from pytesseract import Output
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


class PythonOCR:
    """
    PythonOCR class contains methods for finding and locating words in PDF or image files.

    Class methods:

    click_word: Searches for a word on screen and clicks it's location.

    find_words: Searches for a word in PDF or image file.

    find_coordinates: Searches for a word and it's coordinates in PDF or image file.

    verify_word: Verifies, if image file contains any instance of a word.

    (Other class methods are intended to be used by these main methods.)
    """

    def get_this_dir(self):
        """
        :return: PythonOCR directory.
        """
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        return os.path.dirname(os.path.abspath(filename))

    def is_image(self, file_path):
        if ".jpg" or ".jpeg" or ".png" in file_path:
            return True
        else:
            return False

    # DEPRECATED METHOD
    def clean_line(self, line, word):
        """
        Cleans the text in 'line' by cutting extra characters and words before
        and after the specified word.
        Precondition: 'line' must contain 'word'.

        :return: Text line.
        """
        # Get index of the last space, " ", before the word.
        new_beginning = line.find(word)
        index = line.find(word)
        while index >= 0 and line[index] != " ":
            new_beginning = index
            index -= 1

        # Get index of the next space, " ", after the word.
        new_end = len(line)
        if line.find(" ", new_beginning) != -1:
            new_end = line.find(" ", new_beginning)

        return line[new_beginning:new_end]

    def validate_file(self, file_path, output_path):
        """
        Verifies that a given filename is .jpg, .jpeg, .png or .pdf -file.
        Converts PDF-file to images: each page into its own image. Returns valid image(s).

        :return: A list of image files.
        """
        images = []
        if not self.is_image(file_path) and ".pdf" not in file_path:
            return
        elif self.is_image(file_path):
            images.append(file_path)
        elif ".pdf" in file_path:
            # Get the pythonOCR (this) directory, as passing poppler files directory to pdf2image relies on it.
            poppler_directory = os.path.join(self.get_this_dir(), "bin")

            # Variable 'images' will be an array of images from the pages of PDF-file.
            # Array elements of 'images' will be image file paths.
            images = pdf2image.convert_from_path(file_path, fmt="jpeg",
                                                 output_folder=output_path,
                                                 poppler_path=poppler_directory
                                                 )
        return images

    # MAIN METHODS:
    def click_word(self, word):
        """
        Locates a specified word on screen and clicks the word's location. Takes a screenshot using pyautogui
        and recognizes text in it with pytesseract. If able to find a single instance of the word, retrieves it's
        coordinates and clicks the location with mouse, using pyautogui.
        Unable to click the word's location if multiple instances of the word are found on screen.

        :param word: The specified word. Required. Upper and lowercase sensitive!
        """
        found_single_instance = False
        x_coord = 0
        y_coord = 0
        width = 0
        height = 0

        screenshot = pyautogui.screenshot()
        image_data = pytesseract.image_to_data(screenshot, lang="eng+fin", output_type=Output.DICT)
        # Image data is a dictionary of lists.
        # Accessing specific data list in dictionary:  image_data[<dictionary_key>]
        # Accessing specific data in a list, by index: image_data[<dictionary_key>][<index>]
        number_of_items = len(image_data["level"])
        for index in range(number_of_items):
            text = image_data["text"][index]

            if word in text and not found_single_instance:
                x_coord = image_data["left"][index]
                y_coord = image_data["top"][index]
                width = image_data["width"][index]
                height = image_data["height"][index]
                found_single_instance = True

            elif word in text and found_single_instance:
                print("PythonOCR method: click_word({param}): Found multiple instances of the word ({param}) on screen!"
                      .format(param=word))
                return

        # Click coordinates.
        if found_single_instance:
            pyautogui.moveTo(x_coord + width/2, y_coord + height/2, 0)
            pyautogui.click()

    def find_words(self, word, file_path, output_path="./"):
        """
        Searches for all instances of a specified word in PDF or image file.
        Converts a PDF-file to image(s), and recognizes the text in image(s) with pytesseract.

        :param word: The specified word. Required. Upper and lowercase sensitive!
        :type word: str
        :param file_path: PDF or image file path. Can be absolute or relative to pythonOCR directory. Required.
        :type file_path: str
        :param output_path: Output directory for image files. Recommended if processing a PDF file,
        by default pythonOCR directory.
        :type output_path: str
        :return: A list of found instances of the specified word.
                A list of tuples, consisting of: (found text, page number).
                Returns None if file is not a .pdf, .jpg, .jpeg nor .png -file.
        :rtype: list
        """
        images = self.validate_file(file_path, output_path)
        if not images:
            return

        results = []
        page_number = 1
        for image in images:
            text_in_image = pytesseract.image_to_string(image, lang="eng+fin")

            # In order to find multiple instances of the word in text,
            # "if word in text_in_image:" is not sufficient.
            text_array = text_in_image.splitlines()
            for line in text_array:
                if word in line:
                    # Clean the line where the word was found.  DEPRECATED
                    # cleaned_line = self.clean_line(line, word)  DEPRECATED
                    results.append((line, page_number))
            page_number += 1
        return results

    def find_coordinates(self, word, file_path, output_path="./"):
        """
        Searches for all instances of a specified word and it's coordinates in PDF or image file.
        Converts a PDF-file to image(s), and recognizes the text in image(s) with pytesseract.

        :param word: The specified word. Required. Upper and lowercase sensitive!
        :type word: str
        :param file_path: PDF or image file path. Can be absolute or relative to pythonOCR directory. Required.
        :type file_path: str
        :param output_path: Output directory for image files. Recommended if processing a PDF file,
        by default pythonOCR directory.
        :type output_path: str
        :return: Found instances of the word and their coordinates in image.
                A list of tuples, consisting of: (found text, left coordinates (X), top coordinates (Y),
                text width, text height, page number).
                Returns None if file is not a .pdf, .jpg, .jpeg nor .png -file.
        :rtype: list
        """
        images = self.validate_file(file_path, output_path)
        if not images:
            return

        results = []
        page_number = 1
        for image in images:
            image_data = pytesseract.image_to_data(image, lang="eng+fin", output_type=Output.DICT)
            # Image data is a dictionary of lists.
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

                    results.append((text, x_coord, y_coord, width, height, page_number))
                    # Keskipisteen laskeminen ja vieminen 'results'-listaan:
                    # results.append((text, x_coord, y_coord, x_coord + width/2, y_coord + height/2, page_number))
            page_number += 1
        return results

    def verify_word(self, word, image_path):
        """
        Searches any instance of a specified word in image file.
        Recognizes the text in image with pytesseract.

        :param word: The specified word. Required. Upper and lowercase sensitive!
        :type word: str
        :param image_path: Image file path. Can be absolute or relative to pythonOCR directory. Required.
        :type image_path: str
        :return: Returns True if found at least one instance of specified word in image, False if none.
                Returns None if image is not a .jpg, .jpeg nor .png -file.
        :rtype: bool
        """
        if not self.is_image(image_path):
            return
        text_in_image = pytesseract.image_to_string(image_path, lang="eng+fin")
        if word in text_in_image:
            return True
        else:
            return False

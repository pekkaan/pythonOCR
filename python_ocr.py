import os
import pdf2image
import pytesseract
from pytesseract import Output
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


class PythonOCR:
    """
    PythonOCR class contains functions for finding and locating words in PDF or image files.

    Class functions:

    find_words: Searches for a word in PDF or image file.

    find_coordinates: Searches for a word and it's coordinates in PDF or image file.

    verify_word: Verifies, if image file contains any instance of a word.

    (Other class functions are intended to be used by these main functions.)
    """

    def is_image(self, file_path):
        if ".jpg" or ".jpeg" or ".png" in file_path:
            return True
        else:
            return False

    def clean_line(self, line, word):
        """
        Cleans the text in 'line' by cutting extra characters and words before
        and after the specified word.
        Precondition: 'line' must contain 'word'.
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

    def validate_file(self, file_path):
        """
        Verifies that a given filename is .jpg, .jpeg, .png or .pdf -file.
        Converts PDF-file to a list of images.
        """
        images = []
        if not self.is_image(file_path) and ".pdf" not in file_path:
            return
        elif ".pdf" in file_path:
            images_output = os.path.join(os.getcwd(), "images")
            bin_path = os.path.join(os.getcwd(), "bin")
            # Variable 'images' will be an array of images from the pages of PDF-file.
            # Array elements of 'images' will be image file paths.
            images = pdf2image.convert_from_path(file_path, fmt="jpeg", output_folder=images_output, poppler_path=bin_path)
        elif self.is_image(file_path):
            images = file_path
        return images

    # MAIN FUNCTIONS:
    def find_words(self, word, file_path):
        """
        Searches for all instances of a specified word in PDF or image file.
        Converts a PDF-file to image(s), and recognizes the text in image(s) with pytesseract.
        Returns None if file_path argument is not a .pdf, .jpg, .jpeg nor .png -file.

        :param word: The specified word. Required.
        :type word: str
        :param file_path: PDF or image file path. Required.
        :type file_path: str
        :return: A list of found instances of the specified word.
        :rtype: list
        """
        images = self.validate_file(file_path)
        if not images:
            return

        results = []
        for image in images:
            text_in_image = pytesseract.image_to_string(image, lang="eng")

            # In order to find multiple instances of the word in text,
            # "if word in text_in_image:" is not sufficient.
            text_array = text_in_image.splitlines()
            for line in text_array:
                if word in line:
                    # Clean the line where the word was found.
                    cleaned_line = self.clean_line(line, word)
                    results.append(cleaned_line)
        return results

    def find_coordinates(self, word, file_path):
        """
        Searches for all instances of a specified word and it's coordinates in PDF or image file.
        Converts a PDF-file to image(s), and recognizes the text in image(s) with pytesseract.
        Returns None if file_path argument is not a .pdf, .jpg, .jpeg nor .png -file.

        :param word: The specified word. Required.
        :type word: str
        :param file_path: PDF or image file path. Required.
        :type file_path: str
        :return: Found instances of the word and word coordinates in image.
            A list of tuples, containing (found text, left coordinates, top coordinates, text width, text height)
        :rtype: list
        """
        images = self.validate_file(file_path)
        if not images:
            return

        results = []
        for image in images:
            image_data = pytesseract.image_to_data(image, lang="eng", output_type=Output.DICT)
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

                    results.append((text, x_coord, y_coord, width, height))
                    # Keskipisteen laskeminen ja vieminen 'results'-listaan:
                    # results.append((text, x_coord + width/2, y_coord + height/2))
        return results

    def verify_word(self, word, image_path):
        """
        Searches any instance of a specified word in image file.
        Recognizes the text in image with pytesseract.
        Returns None if image_path argument is not a .jpg, .jpeg nor .png -file.

        :param word: The specified word. Required.
        :type word: str
        :param image_path: Image file path. Required.
        :type image_path: str
        :return: Returns True if found at least one instance of specified word in image, False if none.
        :rtype: bool
        """
        if not self.is_image(image_path):
            return
        text_in_image = pytesseract.image_to_string(image_path, lang="eng")
        if word in text_in_image:
            return True
        else:
            return False

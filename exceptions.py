"""
Defined exceptions specific to PythonOCR.
"""


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

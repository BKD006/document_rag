import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException

class DocumentCompare:
    def __init__(self):
        pass
    def delete_existing_file(self):
        """
        Deletes existing files at the specified paths.
        """
        pass
    def save_uploaded_files(self):
        """
        Saves uploaded files to a specified directory.
        """
        pass
    def read_pdf(self):
        """
        Reads a PDF file and extracts text from each page.
        """
        pass
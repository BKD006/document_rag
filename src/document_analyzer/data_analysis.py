import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzed documents using a pre-trained model.
    Automatically logs all actions and supports session-based organisation.
    """
    def __init__(self):
        self.model_loader=ModelLoader()
        self.logger=CustomLogger()
        self.output_parser=JsonOutputParser
        self.fixing_parser=OutputFixingParser.from_output_parser(self.output_parser)

    def analyze_metadata(self):
        pass
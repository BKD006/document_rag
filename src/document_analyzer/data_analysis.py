import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY

class DocumentAnalyzer:
    """
    Analyzed documents using a pre-trained model.
    Automatically logs all actions and supports session-based organisation.
    """
    def __init__(self):
        self.log= CustomLogger().get_logger(__name__)
        try:
          self.loader=ModelLoader()
          self.llm= self.loader.load_llm()

          #Prepare parsers
          self.parser= JsonOutputParser(pydantic_object=MetaData)
          self.fixing_parser= OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
          
          self.prompt= PROMPT_REGISTRY["document_analysis"]
          
          self.log.info("Document initialized successfully")
          

        except Exception as e:
            self.log.error(f"Error initializing DcoumenetAnalyzer", sys)
            raise DocumentalRagException("Error in DocumentAnalyzer initialization", sys)  

    def analyze_document(self, document_text:str)-> dict:
        try:
            chain= self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta-data analysis chain initialized")

            response= chain.invoke({
                "format_instruction": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            self.log.info("Metadata extraction successful", key=list(response.keys()))
            return response
        
        except Exception as e:
            self.log.error("Metadata analysis failed", error=str(e))
            raise DocumentalRagException("Metadata extraction failed") from e
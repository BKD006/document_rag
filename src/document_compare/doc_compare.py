import sys
from dotenv import load_dotenv
import pandas as pd
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentRAGException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentCompareLLM:
    def __init__(self):
        load_dotenv()
        self.loader= ModelLoader()
        self.llm= self.loader.load_llm()
        self.parser= JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser=OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
        self.prompt= PROMPT_REGISTRY[PromptType.DOCUMENT_COMPARISON.value]
        self.chain= self.prompt | self.llm | self.parser 
        log.info("DocumentCompareLLM has been initialized with model and parser.", model=self.llm)

    def compare_documents(self, combined_documents):
        """
        Compares two documents and returns a structured comparison.
        """
        try:
           inputs={
               "combined_docs": combined_documents,
               "format_instruction": self.parser.get_format_instructions()
           }
           log.info("Invoking document comparison LLM chain")
           response= self.chain.invoke(inputs)
           log.info("Document Comparison completed", response=str(response)[:200])
           return self.format_response(response)
        
        except Exception as e:
            log.error(f"Error in compare_documents", error=str(e))
            raise DocumentRAGException("Error comparing documents", sys)
        
    def format_response(self, response_parsed: list[dict])->pd.DataFrame:
        """
        Formats the response from the LLM into a structured format.
        """
        try:
            df= pd.DataFrame(response_parsed)
            log.info("Response formatted into DataFrame", dataframe=df)
            return df
        except Exception as e:
            log.error(f"Error formatting message in DataFrame: {e}")
            raise DocumentRAGException("Error formatting response", sys)
        
import uuid
from pathlib import Path
import sys
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException
from utils.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self):
        try:
            self.log=CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to initialize SingleDocIngestor", error=str(e))
            raise DocumentalRagException("Initialization error in SingleDocIngestor", sys)
        
    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error("Dcoument Ingestion failed", error=str(e))
            raise DocumentalRagException("Error during file ingestion", sys)
    
    def _create_retriver(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentalRagException("Error during retriever creation", sys)
        
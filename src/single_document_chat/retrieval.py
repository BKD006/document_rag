import sys
import os
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from utils.model_loader import ModelLoader
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConversationalRAG:
    def __init__(self, session_id: str, retriver)->None:
        try:
            self.log= CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Unable to initiate ConverstaionalRAG", error=str(e))
            raise DocumentalRagException("Failed to initialize ConversationalRAG", sys)
    
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error=str(e))
            raise DocumentalRagException("Failed to LLM", sys)
    
    def _get_session_history(self, session_id:str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to access session history", session_id=session_id, error=str(e))
            raise DocumentalRagException("Failed to retrieve session history", sys)
    
    def load_retriever_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", sys(e))
            raise DocumentalRagException("Failed to load retriever from FAISS", sys)
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke conversational RAG", error=str(e), session_id=self.session_id)
            raise DocumentalRagException("Failed to invoke RAG chain", sys)
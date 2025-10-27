import sys
import os
from operator import itemgetter
from typing import List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentRAGException
from logger import GLOBAL_LOGGER as log
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConversationalRAG:
    """
    LCEL-based Conversational RAG with retriever initialization.

    Usage:
        rag= ConversationalRAG(session_id="xyz")
        rag.load.retriever_from_faiss(index_path="faiss_index/xyz", k=5, index_name="index")
        answer= rag.invoke("Query", chat_history=[])
    """
    def __init__(self, session_id:str, retriever=None):
        try:
            self.session_id= session_id

            #Load LLM and prompts once
            self.llm=self._load_llm()
            self.contextualize_prompt: ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt: ChatPromptTemplate = PROMPT_REGISTRY[
                PromptType.CONTEXT_QA.value
                ]
            
            self.retriever= retriever
            self.chain=None
            if retriever is not None:
                self._build_lcel_chain()

            log.info("Conversational RAG initialized", session_id=self.session_id)

        except Exception as e:
            log.error("Unable to initiate ConverstaionalRAG", error=str(e))
            raise DocumentRAGException("Failed to initialize ConversationalRAG", sys)
    
    def load_retriever_from_faiss(self, 
                                  index_path: str,
                                  k: int=5,
                                  index_name:str= "index",
                                  search_type: str="similarity",
                                  search_kwargs: Optional[Dict[str, Any]]=None
                                  ):
        """
        Load the FAISS vectorstore from index and build retriever + LCEL chain.
        """
        try:
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            embedding=ModelLoader().load_embeddings()
            vectorstore=FAISS.load_local(
                index_path,
                embeddings=embedding,
                allow_dangerous_deserialization=True
            )
            if search_kwargs is None:
                search_kwargs= {'k':k}
            self.retriever= vectorstore.as_retriever(
                search_type=search_type, search_kwargs=search_kwargs)
            self._build_lcel_chain()
            log.info("FAISS retriever loaded successfully", index_path=index_path, 
                     index_name=index_name,
                     k=k,
                     session_id=self.session_id
                     )
            return self.retriever
        except Exception as e:
            log.error("Failed to load retriever from FAISS", error=str(e))
            raise DocumentRAGException("Loading error in ConversationalRAG", sys)
    
    def invoke(self, user_input:str, chat_history:Optional[List[BaseMessage]]=None)->str:
        """Invoke the LECL pipeline"""
        try:
            if self.chain is None:
                raise DocumentRAGException("RAG chain is not initialized. Call load_from_faiss() before invoke().", sys)
            
            chat_history= chat_history or []
            payload={"input": user_input,
                     "chat_history":chat_history}
            answer=self.chain.invoke(payload)
            if answer is None:
                log.warning("No answer generated", user_input=user_input, session_id=self.session_id)
                return "No answer generated"
            log.info("Answer generated successfully",
                          session_id=self.session_id,
                          user_input=user_input,
                          answer_preview=answer[:150])
            return answer

        except Exception as e:
            log.error("Failed to invoke ConverstaionalRAG", error=str(e))
            raise DocumentRAGException("Invocation error in ConversationalRAG", sys)
        
    def _load_llm(self):
        try:
            llm=ModelLoader().load_llm()
            if not llm:
                raise ValueError("LLM cannot be loaded")
            log.info("LLM loaded successfully", session_id=self.session_id)
            return llm
        except Exception as e:
            log.error("Failed to load LLM", error=str(e))
            raise DocumentRAGException("LLM loading error in ConversationalRAG", sys)


    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)

    def _build_lcel_chain(self):
        try:
            if self.retriever is None:
                raise DocumentRAGException("No retriever set before building chain", sys)
            
            # 1. Rewrite user question with chat history context
            question_rewriter=(
                {"input":itemgetter("input"), "chat_history":itemgetter("chat_history")}
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser() 
            )

            # 2. Retrieve docs for rewritten question
            retrieved_docs=question_rewriter| self.retriever | self._format_docs

            # 3. Answer using retrieved context + original input + chat history
            self.chain=(
                {
                    "context": retrieved_docs,
                    "input": itemgetter("input"),
                    "chat_history": itemgetter("chat_history")
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
                )
            log.info("LCEL chain built successfully", session_id=self.session_id)
        except Exception as e:
            log.error("Failed to build LCEL", error=str(e), session_id=self.session_id)
            raise DocumentRAGException("Chain building error in ConversationalRAG", sys)
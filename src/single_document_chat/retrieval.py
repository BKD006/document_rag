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
    def __init__(self, session_id: str, retriever):
        try:
            self.log= CustomLogger().get_logger(__name__)
            self.session_id=session_id
            self.retriever=retriever
            self.llm=self._load_llm()
            self.contextualize_prompt= PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt= PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            self.history_aware_retriever= create_history_aware_retriever(
                self.llm, self.retriever, self.contextualize_prompt
            )
            self.log.info("Created history-aware retriever", session_id=session_id)
            self.qa_chain=create_stuff_documents_chain(self.llm, self.qa_prompt)
            self.rag_chain= create_retrieval_chain(self.history_aware_retriever, self.qa_chain)
            self.log.info("Initialized ConversationalRAG", session_id=session_id)

            self.chain=RunnableWithMessageHistory(self.rag_chain,
                                                  self._get_session_history(),
                                                  input_messages_key="input",
                                                  history_messages_key="chat_history",
                                                  output_messages_key="answer"
                                                  )
            self.log.info("Created RunnableWithMessageHistory", session_id=session_id)


        except Exception as e:
            self.log.error("Unable to initiate ConverstaionalRAG", error=str(e))
            raise DocumentalRagException("Failed to initialize ConversationalRAG", sys)
    
    def _load_llm(self):
        try:
            llm=ModelLoader().load_llm()
            self.log.info("LLM Loaded successfully", class_name=llm.__class__.__name__)
            return llm

        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error=str(e))
            raise DocumentalRagException("Failed to LLM", sys)
    
    def _get_session_history(self, session_id:str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to access session history", session_id=session_id, error=str(e))
            raise DocumentalRagException("Failed to retrieve session history", sys)
    
    def load_retriever_from_faiss(self, index_path:str):
        try:
            embeddings= ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            vectorstore= FAISS.load_local(index_path, embeddings)
            self.log.info("Loaded retriver from FAISS index", index_path=index_path)
            return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})

        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", sys(e))
            raise DocumentalRagException("Failed to load retriever from FAISS", sys)
        
    def invoke(self, user_input:str)-> str:
        try:
            response=self.chain.invoke(
                {"input":user_input},
                config={"configurable": {"session_id":self.session_id}}
            )
            answer= response.get("answer", "No answer")
            if not answer:
                self.log.warning("Empty answer received", session_id=self.session_id)
            self.log.info("Chain invoked sucessfully", session_id=self.session_id,user_input=user_input, answer_preview=answer[:158]) 
            return answer

        except Exception as e:
            self.log.error("Failed to invoke conversational RAG", error=str(e), session_id=self.session_id)
            raise DocumentalRagException("Failed to invoke RAG chain", sys)
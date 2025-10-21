# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

# #Path to this PDF you want to test
# PDF_PATH=r"C:\\Users\\birok\\Python\\LLMOPs\\document_rag\\data\\document_analysis\\Attention_All__you_need.pdf"

# # Dummy file wrapper to simulate uploaded file (streamlit style)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name=Path(file_path).name
#         self._file_path= file_path

#     def getbuffer(self):
#         return open(self._file_path,"rb").read()
    
# def main():
#     try:
#         #----Step 1: Data Ingestion-----
#         print("Starting PDF Ingestion...")
#         dummy_pdf= DummyFile(PDF_PATH)
#         handler= DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path= handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content= handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         #----Step 2: Data Analysis----
#         print("Starting metadata analysis---")
#         analyzer= DocumentAnalyzer() #Loads LLM+parser
#         analysis_result= analyzer.analyze_document(text_content)
        
#         #----Step 3: Display results----
#         print("\n=== METADATA ANALYSIS RESULT===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")
    
#     except Exception as e:
#         print(f"Test Failed: {e}")

# if __name__=="__main__":
#     main()


## Testing for Document Compare
# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.doc_compare import DocumentCompareLLM

# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(open(file_path.read_bytes()))

# def test_compare_documents():
#     ref_path= Path("C:\\Users\\birok\\Python\\LLMOPs\\document_rag\\data\\document_compare\\LongReport_V1.pdf")
#     act_path= Path("C:\\Users\\birok\\Python\\LLMOPs\\document_rag\\data\\document_compare\\LongReport_V2.pdf")

#     class FakeUpload:
#         def __init__(self, file_path:Path):
#             self.name=file_path.name
#             self._buffer= file_path.read_bytes()
        
#         def getbuffer(self):
#             return self._buffer
    
#     ingestion= DocumentIngestion()
#     ref_upload= FakeUpload(ref_path)
#     act_upload= FakeUpload(act_path)

#     ref_file,act_file= ingestion.save_uploaded_files(ref_upload, act_upload)
#     combined_text= ingestion.combined_documents()
#     ingestion.clean_old_sessions(keep_latest=3)
#     print(combined_text[:1000])

#     llm_compare=DocumentCompareLLM()
#     comparison_df=llm_compare.compare_documents(combined_text)
#     print(comparison_df)


# if __name__=="__main__":
#     test_compare_documents()

## Testing code for single document chat
# import sys
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH=Path("faiss_index")

# def test_conversational_rag_on_pdf(pdf_path:str, question:str):
#     try:
#         model_loader=ModelLoader()
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS index...")
#             embeddings=model_loader.load_embeddings()
#             vectorstore=FAISS.load_local(str(FAISS_INDEX_PATH), embeddings=embeddings, allow_dangerous_deserialization=True)
#             retriever= vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingesting PDF and creating index...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files=[f]
#                 ingestor=SingleDocIngestor()
#                 retriever= ingestor.ingest_files(uploaded_files)
#         print("Running Conversational RAG...")
#         session_id= "test_conversational_rag"
#         rag= ConversationalRAG(retriever=retriever, session_id=session_id)

#         response= rag.invoke(question)
#         print(f"\nQuestion: {question}\nAnswer: {response}")

#     except Exception as e:
#         print("Test Failed", str(e))

# if __name__=="__main__":
#     pdf_path=r"C:\\Users\\birok\\Python\\LLMOPs\\document_rag\\data\\single_document_chat\\Attention_All__you_need.pdf"
#     question="What is the significance of attention mechanism? Can you explain in simple terms?"

#     if not Path(pdf_path).exists():
#         print(f"File doesn't exist at {pdf_path}")
#         sys.exit(1)

#     # Run the test
#     test_conversational_rag_on_pdf(pdf_path, question)

## Testing code for multi document chat
import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from utils.model_loader import ModelLoader
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.multi_document_chat.retrieval import ConversationalRAG

def test_document_ingestion_rag():
    try:
        test_files=["data\\multi_document_chat\\Adanced_Techniques_for_RAG.docx",
                   "data\\multi_document_chat\\All_the_fine_tuning_techniques.txt",
                   "data\\multi_document_chat\\Attention_All__you_need.pdf"]
        uploaded_files=[]
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"Files doesn't exist: {file_path}")

        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
        ingestor= DocumentIngestor()
        retriever= ingestor.ingest_files(uploaded_files)

        for f in uploaded_files:
            f.close()
        
        session_id= "test_multi_doc_chat"
        rag= ConversationalRAG(session_id=session_id, retriever=retriever)
        question="Give me brief fine tuning of llm"
        answer=  rag.invoke(question)
        print("\n Question", question)
        print("Answer", answer)

    except Exception as e:
        print(f"Test Failed: str{e}")
        sys.exit()


if __name__=="__main__":
    test_document_ingestion_rag()
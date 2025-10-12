import os
from pathlib import Path
from src.document_analyzer.data_ingestion import DocumentHandler
from src.document_analyzer.data_analysis import DocumentAnalyzer

#Path to this PDF you want to test
PDF_PATH=r"C:\\Users\\birok\\Python\\LLMOPs\\document_rag\\data\\document_analysis\\Attention_All__you_need.pdf"

# Dummy file wrapper to simulate uploaded file (streamlit style)
class DummyFile:
    def __init__(self, file_path):
        self.name=Path(file_path).name
        self._file_path= file_path

    def getbuffer(self):
        return open(self._file_path,"rb").read()
    
def main():
    try:
        #----Step 1: Data Ingestion-----
        print("Starting PDF Ingestion...")
        dummy_pdf= DummyFile(PDF_PATH)
        handler= DocumentHandler(session_id="test_ingestion_analysis")
        saved_path= handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")

        text_content= handler.read_pdf(saved_path)
        print(f"Extracted text length: {len(text_content)} chars\n")

        #----Step 2: Data Analysis----
        print("Starting metadata analysis---")
        analyzer= DocumentAnalyzer() #Loads LLM+parser
        analysis_result= analyzer.analyze_document(text_content)
        
        #----Step 3: Display results----
        print("\n=== METADATA ANALYSIS RESULT===")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")
    
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__=="__main__":
    main()
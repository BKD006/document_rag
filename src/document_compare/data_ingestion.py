import sys
import uuid
import os
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from logger.custom_logger import CustomLogger
from exception.custom_expection import DocumentalRagException

class DocumentIngestion:
    def __init__(self, base_dir:str= "data\\document_compare", session_id:str=None):
        self.log= CustomLogger().get_logger(__name__)
        self.base_dir= Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        #Create base session directory
        self.session_id= session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.session_path=os.path.join(self.base_dir,self.session_id)
        os.makedirs(self.session_path, exist_ok=True)

    def delete_existing_file(self):
        """
        Deletes existing files at the specified paths.
        """
        try:
            session_dir=Path(self.session_path)
            if session_dir.exists() and session_dir.is_dir():
                for file in session_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted", path= str(file))
                self.log.info("Directory cleaned", directory=str(session_dir))
        except Exception as e:
            self.log.error(f"Error deleting existing files: {e}")
            raise DocumentalRagException("An error occured while deleting existing files", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        """
        Saves uploaded files to a specified session directory.
        """
        try:
            self.delete_existing_file()
            self.log.info("Existing file deleted successfully.")

            ref_path=Path(self.session_path) / reference_file.name
            act_path=Path(self.session_path) / actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
            
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())
            
            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files Saved ", reference=str(ref_path), actual=str(act_path))
            
            return ref_path, act_path
        except Exception as e:
            self.log.error(f"Error uploading PDF: {e}")
            raise DocumentalRagException("An error occured while up;oading the PDF.", sys)

    def read_pdf(self, pdf_path)->str:
        """
        Reads a PDF file and extracts text from each page.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text=[]
                for page_num in range(doc.page_count):
                    page=doc.load_page(page_num)
                    text=page.get_text()
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num+1} --- \n{text}")
            self.log.info("PDF read successfully", file= str(pdf_path), pages=len(all_text))
            return "\n".join(all_text)
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentalRagException("An error occured while reading the PDF.", sys)
        
    def combined_documents(self)->str:
        try:
            content_dict={}
            doc_parts=[]

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix==".pdf":
                    content_dict[filename.name]=self.read_pdf(filename)
            
            for filename, content in content_dict.items():
                doc_parts.append(f"DocumentL: {filename}\n{content}")

            combined_text="\n\n".join(doc_parts)
            self.log.info("Documents combined", count= len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise  DocumentalRagException("An error occured while combining documents.", sys)
        
    def clean_old_sessions(self, keep_latest: int=5):
        """
        Cleans up old session directories, keeping only the latest specified number of sessions.
        """
        try:
            session_dirs=[d for d in self.base_dir.iterdir() if d.is_dir()]
            #Sort directories by modification time, newest first
            session_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
            if len(session_dirs) > keep_latest:
                for old_dir in session_dirs[keep_latest:]:
                    for item in old_dir.iterdir():
                        if item.is_file():
                            item.unlink()
                    old_dir.rmdir()
                    self.log.info("Old session cleaned", path=str(old_dir))
            else:
                self.log.info("No old sessions to clean.")
        except Exception as e:
            self.log.error(f"Error cleaning old sessions: {e}")
            raise DocumentalRagException("An error occured while cleaning old sessions.", sys)
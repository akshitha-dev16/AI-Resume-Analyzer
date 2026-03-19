import os
import docx2txt
from pdfminer.high_level import extract_text

def parse_resume(file_path):
    """
    Extracts text from PDF or DOCX files.
    """
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == '.pdf':
        try:
            return extract_text(file_path)
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
    elif extension == '.docx':
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            return f"Error parsing DOCX: {str(e)}"
    elif extension == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading TXT: {str(e)}"
    else:
        return "Unsupported file format"

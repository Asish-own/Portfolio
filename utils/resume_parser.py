import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return ""

    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def load_resume_data(pdf_path):
    """
    Loads and parses resume data. 
    (For now, it just returns raw text. 
    Ideally, we could parse it into sections like Skills, Experience, etc.)
    """
    raw_text = extract_text_from_pdf(pdf_path)
    return {
        "raw_text": raw_text
    }

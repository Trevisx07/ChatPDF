import fitz  

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500):
    if not text.strip():
        return []
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


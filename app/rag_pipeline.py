from pypdf import PdfReader

def extract_text_from_pdfs(files):
    text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

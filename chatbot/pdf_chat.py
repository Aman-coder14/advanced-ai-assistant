from PyPDF2 import PdfReader


def read_pdf(uploaded_pdf):

    reader = PdfReader(uploaded_pdf)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text
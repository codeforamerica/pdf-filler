from src.main import db
from src.pdfhook.models import PDFForm


def create_pdf_form(**kwargs):
    pdf = PDFForm.create(**kwargs)
    return pdf

def get_pdf(id):
    return PDFForm.select().where(PDFForm.id==id)

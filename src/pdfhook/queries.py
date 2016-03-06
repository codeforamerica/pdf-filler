from src.main import db
from src.pdfhook.models import PDFForm


def create_pdf_form(**kwargs):
    pdf = PDFForm(**kwargs)
    db.session.add(pdf)
    db.session.commit()
    return pdf

def get_pdf(id):
    return db.session.query(PDFForm).filter(PDFForm.id==id).first()
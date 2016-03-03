from marshmallow import Schema, fields, pre_dump, post_dump, pre_load
from src.main import ma
from flask import url_for
from pprint import pprint

from src.pdfhook.models import PDFForm

def generate_pdf_post_url(pdf):
    return url_for('pdfhook.fill_pdf', _external=True, pdf_id=pdf.id)

class PDFFormSerializer(ma.ModelSchema):
    url = fields.Function(lambda pdf: generate_pdf_post_url(pdf))

    @post_dump
    def post_process_fdf_map(self, data, *args, **kwargs):
        fields = {}
        for key, field in data.pop('fdf_mapping').items():
            fields[key] = field['type']
        data['fields'] = fields
        return data

    class Meta:
        model = PDFForm
        fields = (
            'id',
            'added_on',
            'url',
            'original_pdf_title',
            'latest_post',
            'post_count',
            'fdf_mapping',
            )
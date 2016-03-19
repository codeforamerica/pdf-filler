import json
from marshmallow import Schema, fields, pre_dump, post_dump, pre_load, post_load
from src.main import ma
from flask import url_for
from src.pdfhook.models import PDFForm

def generate_pdf_post_url(pdf):
    return url_for('pdfhook.fill_pdf', _external=True, pdf_id=pdf.id)

class PDFFormDumper(ma.ModelSchema):
    url = fields.Function(lambda pdf: generate_pdf_post_url(pdf))

    @post_dump
    def post_process_field_map(self, data, *args, **kwargs):
        field_map_string = data.pop('field_map')
        data['fields'] = json.loads(field_map_string)
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
            'field_map',
            )

class PDFFormIndexDumper(ma.ModelSchema):
    url = fields.Function(lambda pdf: generate_pdf_post_url(pdf))

    class Meta:
        model = PDFForm
        fields = (
            'added_on',
            'url',
            'original_pdf_title',
            'latest_post',
            'post_count',
            )

class PDFFormLoader(ma.ModelSchema):

    @pre_load
    def field_map_to_string(self, data, *args, **kwargs):
        if 'field_map' in data:
            data['field_map'] = json.dumps(data['field_map'])
        return data

    class Meta:
        model = PDFForm

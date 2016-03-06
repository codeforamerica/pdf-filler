import json
from marshmallow import Schema, fields, pre_dump, post_dump, pre_load, post_load
from src.main import ma
from flask import url_for
from pprint import pprint

from src.pdfhook.models import PDFForm

def generate_pdf_post_url(pdf):
    return url_for('pdfhook.fill_pdf', _external=True, pdf_id=pdf.id)

class PDFFormDumper(ma.ModelSchema):
    url = fields.Function(lambda pdf: generate_pdf_post_url(pdf))

    @post_dump
    def post_process_fdf_map(self, data, *args, **kwargs):
        fields = {}
        fdf_string = data.pop('fdf_mapping')
        fdf_dict = json.loads(fdf_string)
        for key, field in fdf_dict.items():
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


class PDFFormLoader(ma.ModelSchema):

    @pre_load
    def fdf_map_to_string(self, data, *args, **kwargs):
        if 'fdf_mapping' in data:
            data['fdf_mapping'] = json.dumps(data['fdf_mapping'])
        return data

    class Meta:
        model = PDFForm

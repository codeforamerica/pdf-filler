
import os
from pprint import pprint
from flask import url_for
from unittest.mock import patch
import requests
import json
import glob
from tests.test_base import BaseTestCase
from src.pdfparser import PDFParser


class TestPDFHook(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.pdf_file = 'data/sample_pdfs/sample_form.pdf'
        self.output_path = 'data/sample_output/sample_form-filled.pdf'

    def test_pdf_upload(self):
        from tests.mock import PDFHOOK_FIELD_OUPUT_SAMPLE
        with open(self.pdf_file, 'rb') as f:
            response = self.client.post(
                url_for('pdfhook.post_pdf'),
                data={'file':f},
                headers=[('Accept', 'application/json')]
                )
            results = json.loads(response.data.decode('utf-8'))
            self.assertIn('id', results)
            self.assertEqual(
                results['url'], url_for(
                    'pdfhook.fill_pdf', _external=True, pdf_id=results['id']))
            self.assertIn('fields', results)
            self.assertListEqual(results['fields'], PDFHOOK_FIELD_OUPUT_SAMPLE)


    def test_fill_pdf(self):
        # first we need a pdf loaded
        with open(self.pdf_file, 'rb') as f:
            files = {'file': f}
            r = self.client.post(
                url_for('pdfhook.post_pdf'),
                data={'file':f},
                headers=[('Accept', 'application/json')]
                )
            results = json.loads(r.data.decode('utf-8'))
        fields = results['fields']

        post_data = {
            'Given Name Text Box': 'Gaurav',
            'Family Name Text Box': 'Kulkarni',
            'Address 1 Text Box': '1 Main St',
            'Postcode Text Box': '94107',
            'City Text Box': 'San Francisco',
            'Height Formatted Field': '150cm',
            'Driving License Check Box': 'Yes',
            'Language 2 Check Box': 'Yes',
        }
        response = self.client.post(
            results['url'],
            headers={'Content-Type': 'application/json'},
            data=json.dumps(post_data)
            )
        raw_pdf_bytes = response.data
        # compare filled pdf data to the posted answers
        pdfparser = PDFParser()
        field_data_results = pdfparser.get_field_data(raw_pdf_bytes)['fields']
        for key, value in post_data.items():
            for field in field_data_results:
                if field['name'] == key:
                    self.assertEqual(field['value'], value)


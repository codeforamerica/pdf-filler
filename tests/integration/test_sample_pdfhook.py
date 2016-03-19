
import os
from pprint import pprint
from flask import url_for
from unittest.mock import patch
import requests
import json
import glob
from tests.test_base import BaseTestCase, format_pdf_search_term


class TestPDFHook(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.pdf_file = 'data/sample_pdfs/sample_form.pdf'
        self.output_path = 'data/sample_output/sample_form-filled.pdf'

    def test_pdf_upload(self):
        # TODO: Implement choice inputs that were stripped from the form
        results_sample = {
            'id': 1,
            'original_pdf_title': 'sample_form.pdf',
            'url': 'http://localhost/1/',
            'latest_post': None,
            'post_count': 0,
            'fields': [
                {'name': 'Address 1 Text Box', 'type': 'text', 'value': ''},
                {'name': 'Address 2 Text Box', 'type': 'text', 'value': ''},
                {'name': 'City Text Box', 'type': 'text', 'value': ''},
                {'name': 'Driving License Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Off'},
                {'name': 'Family Name Text Box', 'type': 'text', 'value': ''},
                {'name': 'Given Name Text Box', 'type': 'text', 'value': ''},
                {'name': 'Height Formatted Field', 'type': 'text', 'value': '150'},
                {'name': 'House nr Text Box', 'type': 'text', 'value': ''},
                {'name': 'Language 1 Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Off'},
                {'name': 'Language 2 Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Yes'},
                {'name': 'Language 3 Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Off'},
                {'name': 'Language 4 Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Off'},
                {'name': 'Language 5 Check Box',
                 'options': ['Off', 'Yes'],
                 'type': 'button',
                 'value': 'Off'},
                {'name': 'Postcode Text Box', 'type': 'text', 'value': ''}],
        }
        with open(self.pdf_file, 'rb') as f:
            response = self.client.post(
                url_for('pdfhook.post_pdf'),
                data={'file':f}
                )
            results = json.loads(response.data.decode('utf-8'))
            self.assertIn('id', results)
            self.assertEqual(
                results['url'], url_for(
                    'pdfhook.fill_pdf', _external=True, pdf_id=results['id']))
            self.assertIn('fields', results)
            # compare results sans date
            results.pop('added_on')
            self.maxDiff = None
            self.assertDictEqual(results, results_sample)
            self.assertEqual(glob.glob('data/tmp*'), [])
            self.assertEqual(glob.glob('data/filled*'), [])

    def test_fill_pdf(self):
        # first we need a pdf loaded
        with open(self.pdf_file, 'rb') as f:
            files = {'file': f}
            r = self.client.post(
                url_for('pdfhook.post_pdf'),
                data={'file':f}
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
        for key, value in post_data.items():
            for field in fields:
                if field['name'] == key:
                    if field['type'] == 'text':
                        pdf_formatted_value = format_pdf_search_term(value)
                        self.assertIn(pdf_formatted_value, raw_pdf_bytes)

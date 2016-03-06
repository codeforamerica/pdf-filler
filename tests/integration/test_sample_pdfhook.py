
from pprint import pprint
from flask import url_for
import requests
import json
from tests.test_base import BaseTestCase


class TestPDFHook(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.pdf_file = 'data/sample_pdfs/sample_form.pdf'

    def test_pdf_upload(self):
        # TODO: Implement choice inputs that were stripped from the form
        results_sample = {
            'id': 1,
            'url': 'http://localhost:5000/1/',
            'added_on': '2016-01-10T18:35:42.653853+00:00',
            'original_pdf_title': 'sample_form.pdf',
            'latest_post': None,
            'post_count': 0,
            'fields': {
                'given-name-text-box': 'Text',
                'family-name-text-box': 'Text',
                'address-1-text-box': 'Text',
                'house-nr-text-box': 'Text',
                'address-2-text-box': 'Text',
                'postcode-text-box': 'Text',
                'city-text-box': 'Text',
                '150': 'Text', # This is for height and is kind of strange
                'driving-license-check-box': 'Button',
                'language-1-check-box': 'Button',
                'language-2-check-box': 'Button',
                'language-3-check-box': 'Button',
                'language-4-check-box': 'Button',
                'language-5-check-box': 'Button',
            }
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
            results_sample.pop('added_on')
            results.pop('added_on')
            self.maxDiff = None
            self.assertDictEqual(results, results_sample)

    def test_fill_pdf(self):
        # TODO: Setting checkboxes still doesn't do anything
        post_data = {
            'given-name-text-box': 'Gaurav',
            'family-name-text-box': 'Kulkarni',
            'address-1-text-box': '1 Main St',
            'postcode-text-box': '94107',
            'city-text-box': 'San Francisco',
            '150': '150cm',
            'driving-license-check-box': True,
            'language-2-check-box': True,
        }
        # first we need a pdf loaded
        with open(self.pdf_file, 'rb') as f:
            files = {'file': f}
            r = self.client.post(
                url_for('pdfhook.post_pdf'),
                data={'file':f}
                )
            results = json.loads(r.data.decode('utf-8'))
        response = self.client.post(
            results['url'],
            headers={'Content-Type': 'application/json'},
            data=json.dumps(post_data)
            )
        results = response.data.decode('utf-8')
        self.assertIn('filled', results)
        self.assertIn('.pdf', results)



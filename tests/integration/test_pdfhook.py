
from pprint import pprint
from flask import url_for
import requests
import json
from tests.test_base import BaseTestCase


class TestPDFHook(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.pdf_file = 'data/sample_pdfs/General_Petition_Form-form.pdf'

    def test_pdf_upload(self):
        results_sample = {
            'id': 1,
            'url': 'http://localhost:9000/pdfhook/1/',
            'added_on': '2016-01-10T18:35:42.653853+00:00',
            'original_pdf_title': 'General_Petition_Form-form.pdf',
            'latest_post': None,
            'post_count': 0,
            'fields': {
                'attorney-for-name': 'Text',
                'case-number': 'Text',
                'code-and-sections-of-convictions': 'Text',
                'created-november-2014': 'Text',
                'date-of-birth': 'Text',
                'date-of-conviction': 'Text',
                'date-of-execution': 'Text',
                'defendant': 'Text',
                'e-mail-address': 'Text',
                'fax-number': 'Text',
                'for-reduction-to-misdemeanor': 'Button',
                'petition-and-response': 'Text',
                'petitioner-city': 'Text',
                'petitioner-requests-a-hearing': 'Button',
                'petitioner-state': 'Text',
                'petitioner-street-address': 'Text',
                'petitioner-zip-code': 'Text',
                'reduction-to-misdemeanor': 'Button',
                'sentence-imposed': 'Text',
                'signature-of-petitioner-or-attorney': 'Signature',
                'telephone-number': 'Text'}
        }
        with open(self.pdf_file, 'rb') as f:
            files = {'file': f}
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
            self.assertDictEqual(results, results_sample)

    def test_fill_pdf(self):
        post_data = {
                'attorney-for-name': 'Arthur Dent',
                'case-number': 'X9999999',
                'code-and-sections-of-convictions': "HS11357\nPC496",
                'date-of-birth': "1978-03-08",
                'date-of-conviction': '1997-06-04',
                'defendant': 'Arthur Dent',
                'e-mail-address': 'bring.a.towell@yahoo.com',
                'for-reduction-to-misdemeanor': True,
                'petitioner-city': 'Plural Z',
                'petitioner-requests-a-hearing': True,
                'petitioner-state': 'Alpha',
                'petitioner-street-address': 'ZZ9 Sector',
                'petitioner-zip-code': '99999',
                'reduction-to-misdemeanor': 'True',
                'sentence-imposed': '2 years prison',
                'telephone-number': '999-999-9999'
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


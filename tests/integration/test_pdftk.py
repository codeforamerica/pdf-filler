from unittest import TestCase

import os
from src.pdftk_wrapper import (
    PDFTKWrapper, PdftkError
    )

from tests.unit.test_pdftk import (
        FDF_STR_SAMPLE,
        DATA_FIELDS_STR_SAMPLE,
        FIELD_DATA_MAP_SAMPLE,
        FIELD_DATA,
        CHECKBOX_SAMPLE,
        RADIO_SAMPLE,
        LISTBOX_SAMPLE,
        DROPDOWN_SAMPLE,
        TEXT_SAMPLE
    )

from pprint import pprint

class TestPDFTK(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/CleanSlateSinglePage.pdf'

    def test_get_fdf(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_fdf(self.sample_form_path)
        self.assertEqual(results, FDF_STR_SAMPLE)
        pdftk.clean_up_tmp_files()

    def test_get_data_fields(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_data_fields(self.sample_form_path)
        self.assertEqual(results, DATA_FIELDS_STR_SAMPLE)
        pdftk.clean_up_tmp_files()

    def test_get_full_form_field_data(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_full_form_field_data(self.sample_form_path)
        self.assertDictEqual(results, FIELD_DATA_MAP_SAMPLE)

    def test_get_field_data(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(
            self.sample_form_path
            )
        self.assertListEqual(results, FIELD_DATA)


class TestFields(TestCase):

    def setUp(self):
        self.field_pdfs = {}
        for field in ['text', 'checkbox', 'radio', 'listbox', 'dropdown']:
            self.field_pdfs[field] = os.path.join(
                'data/sample_pdfs/fields', field + '.pdf')

    def test_fill_checkbox(self):
        path = self.field_pdfs['checkbox']
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(path)
        self.assertListEqual(results, CHECKBOX_SAMPLE)
        sample_answers = {
            'Check Box2': 'Off',
            'Check Box3': 'Yes'
        }
        filled_pdf = pdftk.fill_pdf(path, sample_answers)
        filled_sample = open(
            'data/sample_output/fields/checkbox.pdf', 'rb').read()
        self.assertEqual(filled_pdf, filled_sample)

    def test_fill_radio(self):
        path = self.field_pdfs['radio']
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(path)
        self.assertListEqual(results, RADIO_SAMPLE)
        sample_answers = {
            'Radio Buttons': 'yellow'
        }
        filled_pdf = pdftk.fill_pdf(path, sample_answers)
        filled_sample = open(
            'data/sample_output/fields/radio.pdf', 'rb').read()
        self.assertEqual(filled_pdf, filled_sample)

    def test_fill_text(self):
        path = self.field_pdfs['text']
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(path)
        self.assertListEqual(results, TEXT_SAMPLE)
        sample_answers = {
            'multiline': 'So\nmany\nlines',
            'single': 'Hello pdf world'
        }
        filled_pdf = pdftk.fill_pdf(path, sample_answers)
        filled_sample = open(
            'data/sample_output/fields/text.pdf', 'rb').read()
        self.assertEqual(filled_pdf, filled_sample)



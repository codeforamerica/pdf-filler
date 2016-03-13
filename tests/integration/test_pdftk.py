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


class TestPDFTK(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/field_type_survey.pdf'

    def test_pdftk_errors(self):
        pdftk = PDFTKWrapper()
        pdf_file_path = os.path.join(self.tmp_dir, 'sample_form.pdf')
        field_dump_path = os.path.join(self.tmp_dir, 'tmp-data_fields.txt')
        args = [
            'pdftk',
            pdf_file_path,
            'dump_data_fields_utf8',
            'output',
            field_dump_path
        ]
        with self.assertRaises(PdftkError):
            pdftk.run_command(args)

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
        # open('data/sample_output/fields/radio.pdf', 'wb'
            # ).write(filled_pdf)
        filled_sample = open(
            'data/sample_output/fields/radio.pdf', 'rb').read()
        self.assertEqual(filled_pdf, filled_sample)


    def test_fill_listbox(self):
        path = self.field_pdfs['listbox']
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(path)
        self.assertListEqual(results, LISTBOX_SAMPLE)
        sample_answers = {
            'List Box1': 'durian'
        }
        with self.assertRaises(PdftkError):
            filled_pdf = pdftk.fill_pdf(path, sample_answers)


    def test_fill_dropdown(self):
        path = self.field_pdfs['dropdown']
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(path)
        self.assertListEqual(results, DROPDOWN_SAMPLE)
        sample_answers = {
            'Dropdown5': 'river'
        }
        with self.assertRaises(PdftkError):
            filled_pdf = pdftk.fill_pdf(path, sample_answers)

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



from unittest import TestCase

import os
from src.pdftk_wrapper import (
    PDFTKWrapper, PdftkError
    )

from tests.unit.test_pdftk import (
        FDF_STR_SAMPLE,
        DATA_FIELDS_STR_SAMPLE,
        FIELD_DATA_MAP_SAMPLE
    )


class TestPDFTK(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/sample_form.pdf'

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

    def test_get_form_field_data(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_form_field_data(self.sample_form_path)
        self.assertDictEqual(results, FIELD_DATA_MAP_SAMPLE)




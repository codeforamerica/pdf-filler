from unittest import TestCase

import subprocess
import io
import os
import codecs
from src.pdftk_wrapper import (
    PDFTKWrapper, PdftkError
    )



class TestPDFTK(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/sample_form.pdf'
        self.fdf_str_sample = '%FDF-1.2\n%âãÏÓ\n1 0 obj \n<<\n/FDF \n<<\n/Fields [\n<<\n/V /Yes\n/T (Language 2 Check Box)\n>> \n<<\n/V ()\n/T (Address 2 Text Box)\n>> \n<<\n/V /Off\n/T (Language 3 Check Box)\n>> \n<<\n/V ()\n/T (City Text Box)\n>> \n<<\n/V /Off\n/T (Language 1 Check Box)\n>> \n<<\n/V /Off\n/T (Driving License Check Box)\n>> \n<<\n/V ()\n/T (Given Name Text Box)\n>> \n<<\n/V /Off\n/T (Language 5 Check Box)\n>> \n<<\n/V ()\n/T (House nr Text Box)\n>> \n<<\n/V (150)\n/T (Height Formatted Field)\n>> \n<<\n/V ()\n/T (Family Name Text Box)\n>> \n<<\n/V ()\n/T (Address 1 Text Box)\n>> \n<<\n/V /Off\n/T (Language 4 Check Box)\n>> \n<<\n/V ()\n/T (Postcode Text Box)\n>>]\n>>\n>>\nendobj \ntrailer\n\n<<\n/Root 1 0 R\n>>\n%%EOF\n'

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

    def test_generate_fdf(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_fdf(self.sample_form_path)
        self.assertEqual(results, self.fdf_str_sample)





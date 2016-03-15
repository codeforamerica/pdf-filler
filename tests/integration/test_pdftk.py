from unittest import TestCase
from nose.plugins.attrib import attr

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
from tests.mock.factories import example_pdf_answers

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
        results = pdftk._get_full_form_field_data(self.sample_form_path)
        self.assertDictEqual(results, FIELD_DATA_MAP_SAMPLE)
        pdftk.clean_up_tmp_files()

    def test_get_field_data(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_field_data(
            self.sample_form_path
            )
        self.assertListEqual(results, FIELD_DATA)

    def create_pdf_search_term(self, search_term, encoding='utf-8'):
        """Converts a unicode string into the way it might actually
        exist in the bytes of a pdf document. so we can check if the text
        made its way into the final pdf.
        An example:
            the text
                'So\nmany\nlines'
            becomes the bytes
                b'S\x00o\x00\\n\x00m\x00a\x00n\x00y\x00\\n\x00l\x00i\x00n\x00e\x00s'
        """
        # convert to bytes
        base = str(search_term).encode(encoding)
        # interleave the bytes with null bytes
        byte_arr = []
        for null_and_char_pair in list(zip([0 for c in base], base)):
            byte_arr.extend(null_and_char_pair)
        byte_str = bytes(byte_arr[1:])
        # new lines are not what you'd expect
        return byte_str.replace(b'\n', b'\\n')

    def test_fill_example_pdf(self):
        pdftk = PDFTKWrapper()
        fields = pdftk.get_field_data(
            self.sample_form_path
            )

        sample_answers = {
            'Address City': 'Little Town',
            'Address State': 'CA',
            'Address Street': '111 Main Street',
            'Address Zip': '01092',
            'Arrested outside SF': 'No',
            'Cell phone number': '999-999-9999',
            'Charged with a crime': 'No',
            'Date': '09/09/2016',
            'Date of Birth': '09/09/9999',
            'Dates arrested outside SF': '',
            'Drivers License': 'D9999999',
            'Email Address': 'berry.happy.manatee@gmail.com',
            'Employed': 'No',
            'First Name': 'Berry',
            'Home phone number': '',
            'How did you hear about the Clean Slate Program':
                'From a wonderful friend',
            'If probation where and when?': '',
            'Last Name': 'Manatee',
            'MI': 'H',
            'May we leave voicemail': 'Yes',
            'May we send mail here': 'Yes',
            'Monthly expenses': '1000',
            'On probation or parole': 'No',
            'Other phone number': '',
            'Serving a sentence': 'No',
            'Social Security Number': '999-99-9999',
            'US Citizen': 'Yes',
            'What is your monthly income': '0',
            'Work phone number': '',
        }

        filled_pdf = pdftk.fill_pdf(self.sample_form_path, sample_answers)
        for field in fields:
            field_type = field['type']
            if field_type == 'text':
                field_name = field['name']
                answer_text = sample_answers[field_name]
                search_term = self.create_pdf_search_term(answer_text)
                self.assertIn(search_term, filled_pdf)

    @attr('slow')
    def test_fill_many(self):
        pdftk = PDFTKWrapper()
        fields = pdftk.get_field_data(
            self.sample_form_path
            )
        answers = example_pdf_answers(3)
        results = pdftk.fill_pdf_many(self.sample_form_path, answers)
        for field in fields:
            field_type = field['type']
            if field_type == 'text':
                field_name = field['name']
                for answer in answers:
                    answer_text = answer[field_name]
                    search_term = self.create_pdf_search_term(answer_text)
                    self.assertIn(search_term, results)




class TestFields(TestPDFTK):

    def setUp(self):
        TestPDFTK.setUp(self)
        self.field_pdfs = {}
        for field in ['text', 'checkbox', 'radio']:
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
        for key, value in sample_answers.items():
            pdf_friendly_search_term = self.create_pdf_search_term(
                value, pdftk.encoding)
            self.assertIn(pdf_friendly_search_term, filled_pdf)

    @attr('slow')
    def test_combine_pdfs(self):
        pdftk = PDFTKWrapper()
        # get all the paths of filled field samples
        paths = [
                    p.replace('pdfs', 'output')
                    for p in self.field_pdfs.values()
                ]
        paths.sort()
        combined_pdf = pdftk.join_pdfs(paths)
        sample_combined = open(
            'data/sample_output/fields/all.pdf', 'rb').read()
        # check that there is less than 1kb difference in length
        # between result and sample
        self.assertLess(
            abs(
                len(combined_pdf) - len(sample_combined)
                ),
            1000
            )






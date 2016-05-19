from unittest import TestCase

from src.pdfparser import (
    PDFParser, PDFParserError, InvalidOptionError
    )

from tests.mock.factories import example_pdf_answers
from tests.unit.test_pdfparser import (
    FIELD_DATA,
    )

class TestPDFParser(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/CleanSlateSinglePage.pdf'

    def test_bad_path_raises_error(self):
        pdfparser = PDFParser()
        pdfparser.PDFPARSER_PATH = 'nowhere'
        with self.assertRaises(PDFParserError):
            pdfparser.get_field_data(self.sample_form_path)

    def test_get_field_data(self):
        pdfparser = PDFParser()
        results = pdfparser.get_field_data(
            self.sample_form_path)
        self.assertDictEqual(results, FIELD_DATA)

    def test_fill_example_pdf(self):
        pdfparser = PDFParser()
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
            'Drivers License': 'D99999',
            'Email Address': 'berry.happy.mañatee@gmail.com',
            'Employed': 'No',
            'First Name': 'Berry',
            'Home phone number': '',
            'How did you hear about the Clean Slate Prograthim':
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

        filled_pdf = pdfparser.fill_pdf(self.sample_form_path, sample_answers)
        field_data_output = pdfparser.get_field_data(filled_pdf)
        expected_field_output = pdfparser.get_field_data(
            'data/sample_output/CleanSlateSinglePage.pdf')
        self.assertDictEqual(field_data_output, expected_field_output)

    def test_incorrect_option_raises_error(self):
        pdfparser = PDFParser()
        sample_answers = {
            'Arrested outside SF': 'Maybe'
        }
        with self.assertRaises(InvalidOptionError):
            filled_pdf = pdfparser.fill_pdf(self.sample_form_path, sample_answers)

    def test_join_pdfs(self):
        pdfparser = PDFParser()
        joined_pdf = pdfparser.join_pdfs([
            self.sample_form_path,
            self.sample_form_path])
        open('data/sample_output/joined.pdf', 'wb').write(joined_pdf)

    def test_fill_multiple(self):
        pdfparser = PDFParser()
        answers = example_pdf_answers(2)
        filled_pdf = pdfparser.fill_many_pdfs(self.sample_form_path, answers)
        open('data/sample_output/multi.pdf', 'wb').write(filled_pdf)
      





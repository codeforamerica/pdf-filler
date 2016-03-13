from unittest import TestCase

import os
from src.pdftk_wrapper import (
    PDFTKWrapper, PdftkError
    )



class TestPDFTK(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.tmp_dir = 'data'
        self.sample_form_path = 'data/sample_pdfs/sample_form.pdf'
        self.fdf_str_sample = '%FDF-1.2\n%âãÏÓ\n1 0 obj \n<<\n/FDF \n<<\n/Fields [\n<<\n/V /Yes\n/T (Language 2 Check Box)\n>> \n<<\n/V ()\n/T (Address 2 Text Box)\n>> \n<<\n/V /Off\n/T (Language 3 Check Box)\n>> \n<<\n/V ()\n/T (City Text Box)\n>> \n<<\n/V /Off\n/T (Language 1 Check Box)\n>> \n<<\n/V /Off\n/T (Driving License Check Box)\n>> \n<<\n/V ()\n/T (Given Name Text Box)\n>> \n<<\n/V /Off\n/T (Language 5 Check Box)\n>> \n<<\n/V ()\n/T (House nr Text Box)\n>> \n<<\n/V (150)\n/T (Height Formatted Field)\n>> \n<<\n/V ()\n/T (Family Name Text Box)\n>> \n<<\n/V ()\n/T (Address 1 Text Box)\n>> \n<<\n/V /Off\n/T (Language 4 Check Box)\n>> \n<<\n/V ()\n/T (Postcode Text Box)\n>>]\n>>\n>>\nendobj \ntrailer\n\n<<\n/Root 1 0 R\n>>\n%%EOF\n'
        self.data_fields_str_sample = '---\nFieldType: Text\nFieldName: Given Name Text Box\nFieldNameAlt: First name\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Family Name Text Box\nFieldNameAlt: Last name\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Address 1 Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: House nr Text Box\nFieldNameAlt: House and floor\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Text\nFieldName: Address 2 Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Postcode Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Text\nFieldName: City Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Height Formatted Field\nFieldNameAlt: Value from 40 to 250 cm\nFieldFlags: 0\nFieldValue: 150\nFieldValueDefault: 150\nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Button\nFieldName: Driving License Check Box\nFieldNameAlt: Car driving license\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 1 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 2 Check Box\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 3 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 4 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 5 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n'
        self.parsed_fdf_fields = [('Language 2 Check Box', {'name': 'Language 2 Check Box', 'escaped_name': 'Language 2 Check Box', 'value_template': '/Yes', 'name_span': (61, 81), 'value_template_span': (52, 56)}), ('Address 2 Text Box', {'name': 'Address 2 Text Box', 'escaped_name': 'Address 2 Text Box', 'value_template': '()', 'name_span': (100, 118), 'value_template_span': (93, 95)}), ('Language 3 Check Box', {'name': 'Language 3 Check Box', 'escaped_name': 'Language 3 Check Box', 'value_template': '/Off', 'name_span': (139, 159), 'value_template_span': (130, 134)}), ('City Text Box', {'name': 'City Text Box', 'escaped_name': 'City Text Box', 'value_template': '()', 'name_span': (178, 191), 'value_template_span': (171, 173)}), ('Language 1 Check Box', {'name': 'Language 1 Check Box', 'escaped_name': 'Language 1 Check Box', 'value_template': '/Off', 'name_span': (212, 232), 'value_template_span': (203, 207)}), ('Driving License Check Box', {'name': 'Driving License Check Box', 'escaped_name': 'Driving License Check Box', 'value_template': '/Off', 'name_span': (253, 278), 'value_template_span': (244, 248)}), ('Given Name Text Box', {'name': 'Given Name Text Box', 'escaped_name': 'Given Name Text Box', 'value_template': '()', 'name_span': (297, 316), 'value_template_span': (290, 292)}), ('Language 5 Check Box', {'name': 'Language 5 Check Box', 'escaped_name': 'Language 5 Check Box', 'value_template': '/Off', 'name_span': (337, 357), 'value_template_span': (328, 332)}), ('House nr Text Box', {'name': 'House nr Text Box', 'escaped_name': 'House nr Text Box', 'value_template': '()', 'name_span': (376, 393), 'value_template_span': (369, 371)}), ('Height Formatted Field', {'name': 'Height Formatted Field', 'escaped_name': 'Height Formatted Field', 'value_template': '(150)', 'name_span': (415, 437), 'value_template_span': (405, 410)}), ('Family Name Text Box', {'name': 'Family Name Text Box', 'escaped_name': 'Family Name Text Box', 'value_template': '()', 'name_span': (456, 476), 'value_template_span': (449, 451)}), ('Address 1 Text Box', {'name': 'Address 1 Text Box', 'escaped_name': 'Address 1 Text Box', 'value_template': '()', 'name_span': (495, 513), 'value_template_span': (488, 490)}), ('Language 4 Check Box', {'name': 'Language 4 Check Box', 'escaped_name': 'Language 4 Check Box', 'value_template': '/Off', 'name_span': (534, 554), 'value_template_span': (525, 529)}), ('Postcode Text Box', {'name': 'Postcode Text Box', 'escaped_name': 'Postcode Text Box', 'value_template': '()', 'name_span': (573, 590), 'value_template_span': (566, 568)})]
        self.parsed_data_fields = [('Given Name Text Box', {'FieldName': 'Given Name Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'First name', 'FieldFlags': '0', 'FieldMaxLength': '40'}), ('Family Name Text Box', {'FieldName': 'Family Name Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Last name', 'FieldFlags': '0', 'FieldMaxLength': '40'}), ('Address 1 Text Box', {'FieldName': 'Address 1 Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('House nr Text Box', {'FieldName': 'House nr Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'House and floor', 'FieldFlags': '0', 'FieldMaxLength': '20'}), ('Address 2 Text Box', {'FieldName': 'Address 2 Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('Postcode Text Box', {'FieldName': 'Postcode Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '20'}), ('City Text Box', {'FieldName': 'City Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('Height Formatted Field', {'FieldName': 'Height Formatted Field', 'FieldValue': '150', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Value from 40 to 250 cm', 'FieldValueDefault': '150', 'FieldFlags': '0', 'FieldMaxLength': '20'}), ('Driving License Check Box', {'FieldName': 'Driving License Check Box', 'FieldValue': 'Off', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldJustification': 'Left', 'FieldNameAlt': 'Car driving license', 'FieldFlags': '0'}), ('Language 1 Check Box', {'FieldName': 'Language 1 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 2 Check Box', {'FieldName': 'Language 2 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Yes'}), ('Language 3 Check Box', {'FieldName': 'Language 3 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 4 Check Box', {'FieldName': 'Language 4 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 5 Check Box', {'FieldName': 'Language 5 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'})]

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
        self.assertEqual(results, self.fdf_str_sample)
        pdftk.clean_up_tmp_files()

    def test_get_data_fields(self):
        pdftk = PDFTKWrapper()
        results = pdftk.get_data_fields(self.sample_form_path)
        self.assertEqual(results, self.data_fields_str_sample)
        pdftk.clean_up_tmp_files()

    def test_parse_fdf(self):
        pdftk = PDFTKWrapper()
        results = list(pdftk.parse_fdf_fields(self.fdf_str_sample))
        self.assertListEqual(results, self.parsed_fdf_fields)

    def test_parse_data_fields(self):
        pdftk = PDFTKWrapper()
        results = list(pdftk.parse_data_fields(
            self.data_fields_str_sample))
        self.assertListEqual(results, self.parsed_data_fields)








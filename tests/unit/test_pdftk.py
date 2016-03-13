from unittest import TestCase
from unittest.mock import Mock, patch
from src.pdftk_wrapper import PDFTKWrapper, PdftkError

# these are based on the pdf form in 'data/sample_pdfs/sample_form.pdf'
FDF_STR_SAMPLE = "%FDF-1.2\n%âãÏÓ\n1 0 obj \n<<\n/FDF \n<<\n/Fields [\n<<\n/V /Yes\n/T (Language 2 Check Box)\n>> \n<<\n/V ()\n/T (Address 2 Text Box)\n>> \n<<\n/V /Off\n/T (Language 3 Check Box)\n>> \n<<\n/V ()\n/T (City Text Box)\n>> \n<<\n/V /Off\n/T (Language 1 Check Box)\n>> \n<<\n/V /Off\n/T (Driving License Check Box)\n>> \n<<\n/V ()\n/T (Given Name Text Box)\n>> \n<<\n/V /Off\n/T (Language 5 Check Box)\n>> \n<<\n/V ()\n/T (House nr Text Box)\n>> \n<<\n/V (150)\n/T (Height Formatted Field)\n>> \n<<\n/V ()\n/T (Family Name Text Box)\n>> \n<<\n/V ()\n/T (Address 1 Text Box)\n>> \n<<\n/V /Off\n/T (Language 4 Check Box)\n>> \n<<\n/V ()\n/T (Postcode Text Box)\n>>]\n>>\n>>\nendobj \ntrailer\n\n<<\n/Root 1 0 R\n>>\n%%EOF\n"
DATA_FIELDS_STR_SAMPLE = "---\nFieldType: Text\nFieldName: Given Name Text Box\nFieldNameAlt: First name\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Family Name Text Box\nFieldNameAlt: Last name\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Address 1 Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: House nr Text Box\nFieldNameAlt: House and floor\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Text\nFieldName: Address 2 Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Postcode Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Text\nFieldName: City Text Box\nFieldFlags: 0\nFieldValue: \nFieldJustification: Left\nFieldMaxLength: 40\n---\nFieldType: Text\nFieldName: Height Formatted Field\nFieldNameAlt: Value from 40 to 250 cm\nFieldFlags: 0\nFieldValue: 150\nFieldValueDefault: 150\nFieldJustification: Left\nFieldMaxLength: 20\n---\nFieldType: Button\nFieldName: Driving License Check Box\nFieldNameAlt: Car driving license\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 1 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 2 Check Box\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 3 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 4 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Language 5 Check Box\nFieldFlags: 0\nFieldValue: Off\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n"
PARSED_FDF_FIELDS = [('Language 2 Check Box', {'name': 'Language 2 Check Box', 'escaped_name': 'Language 2 Check Box', 'value_template': '/Yes', 'name_span': (61, 81), 'value_template_span': (52, 56)}), ('Address 2 Text Box', {'name': 'Address 2 Text Box', 'escaped_name': 'Address 2 Text Box', 'value_template': '()', 'name_span': (100, 118), 'value_template_span': (93, 95)}), ('Language 3 Check Box', {'name': 'Language 3 Check Box', 'escaped_name': 'Language 3 Check Box', 'value_template': '/Off', 'name_span': (139, 159), 'value_template_span': (130, 134)}), ('City Text Box', {'name': 'City Text Box', 'escaped_name': 'City Text Box', 'value_template': '()', 'name_span': (178, 191), 'value_template_span': (171, 173)}), ('Language 1 Check Box', {'name': 'Language 1 Check Box', 'escaped_name': 'Language 1 Check Box', 'value_template': '/Off', 'name_span': (212, 232), 'value_template_span': (203, 207)}), ('Driving License Check Box', {'name': 'Driving License Check Box', 'escaped_name': 'Driving License Check Box', 'value_template': '/Off', 'name_span': (253, 278), 'value_template_span': (244, 248)}), ('Given Name Text Box', {'name': 'Given Name Text Box', 'escaped_name': 'Given Name Text Box', 'value_template': '()', 'name_span': (297, 316), 'value_template_span': (290, 292)}), ('Language 5 Check Box', {'name': 'Language 5 Check Box', 'escaped_name': 'Language 5 Check Box', 'value_template': '/Off', 'name_span': (337, 357), 'value_template_span': (328, 332)}), ('House nr Text Box', {'name': 'House nr Text Box', 'escaped_name': 'House nr Text Box', 'value_template': '()', 'name_span': (376, 393), 'value_template_span': (369, 371)}), ('Height Formatted Field', {'name': 'Height Formatted Field', 'escaped_name': 'Height Formatted Field', 'value_template': '(150)', 'name_span': (415, 437), 'value_template_span': (405, 410)}), ('Family Name Text Box', {'name': 'Family Name Text Box', 'escaped_name': 'Family Name Text Box', 'value_template': '()', 'name_span': (456, 476), 'value_template_span': (449, 451)}), ('Address 1 Text Box', {'name': 'Address 1 Text Box', 'escaped_name': 'Address 1 Text Box', 'value_template': '()', 'name_span': (495, 513), 'value_template_span': (488, 490)}), ('Language 4 Check Box', {'name': 'Language 4 Check Box', 'escaped_name': 'Language 4 Check Box', 'value_template': '/Off', 'name_span': (534, 554), 'value_template_span': (525, 529)}), ('Postcode Text Box', {'name': 'Postcode Text Box', 'escaped_name': 'Postcode Text Box', 'value_template': '()', 'name_span': (573, 590), 'value_template_span': (566, 568)})]
PARSED_DATA_FIELDS = [('Given Name Text Box', {'FieldName': 'Given Name Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'First name', 'FieldFlags': '0', 'FieldMaxLength': '40'}), ('Family Name Text Box', {'FieldName': 'Family Name Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Last name', 'FieldFlags': '0', 'FieldMaxLength': '40'}), ('Address 1 Text Box', {'FieldName': 'Address 1 Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('House nr Text Box', {'FieldName': 'House nr Text Box', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'House and floor', 'FieldFlags': '0', 'FieldMaxLength': '20'}), ('Address 2 Text Box', {'FieldName': 'Address 2 Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('Postcode Text Box', {'FieldName': 'Postcode Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '20'}), ('City Text Box', {'FieldName': 'City Text Box', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldValue': '', 'FieldMaxLength': '40'}), ('Height Formatted Field', {'FieldName': 'Height Formatted Field', 'FieldValue': '150', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Value from 40 to 250 cm', 'FieldValueDefault': '150', 'FieldFlags': '0', 'FieldMaxLength': '20'}), ('Driving License Check Box', {'FieldName': 'Driving License Check Box', 'FieldValue': 'Off', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldJustification': 'Left', 'FieldNameAlt': 'Car driving license', 'FieldFlags': '0'}), ('Language 1 Check Box', {'FieldName': 'Language 1 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 2 Check Box', {'FieldName': 'Language 2 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Yes'}), ('Language 3 Check Box', {'FieldName': 'Language 3 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 4 Check Box', {'FieldName': 'Language 4 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'}), ('Language 5 Check Box', {'FieldName': 'Language 5 Check Box', 'FieldJustification': 'Left', 'FieldStateOption': ['Off', 'Yes'], 'FieldType': 'Button', 'FieldFlags': '0', 'FieldValue': 'Off'})]
FIELD_DATA_MAP_SAMPLE = {'Height Formatted Field': {'FieldName': 'Height Formatted Field', 'FieldFlags': '0', 'FieldValue': '150', 'FieldValueDefault': '150', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Value from 40 to 250 cm', 'fdf': {'value_template': '(150)', 'escaped_name': 'Height Formatted Field', 'name_span': (415, 437), 'value_template_span': (405, 410), 'name': 'Height Formatted Field'}, 'FieldMaxLength': '20'}, 'Postcode Text Box': {'FieldName': 'Postcode Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'fdf': {'value_template': '()', 'escaped_name': 'Postcode Text Box', 'name_span': (573, 590), 'value_template_span': (566, 568), 'name': 'Postcode Text Box'}, 'FieldMaxLength': '20'}, 'Language 4 Check Box': {'FieldName': 'Language 4 Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Off', 'FieldType': 'Button', 'FieldJustification': 'Left', 'fdf': {'value_template': '/Off', 'escaped_name': 'Language 4 Check Box', 'name_span': (534, 554), 'value_template_span': (525, 529), 'name': 'Language 4 Check Box'}}, 'Language 3 Check Box': {'FieldName': 'Language 3 Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Off', 'FieldType': 'Button', 'FieldJustification': 'Left', 'fdf': {'value_template': '/Off', 'escaped_name': 'Language 3 Check Box', 'name_span': (139, 159), 'value_template_span': (130, 134), 'name': 'Language 3 Check Box'}}, 'Address 2 Text Box': {'FieldName': 'Address 2 Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'fdf': {'value_template': '()', 'escaped_name': 'Address 2 Text Box', 'name_span': (100, 118), 'value_template_span': (93, 95), 'name': 'Address 2 Text Box'}, 'FieldMaxLength': '40'}, 'Language 5 Check Box': {'FieldName': 'Language 5 Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Off', 'FieldType': 'Button', 'FieldJustification': 'Left', 'fdf': {'value_template': '/Off', 'escaped_name': 'Language 5 Check Box', 'name_span': (337, 357), 'value_template_span': (328, 332), 'name': 'Language 5 Check Box'}}, 'Family Name Text Box': {'FieldName': 'Family Name Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'Last name', 'fdf': {'value_template': '()', 'escaped_name': 'Family Name Text Box', 'name_span': (456, 476), 'value_template_span': (449, 451), 'name': 'Family Name Text Box'}, 'FieldMaxLength': '40'}, 'House nr Text Box': {'FieldName': 'House nr Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'House and floor', 'fdf': {'value_template': '()', 'escaped_name': 'House nr Text Box', 'name_span': (376, 393), 'value_template_span': (369, 371), 'name': 'House nr Text Box'}, 'FieldMaxLength': '20'}, 'Driving License Check Box': {'FieldName': 'Driving License Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Off', 'FieldType': 'Button', 'FieldJustification': 'Left', 'FieldNameAlt': 'Car driving license', 'fdf': {'value_template': '/Off', 'escaped_name': 'Driving License Check Box', 'name_span': (253, 278), 'value_template_span': (244, 248), 'name': 'Driving License Check Box'}}, 'Language 1 Check Box': {'FieldName': 'Language 1 Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Off', 'FieldType': 'Button', 'FieldJustification': 'Left', 'fdf': {'value_template': '/Off', 'escaped_name': 'Language 1 Check Box', 'name_span': (212, 232), 'value_template_span': (203, 207), 'name': 'Language 1 Check Box'}}, 'Given Name Text Box': {'FieldName': 'Given Name Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'FieldNameAlt': 'First name', 'fdf': {'value_template': '()', 'escaped_name': 'Given Name Text Box', 'name_span': (297, 316), 'value_template_span': (290, 292), 'name': 'Given Name Text Box'}, 'FieldMaxLength': '40'}, 'Address 1 Text Box': {'FieldName': 'Address 1 Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'fdf': {'value_template': '()', 'escaped_name': 'Address 1 Text Box', 'name_span': (495, 513), 'value_template_span': (488, 490), 'name': 'Address 1 Text Box'}, 'FieldMaxLength': '40'}, 'City Text Box': {'FieldName': 'City Text Box', 'FieldFlags': '0', 'FieldValue': '', 'FieldType': 'Text', 'FieldJustification': 'Left', 'fdf': {'value_template': '()', 'escaped_name': 'City Text Box', 'name_span': (178, 191), 'value_template_span': (171, 173), 'name': 'City Text Box'}, 'FieldMaxLength': '40'}, 'Language 2 Check Box': {'FieldName': 'Language 2 Check Box', 'FieldStateOption': ['Off', 'Yes'], 'FieldFlags': '0', 'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldJustification': 'Left', 'fdf': {'value_template': '/Yes', 'escaped_name': 'Language 2 Check Box', 'name_span': (61, 81), 'value_template_span': (52, 56), 'name': 'Language 2 Check Box'}}}

class TestPDFTK(TestCase):

    def test_init(self):
        pdftk = PDFTKWrapper()
        self.assertEqual(pdftk.encoding, 'latin-1')
        self.assertEqual(pdftk.TEMP_FOLDER_PATH, None)
        pdftk = PDFTKWrapper(
            encoding='utf-8', tmp_path='data')
        self.assertEqual(pdftk.encoding, 'utf-8')
        self.assertEqual(pdftk.TEMP_FOLDER_PATH, 'data')

    def test_get_fdf(self):
        pdftk = PDFTKWrapper()
        coercer = Mock(return_value='path.pdf')
        pdftk._coerce_to_file_path = coercer
        writer = Mock(return_value='tmp_path.fdf')
        pdftk._write_tmp_file = writer
        runner = Mock()
        pdftk.run_command = runner
        contents_getter = Mock()
        pdftk._get_file_contents = contents_getter
        results = pdftk.get_fdf('something.pdf')
        coercer.assert_called_once_with('something.pdf')
        writer.assert_called_once_with()
        runner.assert_called_once_with([
            'path.pdf', 'generate_fdf',
            'output', 'tmp_path.fdf'])
        contents_getter.assert_called_once_with(
            'tmp_path.fdf', decode=True)

    @patch('src.pdftk_wrapper.subprocess')
    def test_run_command(self, subprocess):
        pdftk = PDFTKWrapper()
        comm_err = Mock(return_value=(b'', b'an error'))
        comm_out = Mock(return_value=(b'success', b''))
        proc_out = Mock(communicate=comm_out)
        proc_err = Mock(communicate=comm_err)
        popen_yes = Mock(return_value=proc_out)
        popen_bad = Mock(return_value=proc_err)

        # check the good case
        subprocess.Popen = popen_yes
        args = ['pdftk', 'go']
        result = pdftk.run_command(args)
        self.assertEqual('success', result)
        popen_yes.assert_called_once_with(args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        comm_out.assert_called_once_with()
        proc_out.assert_not_called()

        # check the arg fixing
        popen_yes.reset_mock()
        result = pdftk.run_command(['dostuff'])
        popen_yes.assert_called_once_with(['pdftk','dostuff'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # check the bad case
        subprocess.reset_mock()
        subprocess.Popen = popen_bad
        args = ['go']
        with self.assertRaises(PdftkError):
            pdftk.run_command(args)
        proc_err.assert_not_called()
        comm_err.assert_called_once_with()
        popen_bad.assert_called_once_with(['pdftk','go'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @patch('src.pdftk_wrapper.mkstemp')
    @patch('builtins.open')
    def test_write_tmp_file(self, open, mkstemp):
        mkstemp.return_value = ('os.file', 'filepath')
        mock_file = Mock()

        # check with file_object
        pdftk = PDFTKWrapper()
        path = pdftk._write_tmp_file(mock_file)
        mkstemp.assert_called_once_with(dir=pdftk.TEMP_FOLDER_PATH)
        open.assert_called_once_with('filepath', 'wb')
        mock_file.read.assert_called_once_with()
        self.assertEqual(path, 'filepath')
        self.assertListEqual(pdftk._tmp_files, ['filepath'])

        # check with bytes
        pdftk = PDFTKWrapper()
        mkstemp.reset_mock()
        open.reset_mock()
        path = pdftk._write_tmp_file(bytestring=b'content')
        open.assert_called_once_with('filepath', 'wb')
        self.assertEqual(path, 'filepath')
        self.assertListEqual(pdftk._tmp_files, ['filepath'])


    @patch('src.pdftk_wrapper.os.remove')
    def test_clean_up_tmp_files(self, remove):
        pdftk = PDFTKWrapper()
        paths = [c for c in 'hello']
        pdftk._tmp_files = paths
        pdftk.clean_up_tmp_files()
        for p in paths:
            remove.assert_any_call(p)
        self.assertListEqual(pdftk._tmp_files, [])
        # test with no files
        remove.reset_mock()
        pdftk.clean_up_tmp_files()
        remove.assert_not_called()

    def test_coerce_to_file_path(self):
        pdftk = PDFTKWrapper()
        wrt_tmp = Mock(return_value='path')
        pdftk._write_tmp_file = wrt_tmp

        # check with a string input
        result = pdftk._coerce_to_file_path('goodpath')
        self.assertEqual(result, 'goodpath')
        wrt_tmp.assert_not_called()

        # check with a bytestring input
        bstring = b'foo'
        result = pdftk._coerce_to_file_path(bstring)
        self.assertEqual(result, 'path')
        wrt_tmp.assert_called_once_with(bytestring=bstring)

        # check with a not string input
        wrt_tmp.reset_mock()
        not_string = Mock()
        result = pdftk._coerce_to_file_path(not_string)
        self.assertEqual(result, 'path')
        wrt_tmp.assert_called_once_with(file_obj=not_string)

    @patch('builtins.open')
    def test_get_file_contents(self, open):
        pdftk = PDFTKWrapper(encoding='utf-2000')
        decoder = Mock(return_value='decoded')
        # check with no decode
        mock_bytestring = Mock(decode=decoder)
        open.return_value.read.return_value = mock_bytestring
        result = pdftk._get_file_contents('path')
        self.assertEqual(result, mock_bytestring)
        open.assert_called_once_with('path', 'rb')
        decoder.assert_not_called()
        # check with decode
        open.reset_mock()
        open.return_value.read.return_value = mock_bytestring
        result = pdftk._get_file_contents('path', decode=True)
        self.assertEqual(result, 'decoded')
        open.assert_called_once_with('path', 'rb')
        decoder.assert_called_once_with('utf-2000')

    def test_parse_fdf(self):
        pdftk = PDFTKWrapper()
        results = list(pdftk.parse_fdf_fields(FDF_STR_SAMPLE))
        self.assertListEqual(results, PARSED_FDF_FIELDS)

    def test_parse_data_fields(self):
        pdftk = PDFTKWrapper()
        results = list(pdftk.parse_data_fields(
            DATA_FIELDS_STR_SAMPLE))
        self.assertListEqual(results, PARSED_DATA_FIELDS)



















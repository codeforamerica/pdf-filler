from unittest import TestCase
from unittest.mock import Mock, patch
from src.pdfparser import (
    PDFParser, PDFParserError
    )

# these are based on the pdf form in 'data/sample_pdfs/sample_form.pdf'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          'escaped_name': 'Address Street', 'name_span': (568, 582), 'value_template': '()', 'value_template_span': (561, 563)}), ('Drivers License', {'name': 'Drivers License', 'escaped_name': 'Drivers License', 'name_span': (601, 616), 'value_template': '()', 'value_template_span': (594, 596)}), ('Other phone number', {'name': 'Other phone number', 'escaped_name': 'Other phone number', 'name_span': (635, 653), 'value_template': '()', 'value_template_span': (628, 630)}), ('If probation where and when?', {'name': 'If probation where and when?', 'escaped_name': 'If probation where and when?', 'name_span': (672, 700), 'value_template': '()', 'value_template_span': (665, 667)}), ('Dates arrested outside SF', {'name': 'Dates arrested outside SF', 'escaped_name': 'Dates arrested outside SF', 'name_span': (719, 744), 'value_template': '()', 'value_template_span': (712, 714)}), ('Address Zip', {'name': 'Address Zip', 'escaped_name': 'Address Zip', 'name_span': (763, 774), 'value_template': '()', 'value_template_span': (756, 758)}), ('On probation or parole', {'name': 'On probation or parole', 'escaped_name': 'On probation or parole', 'name_span': (792, 814), 'value_template': '/', 'value_template_span': (786, 787)}), ('Charged with a crime', {'name': 'Charged with a crime', 'escaped_name': 'Charged with a crime', 'name_span': (832, 852), 'value_template': '/', 'value_template_span': (826, 827)}), ('Serving a sentence', {'name': 'Serving a sentence', 'escaped_name': 'Serving a sentence', 'name_span': (870, 888), 'value_template': '/', 'value_template_span': (864, 865)}), ('Date of Birth', {'name': 'Date of Birth', 'escaped_name': 'Date of Birth', 'name_span': (907, 920), 'value_template': '()', 'value_template_span': (900, 902)}), ('Work phone number', {'name': 'Work phone number', 'escaped_name': 'Work phone number', 'name_span': (939, 956), 'value_template': '()', 'value_template_span': (932, 934)}), ('Cell phone number', {'name': 'Cell phone number', 'escaped_name': 'Cell phone number', 'name_span': (975, 992), 'value_template': '()', 'value_template_span': (968, 970)}), ('Date', {'name': 'Date', 'escaped_name': 'Date', 'name_span': (1011, 1015), 'value_template': '()', 'value_template_span': (1004, 1006)}), ('Address City', {'name': 'Address City', 'escaped_name': 'Address City', 'name_span': (1034, 1046), 'value_template': '()', 'value_template_span': (1027, 1029)}), ('Employed', {'name': 'Employed', 'escaped_name': 'Employed', 'name_span': (1064, 1072), 'value_template': '/', 'value_template_span': (1058, 1059)})]
FIELD_DATA = {'fields': [{'positions': [{'height': 28.95904541015625, 'top': 626.6790161132812, 'width': 78.52290344238281, 'left': 32.47710037231445, 'page': 1}], 'name': 'Date', 'altText': '', 'value': '', 'tabIndex': 0, 'required': False, 'type': 'text'}, {'positions': [{'height': 29.57904052734375, 'top': 627.2990112304688, 'width': 211.48599243164062, 'left': 115.51399993896484, 'page': 1}], 'name': 'Last Name', 'altText': '', 'value': '', 'tabIndex': 1, 'required': False, 'type': 'text'}, {'positions': [{'height': 30.19903564453125, 'top': 627.9190063476562, 'width': 212.906005859375, 'left': 330.093994140625, 'page': 1}], 'name': 'First Name', 'altText': '', 'value': '', 'tabIndex': 2, 'required': False, 'type': 'text'}, {'positions': [{'height': 29.43902587890625, 'top': 627.1589965820312, 'width': 37.10198974609375, 'left': 546.93798828125, 'page': 1}], 'name': 'MI', 'altText': '', 'value': '', 'tabIndex': 3, 'required': False, 'type': 'text'}, {'positions': [{'height': 28.79998779296875, 'top': 581.1599731445312, 'width': 164.04000854492188, 'left': 32.7599983215332, 'page': 1}], 'name': 'Social Security Number', 'altText': '', 'value': '', 'tabIndex': 4, 'required': False, 'type': 'text'}, {'positions': [{'height': 28.79998779296875, 'top': 581.1599731445312, 'width': 127.91998291015625, 'left': 199.32000732421875, 'page': 1}], 'name': 'Drivers License', 'altText': '', 'value': '', 'tabIndex': 5, 'required': False, 'type': 'text'}, {'positions': [{'height': 30.29901123046875, 'top': 582.6589965820312, 'width': 158.10699462890625, 'left': 330.89300537109375, 'page': 1}], 'name': 'Date of Birth', 'altText': '', 'value': '', 'tabIndex': 6, 'required': False, 'type': 'text'}, {'positions': [{'height': 11.781005859375, 'top': 565.0560302734375, 'width': 9.9219970703125, 'left': 550.6179809570312, 'page': 1}, {'height': 11.781005859375, 'top': 565.0560302734375, 'width': 9.9219970703125, 'left': 550.6179809570312, 'page': 1}], 'name': 'US Citizen', 'altText': '', 'options': ['No', 'Off', 'Yes'], 'value': '', 'tabIndex': 7, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 24.60498046875, 'top': 537.9509887695312, 'width': 242.3610076904297, 'left': 33.21699905395508, 'page': 1}], 'name': 'Address Street', 'altText': '', 'value': '', 'tabIndex': 9, 'required': False, 'type': 'text'}, {'positions': [{'height': 26.45001220703125, 'top': 539.1810302734375, 'width': 150.70700073242188, 'left': 281.7300109863281, 'page': 1}], 'name': 'Address City', 'altText': '', 'value': '', 'tabIndex': 10, 'required': False, 'type': 'text'}, {'positions': [{'height': 23.989990234375, 'top': 537.9509887695312, 'width': 48.595001220703125, 'left': 436.12799072265625, 'page': 1}], 'name': 'Address State', 'altText': '', 'value': '', 'tabIndex': 11, 'required': False, 'type': 'text'}, {'positions': [{'height': 21.52899169921875, 'top': 538.5659790039062, 'width': 86.11798095703125, 'left': 494.56500244140625, 'page': 1}], 'name': 'Address Zip', 'altText': '', 'value': '', 'tabIndex': 12, 'required': False, 'type': 'text'}, {'positions': [{'height': 11.071990966796875, 'top': 513.9609985351562, 'width': 11.68798828125, 'left': 553.0020141601562, 'page': 1}, {'height': 11.071990966796875, 'top': 513.9609985351562, 'width': 11.68798828125, 'left': 553.0020141601562, 'page': 1}], 'name': 'May we send mail here', 'altText': '', 'options': ['No', 'Off', 'Yes'], 'value': '', 'tabIndex': 13, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 21.52899169921875, 'top': 486.8949890136719, 'width': 129.17739868164062, 'left': 97.19059753417969, 'page': 1}], 'name': 'Cell phone number', 'altText': '', 'value': '', 'tabIndex': 15, 'required': False, 'type': 'text'}, {'positions': [{'height': 20.91400146484375, 'top': 486.8949890136719, 'width': 118.10501098632812, 'left': 235.59500122070312, 'page': 1}], 'name': 'Home phone number', 'altText': '', 'value': '', 'tabIndex': 16, 'required': False, 'type': 'text'}, {'positions': [{'height': 19.683990478515625, 'top': 486.2799987792969, 'width': 107.64801025390625, 'left': 359.2359924316406, 'page': 1}], 'name': 'Work phone number', 'altText': '', 'value': '', 'tabIndex': 17, 'required': False, 'type': 'text'}, {'positions': [{'height': 18.454010009765625, 'top': 486.2799987792969, 'width': 110.72299194335938, 'left': 469.9599914550781, 'page': 1}], 'name': 'Other phone number', 'altText': '', 'value': '', 'tabIndex': 18, 'required': False, 'type': 'text'}, {'positions': [{'height': 12.303009033203125, 'top': 465.3659973144531, 'width': 11.68798828125, 'left': 553.0020141601562, 'page': 1}, {'height': 12.303009033203125, 'top': 465.3659973144531, 'width': 11.68798828125, 'left': 553.0020141601562, 'page': 1}], 'name': 'May we leave voicemail', 'altText': '', 'options': ['No', 'Off', 'Yes'], 'value': '', 'tabIndex': 19, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 12.302001953125, 'top': 416.1549987792969, 'width': 12.302978515625, 'left': 553.0020141601562, 'page': 1}, {'height': 12.302001953125, 'top': 416.1549987792969, 'width': 12.302978515625, 'left': 553.0020141601562, 'page': 1}], 'name': 'On probation or parole', 'altText': '', 'options': ['Off', 'Yes', 'No'], 'value': '', 'tabIndex': 21, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 25.32000732421875, 'top': 450.6000061035156, 'width': 470.4789733886719, 'left': 113.44100189208984, 'page': 1}], 'name': 'Email Address', 'altText': '', 'value': '', 'tabIndex': 22, 'required': False, 'type': 'text'}, {'positions': [{'height': 11.68701171875, 'top': 401.3919982910156, 'width': 12.302978515625, 'left': 552.3870239257812, 'page': 1}, {'height': 11.68701171875, 'top': 401.3919982910156, 'width': 12.302978515625, 'left': 552.3870239257812, 'page': 1}], 'name': 'Serving a sentence', 'altText': '', 'options': ['Off', 'Yes', 'No'], 'value': '', 'tabIndex': 24, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 11.686981201171875, 'top': 387.2439880371094, 'width': 13.53302001953125, 'left': 551.77197265625, 'page': 1}, {'height': 11.686981201171875, 'top': 387.2439880371094, 'width': 13.53302001953125, 'left': 551.77197265625, 'page': 1}], 'name': 'Charged with a crime', 'altText': '', 'options': ['Off', 'Yes', 'No'], 'value': '', 'tabIndex': 26, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 11.072998046875, 'top': 342.9549865722656, 'width': 11.072998046875, 'left': 553.6170043945312, 'page': 1}, {'height': 11.072998046875, 'top': 342.9549865722656, 'width': 11.072998046875, 'left': 553.6170043945312, 'page': 1}], 'name': 'Arrested outside SF', 'altText': '', 'options': ['Off', 'Yes', 'No'], 'value': '', 'tabIndex': 28, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 20.91400146484375, 'top': 373.09600830078125, 'width': 314.33197021484375, 'left': 268.81201171875, 'page': 1}], 'name': 'If probation where and when?', 'altText': '', 'value': '', 'tabIndex': 29, 'required': False, 'type': 'text'}, {'positions': [{'height': 27.066009521484375, 'top': 328.8070068359375, 'width': 430.59100341796875, 'left': 150.0919952392578, 'page': 1}], 'name': 'Dates arrested outside SF', 'altText': '', 'value': '', 'tabIndex': 31, 'required': False, 'type': 'text'}, {'positions': [{'height': 12.303009033203125, 'top': 291.28399658203125, 'width': 11.072021484375, 'left': 554.2329711914062, 'page': 1}, {'height': 12.303009033203125, 'top': 291.28399658203125, 'width': 11.072021484375, 'left': 554.2329711914062, 'page': 1}], 'name': 'Employed', 'altText': '', 'options': ['Off', 'Yes', 'No'], 'value': '', 'tabIndex': 32, 'required': False, 'type': 'radio button'}, {'positions': [{'height': 18.239013671875, 'top': 278.20001220703125, 'width': 135.04901123046875, 'left': 210.14599609375, 'page': 1}], 'name': 'What is your monthly income', 'altText': '', 'value': '', 'tabIndex': 34, 'required': False, 'type': 'text'}, {'positions': [{'height': 18.360000610351562, 'top': 250.1999969482422, 'width': 125.6400146484375, 'left': 343.67999267578125, 'page': 1}], 'name': 'Monthly expenses', 'altText': '', 'value': '', 'tabIndex': 35, 'required': False, 'type': 'text'}, {'positions': [{'height': 19.800003051757812, 'top': 216.0, 'width': 304.5599670410156, 'left': 279.4800109863281, 'page': 1}], 'name': 'How did you hear about the Clean Slate Program', 'altText': '', 'value': '', 'tabIndex': 36, 'required': False, 'type': 'text'}], 'appearance': {'font': 0, 'fontColor': 2, 'fontSize': 1}}
CHECKBOX_SAMPLE = [{'name': 'Check Box2', 'options': ['Off', 'Yes'], 'type': 'button'}, {
    'name': 'Check Box3', 'options': ['Off', 'Yes'], 'type': 'button'}]
RADIO_SAMPLE = [{'name': 'Radio Buttons', 'type': 'button',
                 'options': ['Off', 'blue', 'red', 'yellow']}]
LISTBOX_SAMPLE = [{'options': [
    'apple', 'banana', 'durian', 'orange'], 'type': 'choice', 'name': 'List Box1'}]
DROPDOWN_SAMPLE = [{'value': '河', 'type': 'choice',
                    'name': 'Dropdown5', 'options': ['river', 'río', '河', '강']}]
TEXT_SAMPLE = [{'name': 'multiline', 'type': 'text'},
               {'name': 'single', 'type': 'text'}]


class TestPDFParser(TestCase):

    def test_init(self):
        pdfparser = PDFParser()
        self.assertEqual(pdfparser.TEMP_FOLDER_PATH, None)
        self.assertEqual(pdfparser.PDFPARSER_PATH, 'pdfparser.jar')
        pdfparser = PDFParser(tmp_path='data', clean_up=False)
        self.assertEqual(pdfparser.TEMP_FOLDER_PATH, 'data')
        self.assertEqual(pdfparser.clean_up, False)

    @patch('src.pdfparser.subprocess')
    def test_run_command(self, subprocess):
        pdfparser = PDFParser()
        comm_err = Mock(return_value=(b'', b'an error'))
        comm_out = Mock(return_value=(b'success', b''))
        proc_out = Mock(communicate=comm_out)
        proc_err = Mock(communicate=comm_err)
        popen_yes = Mock(return_value=proc_out)
        popen_bad = Mock(return_value=proc_err)

        # check the good case
        subprocess.Popen = popen_yes
        args = ['pdf_action', 'go']
        full_args = ['java', '-jar', 'pdfparser.jar'] + args
        result = pdfparser.run_command(args)
        self.assertEqual('success', result)
        popen_yes.assert_called_once_with(full_args,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        comm_out.assert_called_once_with()
        proc_out.assert_not_called()

        # check the bad case
        subprocess.reset_mock()
        subprocess.Popen = popen_bad
        args = ['go']
        with self.assertRaises(PDFParserError):
            pdfparser.run_command(args)
        full_args = ['java', '-jar', 'pdfparser.jar'] + args
        proc_err.assert_not_called()
        comm_err.assert_called_once_with()
        popen_bad.assert_called_once_with(full_args,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @patch('src.pdfparser.mkstemp')
    @patch('builtins.open')
    def test_write_tmp_file(self, open, mkstemp):
        mkstemp.return_value = ('os.file', 'filepath')
        mock_file = Mock()

        # check with file_object
        pdfparser = PDFParser()
        path = pdfparser._write_tmp_file(mock_file)
        mkstemp.assert_called_once_with(dir=pdfparser.TEMP_FOLDER_PATH)
        open.assert_called_once_with('filepath', 'wb')
        mock_file.read.assert_called_once_with()
        self.assertEqual(path, 'filepath')
        self.assertListEqual(pdfparser._tmp_files, ['filepath'])

        # check with bytes
        pdfparser = PDFParser()
        mkstemp.reset_mock()
        open.reset_mock()
        path = pdfparser._write_tmp_file(bytestring=b'content')
        open.assert_called_once_with('filepath', 'wb')
        self.assertEqual(path, 'filepath')
        self.assertListEqual(pdfparser._tmp_files, ['filepath'])

    @patch('src.pdfparser.os.remove')
    def test_clean_up_tmp_files(self, remove):
        pdfparser = PDFParser()
        paths = [c for c in 'hello']
        pdfparser._tmp_files = paths
        pdfparser.clean_up_tmp_files()
        for p in paths:
            remove.assert_any_call(p)
        self.assertListEqual(pdfparser._tmp_files, [])
        # test with no files
        remove.reset_mock()
        pdfparser.clean_up_tmp_files()
        remove.assert_not_called()

    def test_coerce_to_file_path(self):
        pdfparser = PDFParser()
        wrt_tmp = Mock(return_value='path')
        pdfparser._write_tmp_file = wrt_tmp

        # check with a string input
        result = pdfparser._coerce_to_file_path('goodpath')
        self.assertEqual(result, 'goodpath')
        wrt_tmp.assert_not_called()

        # check with a bytestring input
        bstring = b'foo'
        result = pdfparser._coerce_to_file_path(bstring)
        self.assertEqual(result, 'path')
        wrt_tmp.assert_called_once_with(bytestring=bstring)

        # check with a not string input
        wrt_tmp.reset_mock()
        not_string = Mock()
        result = pdfparser._coerce_to_file_path(not_string)
        self.assertEqual(result, 'path')
        wrt_tmp.assert_called_once_with(file_obj=not_string)

    @patch('builtins.open')
    def test_get_file_contents(self, open):
        pdfparser = PDFParser()
        open.return_value.read.return_value = b'data'
        result = pdfparser._get_file_contents('path')
        self.assertEqual(result, b'data')
        open.assert_called_once_with('path', 'rb')

    def test_fill_pdf(self):
        pdfparser = PDFParser()
        fake_answers = Mock()
        fake_path = "some/fake/path.pdf"

        coerce_to_file_path = Mock(return_value=fake_path)
        pdfparser._coerce_to_file_path = coerce_to_file_path

        fake_get_fields = Mock(return_value='field data')
        pdfparser.get_field_data = fake_get_fields

        fake_get_options = Mock(return_value='options')
        pdfparser._get_name_option_lookup = fake_get_options

        output_path = 'output'
        write_tmp = Mock(return_value=output_path)
        pdfparser._write_tmp_file = write_tmp

        fake_fill = Mock()
        pdfparser._fill = fake_fill

        fake_file_contents = b'a pdf'
        fake_get_contents = Mock(return_value=fake_file_contents)
        pdfparser._get_file_contents = fake_get_contents

        clean_up_tmp_files = Mock()
        pdfparser.clean_up_tmp_files = clean_up_tmp_files

        # run the method
        result = pdfparser.fill_pdf(fake_path, fake_answers)

        coerce_to_file_path.assert_called_with(fake_path)
        fake_get_fields.assert_called_once_with(fake_path)
        fake_get_options.assert_called_once_with('field data')
        write_tmp.assert_called_once_with()
        fake_fill.assert_called_once_with(fake_path, output_path,
            'options', fake_answers)
        fake_get_contents.assert_called_once_with(output_path)
        clean_up_tmp_files.assert_called_with()
        self.assertEqual(result, fake_file_contents)

        clean_up_tmp_files.reset_mock()
        pdfparser.clean_up = False
        pdfparser.fill_pdf(fake_path, fake_answers)
        clean_up_tmp_files.assert_not_called()

    def test_fill_many_pdfs(self):
        pdfparser = PDFParser()
        fake_answer = Mock()
        fake_multiple_answers = [fake_answer]

        fake_path = "some/fake/path.pdf"

        coerce_to_file_path = Mock(return_value=fake_path)
        pdfparser._coerce_to_file_path = coerce_to_file_path

        fake_get_fields = Mock(return_value='field data')
        pdfparser.get_field_data = fake_get_fields

        fake_get_options = Mock(return_value='options')
        pdfparser._get_name_option_lookup = fake_get_options

        fake_fill = Mock()
        pdfparser._fill = fake_fill

        fake_write_tmp_file = Mock(return_value='output path')
        pdfparser._write_tmp_file = fake_write_tmp_file

        fake_join_pdfs = Mock(return_value='filled_pdf')
        pdfparser.join_pdfs = fake_join_pdfs

        #run the method
        result = pdfparser.fill_many_pdfs(fake_path, fake_multiple_answers)

        self.assertEqual(result, 'filled_pdf')
        coerce_to_file_path.assert_called_once_with(fake_path)
        fake_get_fields.assert_called_once_with(fake_path)
        fake_get_options.assert_called_once_with('field data')
        fake_fill.assert_called_once_with(fake_path, 'output path',
            'options', fake_answer)
        fake_join_pdfs.assert_called_with(['output path'])

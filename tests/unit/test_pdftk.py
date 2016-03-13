from unittest import TestCase
from unittest.mock import Mock, patch
from src.pdftk_wrapper import PDFTKWrapper, PdftkError

# these are based on the pdf form in 'data/sample_pdfs/sample_form.pdf'
FDF_STR_SAMPLE = "%FDF-1.2\n%âãÏÓ\n1 0 obj \n<<\n/FDF \n<<\n/Fields [\n<<\n/V /Jalape#f1o\n/T (Check Box4)\n>> \n<<\n/V /Yes\n/T (Check Box3)\n>> \n<<\n/V (fig)\n/T (Dropdown9)\n>> \n<<\n/V (unless you are a cheese)\n/T (Dropdown8)\n>> \n<<\n/V /Yes\n/T (Check Box2)\n>> \n<<\n/V /Yes\n/T (Check Box1)\n>> \n<<\n/V (Choice1)\n/T (Group9)\n>> \n<<\n/V /Choice4\n/T (Group8)\n>> \n<<\n/V (Just another text field)\n/T (MötleyCrüe)\n>> \n<<\n/V /Choice1\n/T (Group7)\n>> \n<<\n/V (lawn)\n/T (List Box11)\n>> \n<<\n/V (Buying an Ant)\n/T (List Box10)\n>> \n<<\n/V (What is going on here???)\n/T (Text field with spaces in name)\n>> \n<<\n/V (¡Ojalá!)\n/T (Text12)\n>> \n<<\n/V /Yes\n/T (Check Box6)\n>> \n<<\n/V /Yes\n/T (Check Box5)\n>> \n<<\n/V (Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.)\n/T (Multi line text)\n>>]\n>>\n>>\nendobj \ntrailer\n\n<<\n/Root 1 0 R\n>>\n%%EOF\n"
DATA_FIELDS_STR_SAMPLE = "---\nFieldType: Button\nFieldName: Check Box1\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Check Box2\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Check Box3\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Check Box4\nFieldFlags: 0\nFieldValue: Jalape&#241;o\nFieldJustification: Left\nFieldStateOption: Jalape&#241;o\nFieldStateOption: Off\n---\nFieldType: Button\nFieldName: Check Box5\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Check Box6\nFieldFlags: 0\nFieldValue: Yes\nFieldJustification: Left\nFieldStateOption: Off\nFieldStateOption: Yes\n---\nFieldType: Button\nFieldName: Group7\nFieldFlags: 49152\nFieldValue: Choice1\nFieldJustification: Left\nFieldStateOption: Choice1\nFieldStateOption: Choice2\nFieldStateOption: Choice3\nFieldStateOption: Off\n---\nFieldType: Button\nFieldName: Group8\nFieldFlags: 49152\nFieldValue: Choice4\nFieldJustification: Left\nFieldStateOption: Choice4\nFieldStateOption: Choice5\nFieldStateOption: Off\n---\nFieldType: Choice\nFieldName: Dropdown8\nFieldFlags: 131072\nFieldValue: unless you are a cheese\nFieldJustification: Left\n---\nFieldType: Choice\nFieldName: Dropdown9\nFieldFlags: 393216\nFieldValue: fig\nFieldValueDefault: apple\nFieldJustification: Left\nFieldStateOption: apple\nFieldStateOption: apricot\nFieldStateOption: banana\nFieldStateOption: cranberry\nFieldStateOption: date\nFieldStateOption: fig\nFieldStateOption: grape\nFieldStateOption: lime\nFieldStateOption: mango\nFieldStateOption: orange\nFieldStateOption: peach\nFieldStateOption: raspberry\nFieldStateOption: tamarind\n---\nFieldType: Button\nFieldName: Group9\nFieldFlags: 49152\nFieldValue: 1\nFieldJustification: Left\nFieldStateOption: 0\nFieldStateOption: 1\nFieldStateOption: 2\nFieldStateOption: Choice1\nFieldStateOption: Choice2\nFieldStateOption: Off\n---\nFieldType: Choice\nFieldName: List Box10\nFieldFlags: 2097152\nFieldValue: Buying an Ant\nFieldValueDefault: The Olympic Hide and Seek Final\nFieldJustification: Left\nFieldStateOption: Bruces\nFieldStateOption: Court Scene – Multiple Murderer\nFieldStateOption: Musical Mice\nFieldStateOption: Scott of the Antarctic\nFieldStateOption: Scott of the Sahara\nFieldStateOption: The Battle of Pearl Harbor\nFieldStateOption: The Olympic Hide and Seek Final\nFieldStateOption: The Visitors\n---\nFieldType: Choice\nFieldName: List Box11\nFieldFlags: 0\nFieldValue: lawn\nFieldJustification: Left\n---\nFieldType: Text\nFieldName: Text12\nFieldFlags: 0\nFieldValue: ¡Ojalá!\nFieldJustification: Left\n---\nFieldType: Text\nFieldName: MötleyCrüe\nFieldFlags: 0\nFieldValue: Just another text field\nFieldJustification: Left\n---\nFieldType: Text\nFieldName: Multi line text\nFieldFlags: 4096\nFieldValue: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.\nFieldJustification: Left\n---\nFieldType: Text\nFieldName: Text field with spaces in name\nFieldFlags: 0\nFieldValue: What is going on here???\nFieldJustification: Left\n"
PARSED_FDF_FIELDS = [('Check Box4', {'escaped_name': 'Check Box4', 'name': 'Check Box4', 'value_template_span': (52, 63), 'value_template': '/Jalape#f1o', 'name_span': (68, 78)}), ('Check Box3', {'escaped_name': 'Check Box3', 'name': 'Check Box3', 'value_template_span': (90, 94), 'value_template': '/Yes', 'name_span': (99, 109)}), ('Dropdown9', {'escaped_name': 'Dropdown9', 'name': 'Dropdown9', 'value_template_span': (121, 126), 'value_template': '(fig)', 'name_span': (131, 140)}), ('Dropdown8', {'escaped_name': 'Dropdown8', 'name': 'Dropdown8', 'value_template_span': (152, 177), 'value_template': '(unless you are a cheese)', 'name_span': (182, 191)}), ('Check Box2', {'escaped_name': 'Check Box2', 'name': 'Check Box2', 'value_template_span': (203, 207), 'value_template': '/Yes', 'name_span': (212, 222)}), ('Check Box1', {'escaped_name': 'Check Box1', 'name': 'Check Box1', 'value_template_span': (234, 238), 'value_template': '/Yes', 'name_span': (243, 253)}), ('Group9', {'escaped_name': 'Group9', 'name': 'Group9', 'value_template_span': (265, 274), 'value_template': '(Choice1)', 'name_span': (279, 285)}), ('Group8', {'escaped_name': 'Group8', 'name': 'Group8', 'value_template_span': (297, 305), 'value_template': '/Choice4', 'name_span': (310, 316)}), ('MötleyCrüe', {'escaped_name': 'MötleyCrüe', 'name': 'MötleyCrüe', 'value_template_span': (328, 353), 'value_template': '(Just another text field)', 'name_span': (358, 368)}), ('Group7', {'escaped_name': 'Group7', 'name': 'Group7', 'value_template_span': (380, 388), 'value_template': '/Choice1', 'name_span': (393, 399)}), ('List Box11', {'escaped_name': 'List Box11', 'name': 'List Box11', 'value_template_span': (411, 417), 'value_template': '(lawn)', 'name_span': (422, 432)}), ('List Box10', {'escaped_name': 'List Box10', 'name': 'List Box10', 'value_template_span': (444, 459), 'value_template': '(Buying an Ant)', 'name_span': (464, 474)}), ('Text field with spaces in name', {'escaped_name': 'Text field with spaces in name', 'name': 'Text field with spaces in name', 'value_template_span': (486, 512), 'value_template': '(What is going on here???)', 'name_span': (517, 547)}), ('Text12', {'escaped_name': 'Text12', 'name': 'Text12', 'value_template_span': (559, 568), 'value_template': '(¡Ojalá!)', 'name_span': (573, 579)}), ('Check Box6', {'escaped_name': 'Check Box6', 'name': 'Check Box6', 'value_template_span': (591, 595), 'value_template': '/Yes', 'name_span': (600, 610)}), ('Check Box5', {'escaped_name': 'Check Box5', 'name': 'Check Box5', 'value_template_span': (622, 626), 'value_template': '/Yes', 'name_span': (631, 641)}), ('Multi line text', {'escaped_name': 'Multi line text', 'name': 'Multi line text', 'value_template_span': (653, 853), 'value_template': '(Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.)', 'name_span': (858, 873)})]
PARSED_DATA_FIELDS = [('Check Box1', {'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldStateOption': ['Off', 'Yes'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box1'}), ('Check Box2', {'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldStateOption': ['Off', 'Yes'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box2'}), ('Check Box3', {'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldStateOption': ['Off', 'Yes'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box3'}), ('Check Box4', {'FieldValue': 'Jalape&#241;o', 'FieldType': 'Button', 'FieldStateOption': ['Jalape&#241;o', 'Off'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box4'}), ('Check Box5', {'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldStateOption': ['Off', 'Yes'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box5'}), ('Check Box6', {'FieldValue': 'Yes', 'FieldType': 'Button', 'FieldStateOption': ['Off', 'Yes'], 'FieldJustification': 'Left', 'FieldFlags': '0', 'FieldName': 'Check Box6'}), ('Group7', {'FieldValue': 'Choice1', 'FieldType': 'Button', 'FieldStateOption': ['Choice1', 'Choice2', 'Choice3', 'Off'], 'FieldJustification': 'Left', 'FieldFlags': '49152', 'FieldName': 'Group7'}), ('Group8', {'FieldValue': 'Choice4', 'FieldType': 'Button', 'FieldStateOption': ['Choice4', 'Choice5', 'Off'], 'FieldJustification': 'Left', 'FieldFlags': '49152', 'FieldName': 'Group8'}), ('Dropdown8', {'FieldValue': 'unless you are a cheese', 'FieldJustification': 'Left', 'FieldType': 'Choice', 'FieldFlags': '131072', 'FieldName': 'Dropdown8'}), ('Dropdown9', {'FieldValue': 'fig', 'FieldType': 'Choice', 'FieldStateOption': ['apple', 'apricot', 'banana', 'cranberry', 'date', 'fig', 'grape', 'lime', 'mango', 'orange', 'peach', 'raspberry', 'tamarind'], 'FieldJustification': 'Left', 'FieldFlags': '393216', 'FieldName': 'Dropdown9', 'FieldValueDefault': 'apple'}), ('Group9', {'FieldValue': '1', 'FieldType': 'Button', 'FieldStateOption': ['0', '1', '2', 'Choice1', 'Choice2', 'Off'], 'FieldJustification': 'Left', 'FieldFlags': '49152', 'FieldName': 'Group9'}), ('List Box10', {'FieldValue': 'Buying an Ant', 'FieldType': 'Choice', 'FieldStateOption': ['Bruces', 'Court Scene – Multiple Murderer', 'Musical Mice', 'Scott of the Antarctic', 'Scott of the Sahara', 'The Battle of Pearl Harbor', 'The Olympic Hide and Seek Final', 'The Visitors'], 'FieldJustification': 'Left', 'FieldFlags': '2097152', 'FieldName': 'List Box10', 'FieldValueDefault': 'The Olympic Hide and Seek Final'}), ('List Box11', {'FieldValue': 'lawn', 'FieldJustification': 'Left', 'FieldType': 'Choice', 'FieldFlags': '0', 'FieldName': 'List Box11'}), ('Text12', {'FieldValue': '¡Ojalá!', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'Text12'}), ('MötleyCrüe', {'FieldValue': 'Just another text field', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'MötleyCrüe'}), ('Multi line text', {'FieldValue': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '4096', 'FieldName': 'Multi line text'}), ('Text field with spaces in name', {'FieldValue': 'What is going on here???', 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'Text field with spaces in name'})]
FIELD_DATA_MAP_SAMPLE = {'MötleyCrüe': {'fdf': {'value_template_span': (328, 353), 'escaped_name': 'MötleyCrüe', 'name_span': (358, 368), 'name': 'MötleyCrüe', 'value_template': '(Just another text field)'}, 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'MötleyCrüe', 'FieldValue': 'Just another text field'}, 'Check Box5': {'fdf': {'value_template_span': (622, 626), 'escaped_name': 'Check Box5', 'name_span': (631, 641), 'name': 'Check Box5', 'value_template': '/Yes'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box5', 'FieldStateOption': ['Off', 'Yes'], 'FieldValue': 'Yes'}, 'Multi line text': {'fdf': {'value_template_span': (653, 853), 'escaped_name': 'Multi line text', 'name_span': (858, 873), 'name': 'Multi line text', 'value_template': '(Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.)'}, 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '4096', 'FieldName': 'Multi line text', 'FieldValue': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.'}, 'Check Box6': {'fdf': {'value_template_span': (591, 595), 'escaped_name': 'Check Box6', 'name_span': (600, 610), 'name': 'Check Box6', 'value_template': '/Yes'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box6', 'FieldStateOption': ['Off', 'Yes'], 'FieldValue': 'Yes'}, 'Check Box2': {'fdf': {'value_template_span': (203, 207), 'escaped_name': 'Check Box2', 'name_span': (212, 222), 'name': 'Check Box2', 'value_template': '/Yes'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box2', 'FieldStateOption': ['Off', 'Yes'], 'FieldValue': 'Yes'}, 'Check Box3': {'fdf': {'value_template_span': (90, 94), 'escaped_name': 'Check Box3', 'name_span': (99, 109), 'name': 'Check Box3', 'value_template': '/Yes'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box3', 'FieldStateOption': ['Off', 'Yes'], 'FieldValue': 'Yes'}, 'Group9': {'fdf': {'value_template_span': (265, 274), 'escaped_name': 'Group9', 'name_span': (279, 285), 'name': 'Group9', 'value_template': '(Choice1)'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '49152', 'FieldName': 'Group9', 'FieldStateOption': ['0', '1', '2', 'Choice1', 'Choice2', 'Off'], 'FieldValue': '1'}, 'Dropdown8': {'fdf': {'value_template_span': (152, 177), 'escaped_name': 'Dropdown8', 'name_span': (182, 191), 'name': 'Dropdown8', 'value_template': '(unless you are a cheese)'}, 'FieldJustification': 'Left', 'FieldType': 'Choice', 'FieldFlags': '131072', 'FieldName': 'Dropdown8', 'FieldValue': 'unless you are a cheese'}, 'List Box11': {'fdf': {'value_template_span': (411, 417), 'escaped_name': 'List Box11', 'name_span': (422, 432), 'name': 'List Box11', 'value_template': '(lawn)'}, 'FieldJustification': 'Left', 'FieldType': 'Choice', 'FieldFlags': '0', 'FieldName': 'List Box11', 'FieldValue': 'lawn'}, 'Dropdown9': {'FieldStateOption': ['apple', 'apricot', 'banana', 'cranberry', 'date', 'fig', 'grape', 'lime', 'mango', 'orange', 'peach', 'raspberry', 'tamarind'], 'fdf': {'value_template_span': (121, 126), 'escaped_name': 'Dropdown9', 'name_span': (131, 140), 'name': 'Dropdown9', 'value_template': '(fig)'}, 'FieldValueDefault': 'apple', 'FieldType': 'Choice', 'FieldFlags': '393216', 'FieldName': 'Dropdown9', 'FieldJustification': 'Left', 'FieldValue': 'fig'}, 'Check Box4': {'fdf': {'value_template_span': (52, 63), 'escaped_name': 'Check Box4', 'name_span': (68, 78), 'name': 'Check Box4', 'value_template': '/Jalape#f1o'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box4', 'FieldStateOption': ['Jalape&#241;o', 'Off'], 'FieldValue': 'Jalape&#241;o'}, 'List Box10': {'FieldStateOption': ['Bruces', 'Court Scene – Multiple Murderer', 'Musical Mice', 'Scott of the Antarctic', 'Scott of the Sahara', 'The Battle of Pearl Harbor', 'The Olympic Hide and Seek Final', 'The Visitors'], 'fdf': {'value_template_span': (444, 459), 'escaped_name': 'List Box10', 'name_span': (464, 474), 'name': 'List Box10', 'value_template': '(Buying an Ant)'}, 'FieldValueDefault': 'The Olympic Hide and Seek Final', 'FieldType': 'Choice', 'FieldFlags': '2097152', 'FieldName': 'List Box10', 'FieldJustification': 'Left', 'FieldValue': 'Buying an Ant'}, 'Text field with spaces in name': {'fdf': {'value_template_span': (486, 512), 'escaped_name': 'Text field with spaces in name', 'name_span': (517, 547), 'name': 'Text field with spaces in name', 'value_template': '(What is going on here???)'}, 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'Text field with spaces in name', 'FieldValue': 'What is going on here???'}, 'Text12': {'fdf': {'value_template_span': (559, 568), 'escaped_name': 'Text12', 'name_span': (573, 579), 'name': 'Text12', 'value_template': '(¡Ojalá!)'}, 'FieldJustification': 'Left', 'FieldType': 'Text', 'FieldFlags': '0', 'FieldName': 'Text12', 'FieldValue': '¡Ojalá!'}, 'Group7': {'fdf': {'value_template_span': (380, 388), 'escaped_name': 'Group7', 'name_span': (393, 399), 'name': 'Group7', 'value_template': '/Choice1'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '49152', 'FieldName': 'Group7', 'FieldStateOption': ['Choice1', 'Choice2', 'Choice3', 'Off'], 'FieldValue': 'Choice1'}, 'Group8': {'fdf': {'value_template_span': (297, 305), 'escaped_name': 'Group8', 'name_span': (310, 316), 'name': 'Group8', 'value_template': '/Choice4'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '49152', 'FieldName': 'Group8', 'FieldStateOption': ['Choice4', 'Choice5', 'Off'], 'FieldValue': 'Choice4'}, 'Check Box1': {'fdf': {'value_template_span': (234, 238), 'escaped_name': 'Check Box1', 'name_span': (243, 253), 'name': 'Check Box1', 'value_template': '/Yes'}, 'FieldJustification': 'Left', 'FieldType': 'Button', 'FieldFlags': '0', 'FieldName': 'Check Box1', 'FieldStateOption': ['Off', 'Yes'], 'FieldValue': 'Yes'}}
FIELD_DATA = [{'options': ['Off', 'Yes'], 'value': 'Yes', 'name': 'Check Box1', 'type': 'button'}, {'options': ['Off', 'Yes'], 'value': 'Yes', 'name': 'Check Box2', 'type': 'button'}, {'options': ['Off', 'Yes'], 'value': 'Yes', 'name': 'Check Box3', 'type': 'button'}, {'options': ['Jalape&#241;o', 'Off'], 'value': 'Jalape&#241;o', 'name': 'Check Box4', 'type': 'button'}, {'options': ['Off', 'Yes'], 'value': 'Yes', 'name': 'Check Box5', 'type': 'button'}, {'options': ['Off', 'Yes'], 'value': 'Yes', 'name': 'Check Box6', 'type': 'button'}, {'value': 'unless you are a cheese', 'name': 'Dropdown8', 'type': 'choice'}, {'options': ['apple', 'apricot', 'banana', 'cranberry', 'date', 'fig', 'grape', 'lime', 'mango', 'orange', 'peach', 'raspberry', 'tamarind'], 'value': 'fig', 'name': 'Dropdown9', 'type': 'choice'}, {'options': ['Choice1', 'Choice2', 'Choice3', 'Off'], 'value': 'Choice1', 'name': 'Group7', 'type': 'button'}, {'options': ['Choice4', 'Choice5', 'Off'], 'value': 'Choice4', 'name': 'Group8', 'type': 'button'}, {'options': ['0', '1', '2', 'Choice1', 'Choice2', 'Off'], 'value': '1', 'name': 'Group9', 'type': 'button'}, {'options': ['Bruces', 'Court Scene – Multiple Murderer', 'Musical Mice', 'Scott of the Antarctic', 'Scott of the Sahara', 'The Battle of Pearl Harbor', 'The Olympic Hide and Seek Final', 'The Visitors', 'Buying an Ant'], 'value': 'Buying an Ant', 'name': 'List Box10', 'type': 'choice'}, {'value': 'lawn', 'name': 'List Box11', 'type': 'choice'}, {'value': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor.', 'name': 'Multi line text', 'type': 'text'}, {'value': 'Just another text field', 'name': 'MötleyCrüe', 'type': 'text'}, {'value': 'What is going on here???', 'name': 'Text field with spaces in name', 'type': 'text'}, {'value': '¡Ojalá!', 'name': 'Text12', 'type': 'text'}]

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



















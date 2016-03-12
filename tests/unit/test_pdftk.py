from unittest import TestCase
from unittest.mock import Mock, patch

from src.pdftk_wrapper import PDFTKWrapper, PdftkError

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

    def test_parse_fdf_fields(self):
        pdftk = PDFTKWrapper()
        fdf_sample = """
        Something
        """
        fields = list(pdftk.parse_fdf_fields(fdf_sample))

    def test_parse_xfdf_fields(self):
        pdftk = PDFTKWrapper()
        xfdf_sample = """
        Something
        """
        fields = list(pdftk.parse_xfdf_fields(xfdf_sample))

    def test_parse_data_fields(self):
        pdftk = PDFTKWrapper()
        data_fields_sample = """
        Something
        """
        fields = list(pdftk.parse_data_fields(data_fields_sample))

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
        pdftk._clean_up_tmp_files()
        for p in paths:
            remove.assert_any_call(p)
        self.assertListEqual(pdftk._tmp_files, [])
        # test with no files
        remove.reset_mock()
        pdftk._clean_up_tmp_files()
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



















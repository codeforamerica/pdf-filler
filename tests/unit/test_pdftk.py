from unittest import TestCase
from unittest.mock import Mock, patch

from pdftk_wrapper import PDFTKWrapper, PdftkError

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
        fp = 'something.pdf'
        results = pdftk.get_fdf(fp)

    def test_get_xfdf(self):
        pdftk = PDFTKWrapper()
        fp = 'something.pdf'
        results = pdftk.get_xfdf(fp)

    def test_get_data_fields(self):
        pdftk = PDFTKWrapper()
        fp = 'something.pdf'
        results = pdftk.get_data_fields(fp)

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

    @patch('pdftk_wrapper.subprocess')
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
        with self.assertRaisesRegex(PdftkError, 'an error'):
            pdftk.run_command(args)
        proc_err.assert_not_called()
        comm_err.assert_called_once_with()
        popen_bad.assert_called_once_with(['pdftk','go'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)





from unittest import TestCase



class TestPDFTKTasks(TestCase):

    def test_parse_fdf(self):
        from src.pdfhook.tasks import parse_fdf_fields
        for name, data in parse_fdf_fields(FDF_STR_SAMPLE):
            self.assertIn('escaped_name', data)
            self.assertIn('name', data)
            self.assertIn('name_span', data)
            self.assertIn('value_template', data)
            self.assertIn('value_template_span', data)
            self.assertEqual(name, data['escaped_name'])

    def test_parse_pdf(self):
        from src.pdfhook.tasks import build_fdf_map
        path = 'data/tmp-Form fields sample.pdf'
        fields = build_fdf_map(path)
        for name, data in fields.items():
            self.assertIn('slug', data)
            self.assertIn('type', data)
            self.assertIn('escaped_name', data)
            self.assertIn('name', data)
            self.assertIn('name_span', data)
            self.assertIn('value_template', data)
            self.assertIn('value_template_span', data)
            self.assertEqual(name, data['slug'])

FDF_STR_SAMPLE = """%FDF-1.2
%âãÏÓ
1 0 obj
<<
/FDF
<<
/Fields [
<<
/V /
/T (Petitioner Requests a hearing)
>>
<<
/V ()
/T (Petitioner State)
>>
<<
/V ()
/T (Created November 2014)
>>
<<
/V ()
/T (Case Number)
>>
<<
/V ()
/T (Date of Execution)
>>
<<
/V ()
/T (Petitioner Street Address)
>>
<<
/V ()
/T (Petitioner City)
>>
<<
/V ()
/T (PETITION AND RESPONSE)
>>
<<
/V ()
/T (Code and Sections of Convictions)
>>
<<
/V ()
/T (Date of Birth)
>>
<<
/V ()
/T (Defendant)
>>
<<
/V ()
/T (Date of Conviction)
>>
<<
/V ()
/T (Fax Number)
>>
<<
/V ()
/T (Attorney For \(Name\))
>>
<<
/V ()
/T (Sentence Imposed)
>>
<<
/V ()
/T (Petitioner Zip Code)
>>
<<
/V /Yes
/T (Reduction to Misdemeanor)
>>
<<
/V /On
/T (FOR REDUCTION TO MISDEMEANOR)
>>
<<
/V ()
/T (E-Mail Address)
>>
<<
/V ()
/T (Telephone Number)
>>
<<
/V ()
/T (Signature of Petitioner or Attorney)
>>]
>>
>>
endobj
trailer

<<
/Root 1 0 R
>>
%%EOF"""

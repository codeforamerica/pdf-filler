import subprocess

class PdftkError(Exception):
    pass

class PDFTKWrapper:

    def __init__(self, encoding='latin-1', tmp_path=None):
        self.encoding = encoding
        self.TEMP_FOLDER_PATH = tmp_path

    def get_fdf(self, fp):
        return None

    def get_xfdf(self, fp):
        return None

    def get_data_fields(self, fp):
        return None

    def parse_fdf_fields(self, fdf_str):
        yield None

    def parse_xfdf_fields(self, xfdf_str):
        yield None

    def parse_data_fields(self, data_str):
        yield None

    def generate_fdf_map(self, fp):
        return None

    def run_command(self, args):
        if args[0] != 'pdftk':
            args.insert(0, 'pdftk')
        process = subprocess.Popen(args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            raise PdftkError(err.decode('utf-8'))
        return out.decode('utf-8')



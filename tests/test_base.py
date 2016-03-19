# -*- coding: utf-8 -*-
import os
from flask.ext.testing import TestCase as FlaskTestCase

from src.main import (
    create_app as _create_app,
    db
    )

def format_pdf_search_term(search_term, encoding='utf-8'):
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


class BaseTestCase(FlaskTestCase):
    '''
    A base test case that boots our app
    '''
    def create_app(self):
        os.environ['CONFIG'] = 'src.settings.TestConfig'
        app = _create_app()
        app.testing = True
        return app

    def setUp(self):
        FlaskTestCase.setUp(self)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()



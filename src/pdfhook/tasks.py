import subprocess
import io
import os
import codecs
import re

from slugify import slugify

TEMP_FOLDER_PATH = 'data'
DEFAULT_ENCODING = 'latin-1'


def dump_data_fields(pdf_file_path):
    field_dump_path = os.path.join(TEMP_FOLDER_PATH, 'tmp-data_fields.txt')
    args = [
        'pdftk',
        pdf_file_path,
        'dump_data_fields_utf8',
        'output',
        field_dump_path
    ]
    subprocess.call(args)
    return open(field_dump_path, 'r').read()


def generate_fdf(pdf_file_path):
    fdf_dump_path = os.path.join(TEMP_FOLDER_PATH, 'tmp-data.fdf')
    args = [
        'pdftk',
        pdf_file_path,
        'generate_fdf',
        'output',
        fdf_dump_path]
    subprocess.call(args)
    return codecs.open(fdf_dump_path, 'r', encoding=DEFAULT_ENCODING).read()


def generate_filled_pdf(pdf_path, fdf_path, filled_pdf_path):
    args = [
        'pdftk',
        pdf_path,
        'fill_form',
        fdf_path,
        'output',
        filled_pdf_path]
    subprocess.call(args)


def parse_fdf_fields(fdf_str):
    '''Yields a series of tuples, using the escaped name of the field
    followed by a dict with useful meta information about the match
        https://regex101.com/r/iL6hW3/5
    '''
    field_pattern = re.compile(r'\/V\ (?P<value>.*)\n\/T\ \((?P<name>.*)\)')
    for match in re.finditer(field_pattern, fdf_str):
        datum = {
            'name': match.group('name'),
            'escaped_name': match.group('name').replace('\\', ''),
            'name_span': match.span('name'),
            'value_template': match.group('value'),
            'value_template_span': match.span('value')
            }
        # it's necessary to deal with escape slashes in the field name
        yield (datum['escaped_name'], datum)

def parse_data_dump(field_dump_str):
    '''Pulls out a field name and type from the resulting string of
        `pdftk dump_data_fields_utf8`
    Uses the following regex to find types and names:
        https://regex101.com/r/iL6hW3/4
    '''
    field_dump_pattern = re.compile(
        r'FieldType:\ (?P<type>.*)\nFieldName:\ (?P<name>.*)')
    for match in re.finditer(field_dump_pattern, field_dump_str):
        yield (match.group('name'), match.group('type'))

# https://regex101.com/r/mH8sI9/2
boolean_value_pattern = re.compile(r'\/(?P<value>.+)\n?')
# https://regex101.com/r/mH8sI9/3
text_value_pattern = re.compile(r'\((?P<value>.+)\)')
def generate_key_for_field(field_data):
    if field_data['type'] == 'Text':
        m = text_value_pattern.match(field_data['value_template'])
        if m:
            return slugify(m.group())
    return slugify(field_data['escaped_name'])

def build_fdf_map(pdf_file_path):
    field_dump = dump_data_fields(pdf_file_path)
    fdf_dump = generate_fdf(pdf_file_path)
    fdf_fields = parse_fdf_fields(fdf_dump)
    data_fields = dict(parse_data_dump(field_dump))
    field_map = {}
    for key, field_data in fdf_fields:
        field_data['type'] = data_fields[key]
        slug = generate_key_for_field(field_data)
        field_data['slug'] = slug
        field_map[slug] = field_data
    return field_map

def fill_fdf(fdf_str, mapping, data):
    insertions = []
    for key in data:
        if key in mapping:
            field = mapping[key]
            if field['type'] == 'Text':
                span = field['value_template_span']
                start = span[0] + 1
                end = span[1] - 1
                value = str(data[key])
                insertions.append((start, end, value))
            elif field['type'] == 'Button':
                span = field['value_template_span']
                start = span[0] + 1
                end = span[1]
                if end < start:
                    end = start
                value = data[key]
                if value in ('True', 'true', True, 'Yes', 'yes', 'on', 'On'):
                    value = 'Yes'
                else:
                    value = 'No'
                insertions.append((start, end, value))
            else:
                raise NotImplementedError(
                    'Not sure how to fill out field type: "{}"'.format(
                        field['type']))
    insertions.sort(key=lambda i: i[0])
    fdf = []
    position = 0
    for start, end, value in insertions:
        fdf.append(fdf_str[position:start])
        fdf.append(value)
        position = end
    fdf.append(fdf_str[position:])
    return ''.join(fdf)

def fill_pdf(pdf, data):
    # write pdf temporarily to disk
    temp_pdf_path = os.path.join(TEMP_FOLDER_PATH, 'tmp-' + pdf.original_pdf_title)
    with open(temp_pdf_path, 'wb') as temp_pdf:
        temp_pdf.write(pdf.original_pdf)
    fdf_str = generate_fdf(temp_pdf_path)
    fdf_str = fill_fdf(fdf_str, pdf.fdf_mapping, data)
    fdf_path = os.path.join(TEMP_FOLDER_PATH, 'tmp-data.fdf')
    with open(fdf_path, 'wb') as fdf_file:
        fdf_file.write(fdf_str.encode(DEFAULT_ENCODING))
    output_path = os.path.join(
        TEMP_FOLDER_PATH, 'filled-' + pdf.original_pdf_title)
    generate_filled_pdf(temp_pdf_path, fdf_path, output_path)
    return output_path


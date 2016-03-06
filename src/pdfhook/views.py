from flask import request, render_template, jsonify, Response, url_for
import io, os
from src.main import db
from src.pdfhook import (
    blueprint,
    tasks,
    queries,
    serializers
)

pdf_dumper = serializers.PDFFormDumper()
pdf_loader = serializers.PDFFormLoader()

@blueprint.route('/', methods=['POST'])
def post_pdf():
    # get pdf
    if not request.files:
        abort(404)
    # what should it do if it receives no files?
    file_storage = request.files['file']
    # here it should pass the
    filename = os.path.basename(file_storage.filename)
    temp_pdf_path = os.path.join(
        tasks.TEMP_FOLDER_PATH, 'tmp-' + filename)
    raw_pdf_data = file_storage.read()
    with open(temp_pdf_path, 'wb') as temp_pdf:
        temp_pdf.write(raw_pdf_data)
    field_definitions = tasks.build_fdf_map(temp_pdf_path)
    pdf, errors = pdf_loader.load(dict(
        original_pdf_title=filename,
        fdf_mapping=field_definitions
        ))
    pdf.original_pdf = raw_pdf_data
    db.session.add(pdf)
    db.session.commit()
    return jsonify(pdf_dumper.dump(pdf).data)


@blueprint.route('/<int:pdf_id>/', methods=['POST'])
def fill_pdf(pdf_id):
    pdf = queries.get_pdf(id=pdf_id)
    data = request.get_json()
    results = tasks.fill_pdf(pdf, data)
    return Response(results)

from flask import (
    request, render_template, jsonify, Response, url_for,
    current_app, send_file)
from sqlalchemy.engine.reflection import Inspector
import io, os, glob
from src.main import db
from src.pdfhook import (
    blueprint,
    queries,
    serializers,
    models
)
from src.pdftk_wrapper import PDFTKWrapper
from src.settings import PROJECT_ROOT

pdf_dumper = serializers.PDFFormDumper()
pdf_loader = serializers.PDFFormLoader()
pdftk = PDFTKWrapper(clean_up=False)

@blueprint.before_app_first_request
def make_sure_there_is_a_working_database(*args, **kwargs):
    if current_app.config.get('ENV') != 'dev':
        return
    inspector = Inspector.from_engine(db.engine)
    tables = inspector.get_table_names()
    required_tables = [models.PDFForm.__tablename__]
    if not (set(required_tables) < set(tables)):
        current_app.logger.warning(
            "database tables {} not found. Creating tables".format(required_tables))
        db.create_all()

@blueprint.after_request
def cleanup_files(response):
    pdftk.clean_up_tmp_files()
    return response

# Index page for uploading pdf
@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@blueprint.route('/', methods=['POST'])
def post_pdf():
    # get pdf
    if not request.files:
        abort(Response("No files found"))
    # what should it do if it receives no files?
    file_storage = request.files['file']
    filename = os.path.basename(file_storage.filename)
    raw_pdf_data = file_storage.read()
    field_map = pdftk.get_field_data(raw_pdf_data)

    pdf, errors = pdf_loader.load(dict(
        original_pdf_title=filename,
        field_map=field_map
        ))
    pdf.original_pdf = raw_pdf_data
    db.session.add(pdf)
    db.session.commit()
    return jsonify(pdf_dumper.dump(pdf).data)


@blueprint.route('/<int:pdf_id>/', methods=['POST'])
def fill_pdf(pdf_id):
    pdf = queries.get_pdf(id=pdf_id)
    data = request.get_json()
    if isinstance(data, list):
        output = pdftk.fill_pdf_many(pdf.original_pdf, data)
    else:
        output = pdftk.fill_pdf(pdf.original_pdf, data)
    filename = pdf.filename_for_submission()
    # I am unsure if this is the correct way to return
    # the filled pdf. `output` is a `bytes` object
    return send_file(
        io.BytesIO(output),
        attachment_filename=filename,
        mimetype='application/pdf')


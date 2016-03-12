from flask import (
    request, render_template, jsonify, Response, url_for,
    current_app, send_file)
from sqlalchemy.engine.reflection import Inspector
import io, os, glob
from src.main import db
from src.pdfhook import (
    blueprint,
    tasks,
    queries,
    serializers,
    models
)
from src.settings import PROJECT_ROOT

pdf_dumper = serializers.PDFFormDumper()
pdf_loader = serializers.PDFFormLoader()

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
    [os.remove(filename) for filename in glob.glob('./data/tmp*')]
    [os.remove(filename) for filename in glob.glob('./data/filled*')]
    return response

# Index page for uploading pdf
@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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
    filename = tasks.fill_pdf(pdf, data)
    return send_file(os.path.join(PROJECT_ROOT, filename), mimetype='application/pdf')

from flask import (
    request, render_template, jsonify, Response, url_for,
    current_app, send_file, redirect)
from sqlalchemy.engine.reflection import Inspector
import io, os, glob, json, datetime
from src.main import db
from src.pdfhook import (
    blueprint,
    serializers,
    models
)
from src.pdftk_wrapper import PDFTKWrapper
from src.settings import PROJECT_ROOT

pdf_dumper = serializers.PDFFormDumper()
pdf_list_dumper = serializers.PDFFormIndexDumper()
pdf_loader = serializers.PDFFormLoader()
pdftk = PDFTKWrapper(clean_up=False)


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


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


@blueprint.route('/', methods=['GET'])
def index():
    pdfs = models.PDFForm.query\
        .order_by(models.PDFForm.latest_post.desc()).all()
    if request_wants_json():
        serialized_pdfs = pdf_list_dumper.dump(pdfs, many=True).data
        return jsonify(dict(pdf_forms=serialized_pdfs))
    return render_template('index.html', pdfs=pdfs)


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
    if request_wants_json():
        return jsonify(pdf_dumper.dump(pdf).data)
    return redirect(url_for('pdfhook.get_pdf', pdf_id=pdf.id))



@blueprint.route('/<int:pdf_id>/', methods=['GET'])
def get_pdf(pdf_id):
    pdf = models.PDFForm.query.filter_by(id=pdf_id).first()
    if not pdf:
        abort(404)
    serialized_pdf = pdf_dumper.dump(pdf).data
    if request_wants_json():
        return jsonify(serialized_pdf)
    return render_template('pdf_detail.html', pdf=serialized_pdf, json=json)


@blueprint.route('/<int:pdf_id>/', methods=['POST'])
def fill_pdf(pdf_id):
    pdf = models.PDFForm.query.filter_by(id=pdf_id).first()
    if not pdf:
        abort(404)
    data = request.get_json()
    if not data and request.form:
        data = {}
        field_map = json.loads(pdf.field_map)
        for fieldname in request.form:
            idx = int(fieldname.replace('field', '')) - 1
            input_value = request.form[fieldname]
            field = field_map[idx]
            data[field['name']] = input_value
    if isinstance(data, list):
        output = pdftk.fill_pdf_many(pdf.original_pdf, data)
    else:
        output = pdftk.fill_pdf(pdf.original_pdf, data)
    pdf.post_count += 1
    pdf.latest_post = datetime.datetime.now()
    db.session.add(pdf)
    db.session.commit()
    filename = pdf.filename_for_submission()
    # I am unsure if this is the best way to return
    # the filled pdf. `output` is a `bytes` object
    return send_file(
        io.BytesIO(output),
        attachment_filename=filename,
        mimetype='application/pdf')


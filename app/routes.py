import io
import zipfile
from flask import request, jsonify
from app import app
from app.deliver import deliver


@app.route('/deliver/dap', methods=['POST'])
def deliver_dap():
    dataset = request.args.get("survey_id")
    process(dataset)


@app.route('/deliver/survey', methods=['POST'])
def deliver_survey():
    process("EDCSurvey")


@app.route('/deliver/feedback', methods=['POST'])
def deliver_feedback():
    process("EDCFeedback")


@app.route('/deliver/comments', methods=['POST'])
def deliver_feedback():
    process("EDCComments")


def process(dataset):
    files = request.files
    file_bytes = files['zip'].read()
    filename = request.args.get("filename")
    description = request.args.get("description")
    iteration = request.args.get("iteration")
    deliver(file_bytes=file_bytes,
            filename=filename,
            dataset=dataset,
            description=description,
            iteration=iteration)


def view_zip():
    files = request.files
    f = files['zip'].read()
    print(type(f))
    file_bytes = io.BytesIO(f)
    print(type(file_bytes))
    z = zipfile.ZipFile(file_bytes)
    print(type(z))

    for filename in z.namelist():
        if filename.endswith('/'):
            continue

        edc_file = z.open(filename)
        print(edc_file.read())

    return jsonify(success=True)

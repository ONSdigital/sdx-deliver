import logging
from flask import request, jsonify
from structlog import wrap_logger

from app import app
from app.deliver import deliver

logger = wrap_logger(logging.getLogger(__name__))


@app.route('/deliver/dap', methods=['POST'])
def deliver_dap():
    dataset = request.args.get("survey_id")
    return process(dataset, "surveys")


@app.route('/deliver/survey', methods=['POST'])
def deliver_survey():
    return process("EDCSurvey", "surveys")


@app.route('/deliver/feedback', methods=['POST'])
def deliver_feedback():
    return process("EDCFeedback", "feedback")


@app.route('/deliver/comments', methods=['POST'])
def deliver_comments():
    return process("EDCComments", "comments")


def process(dataset, directory):
    files = request.files
    file_bytes = files['zip'].read()
    filename = files['zip'].filename
    logger.info(f"filename: {filename}")
    description = request.args.get("description")
    logger.info(f"description: {description}")
    iteration = request.args.get("iteration")
    logger.info(f"iteration: {iteration}")
    deliver(file_bytes=file_bytes,
            filename=filename,
            dataset=dataset,
            description=description,
            iteration=iteration,
            directory=directory)
    return jsonify(success=True)

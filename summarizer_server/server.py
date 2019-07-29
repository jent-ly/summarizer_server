import json
import logging
import os
import sys

from flask import Flask, abort, request
from text_rank import TextRank
from serializers import FeedbackSchema
from feedback_service import FeedbackService, Feedback, database
from settings import Settings


log = logging.getLogger("summarizer_server")

app = Flask(__name__)
app.config.from_object(Settings)
database.init_app(app)

textrank = TextRank()
feedbackservice = FeedbackService()

@app.before_first_request
def before_first_request():
    textrank.setup()


@app.route("/api/")
def index():
    return "Summarizer API"


@app.route("/api/extract", methods=["POST"])
def extract():
    # TODO: call into summary algorithm
    return "Extractive summary endpoint"


@app.route("/api/summarize", methods=["POST"])
def summarize():
    if not request.is_json:
        abort(400)
    request_payload = request.get_json()
    top_sentences = textrank.summarize(
        request_payload["text"], request_payload["percent_sentences"]
    )
    return json.dumps(top_sentences)


@app.route("/api/feedback/submit", methods=["POST"])
def submit_feedback():
    if not request.is_json:
        abort(400)

    request_payload = request.get_json()
    url = request_payload.get("url", "")
    score = request_payload.get("score", "")

    if url == "" or score == "":
        abort(400)

    response = feedbackservice.submit(
        url,
        score,
        request_payload.get("description", ""),
        request_payload.get("email", ""),
        request_payload.get("gaia", ""),
    )
    return json.dumps(response)


# TODO: add feedback deletion
# TODO: make certain routes internal only
@app.route("/api/feedback/view", methods=["GET"])
def view_feedback():
    # TODO: consider pagination
    response = feedbackservice.get_all()
    return json.dumps({"feedback": response})


def configure_logger(debug):
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Configure logger and remove default flask logging
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(log_level)

    app.logger.handlers = []
    app.logger.propagate = True


debug = os.environ.get("DEBUG", "false").lower() == "true"


if __name__ == "__main__":
    configure_logger(debug)
    with app.app_context():
        database.create_all()
    app.run(host="0.0.0.0", debug=False, port=int(os.environ.get("PORT", 5000)))

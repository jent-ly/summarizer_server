import json
import logging
import os
import sys

from flask import Flask, abort, request
from text_rank import TextRank

log = logging.getLogger("summarizer_server")
app = Flask(__name__)
textrank = TextRank()

""" Change this to True to debug. I tried to read from env vars like
`DEBUG=true docker-compose up` but that wasn't working.
"""
debug = False
#  debug = True


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


def configure_logger(debug):
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    # Configure logger and remove default flask logging
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(log_level)

    app.logger.handlers = []
    app.logger.propagate = True


if __name__ == "__main__":
    configure_logger(debug)
    app.run(host="0.0.0.0", debug=debug, port=int(os.environ.get("PORT", 5000)))

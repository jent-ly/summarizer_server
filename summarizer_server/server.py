import json
import os

from flask import Flask, abort, request
from text_rank import TextRank

app = Flask(__name__)
textrank = TextRank()


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=int(os.environ.get("PORT", 5000)))

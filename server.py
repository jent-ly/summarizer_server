import json
import os

from flask import Flask, abort, request
import text_rank

app = Flask(__name__)


@app.before_first_request
def before_first_request():
    text_rank.setup()


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
    return json.dumps(text_rank.summarize(request_payload["text"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

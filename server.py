from flask import Flask
app = Flask(__name__)

@app.route("/api/")
def index():
    return "Summarizer API"

@app.route("/api/extract", methods=["POST"])
def extract():
    # TODO: call into summary algorithm
    return "Extractive summary endpoint"

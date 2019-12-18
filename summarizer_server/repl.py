import json
import readline
import requests
import signal
import sys
import pdb
import text_rank

from nltk import tokenize

from enum import Enum


class OutputType(Enum):
    SUMMARY = 1
    TEXT = 2


class InputType(Enum):
    URL = 1
    TEXT = 2


def sigint_handler(signal, frame):
    exit(0)


DEFAULT_SERVER_LOCATION = "http://localhost:5000"
output_type = OutputType.SUMMARY
input_type = InputType.URL
server_location = DEFAULT_SERVER_LOCATION
signal.signal(signal.SIGINT, sigint_handler)


def print_summary(summary):
    for sentence in summary:
        print(sentence)


def handle_commands(command, response):
    global output_type
    global input_type
    global server_location

    if command == ":exit" or command == ":quit" or command == ":q":
        sys.exit()
    elif command.startswith(":set"):
        tokens = command.split(None, 3)
        set_param = tokens[1]
        if set_param == "output":
            output_type = OutputType[tokens[2].upper()]
        elif set_param == "input":
            input_type = InputType[tokens[2].upper()]
        elif set_param == "server":
            # no argument means go back to localhost
            if len(tokens) == 2:
                server_location = DEFAULT_SERVER_LOCATION
                return
            server_location = tokens[2]
    elif command.startswith(":debug"):
        if not response:
            print("nothing to debug")
        else:
            print("Status code: ", response.status_code)
            print("Response Headers: ", response.headers)
            response.raise_for_status()
    else:
        print(
            """
usage:
    <url>                                Outputs the summary for the article pointed to by the url
    :set <key> <value>                   Changes the configuration of the summarizer:
        output [ summary | text ]         - Sets the output type of the REPL
        server [http[s]://<addr>[:port]]  - Sets the location of the backend
    :debug                               Outputs debug logs for the last sent url
    :[exit | quit | q]                   Exits the REPL
        """
        )


if __name__ == "__main__":
    response = ""
    while True:
        try:
            line = input("jent> ")
        except EOFError:
            exit(0)

        if not line:
            continue

        if line.startswith(":"):
            handle_commands(line, response)
            continue

        if input_type == InputType.URL:
            if not (line.startswith("http://") or line.startswith("https://")):
                line = "http://" + line
            html = requests.get(line).text

            if output_type == OutputType.SUMMARY:
                api_endpoint = f"{server_location}/api/summarize"
                response = requests.post(api_endpoint, json={"html": html})
                print_summary(json.loads(response.content))
            else:
                rank = text_rank.TextRank()
                print(rank.process_html(html).text)
        elif input_type == InputType.TEXT:
            if output_type == OutputType.SUMMARY:
                sentences = tokenize.sent_tokenize(line)
                api_endpoint = f"{server_location}/api/summarize"
                response = requests.post(
                    api_endpoint,
                    json={"title": sentences[0], "text": line, "lang": "en"},
                )
                print_summary(json.loads(response.content))
            else:
                print(line)

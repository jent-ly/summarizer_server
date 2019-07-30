import json
import readline
import requests
import signal
import sys
import text_rank

from enum import Enum


class OutputType(Enum):
    SUMMARY = 1
    TEXT = 2


def sigint_handler(signal, frame):
    exit(0)


output_type = OutputType.SUMMARY
server_location = "http://localhost:5000"
signal.signal(signal.SIGINT, sigint_handler)


def handle_commands(command, response):
    global output_type
    global server_location
    if command == ":exit" or command == ":quit" or command == ":q":
        sys.exit()
    elif command.startswith(":set"):
        tokens = command.split(None, 3)
        set_param = tokens[1]
        if set_param == "output":
            output_type = OutputType[tokens[2].upper()]
        elif set_param == "server":
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
        server http[s]://<addr>[:port]    - Sets the location of the backend
    :debug                               Outputs debug logs for the last sent url
    :[exit | quit | q]                   Exits the REPL
        """
        )


if __name__ == "__main__":
    response = ""
    while True:
        try:
            url = input("url> ")
        except EOFError:
            exit(0)

        if not url:
            continue

        if url.startswith(":"):
            handle_commands(url, response)
            continue

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        html = requests.get(url).text

        if output_type == OutputType.SUMMARY:
            api_endpoint = f"{server_location}/api/summarize"
            response = requests.post(api_endpoint, json={"html": html})
            print(response.content)
        else:
            rank = text_rank.TextRank()
            print(rank.process_html(html))

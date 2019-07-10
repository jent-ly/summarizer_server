import json
import requests
import sys
import readline
import text_rank

from enum import Enum


class OutputType(Enum):
    SUMMARY = 1
    TEXT = 2


output_type = OutputType.SUMMARY


def handle_commands(command, response):
    global output_type
    if command == ":exit" or command == ":quit" or command == ":q":
        sys.exit()
    elif command.startswith(":set"):
        tokens = command.split(None, 3)
        set_param = tokens[1]
        if set_param == "output":
            output_type = OutputType[tokens[2].upper()]
    elif command.startswith(":debug"):
        if not response:
            print("nothing to debug")
        else:
            print("Status code: ", response.status_code)
            print("Response Headers: ", response.headers)
            response.raise_for_status()
    else:
        print("usage: ")
        print(
            "    <url>                                Outputs the summary for the article pointed to by the url"
        )
        print(
            "    :set <key> <value>                   Sets the output type of the REPL. Valid keys are provided below"
        )
        print(
            "        OutputType [summary, text]       Sets the output type of the REPL"
        )
        print(
            "    :debug                               Outputs debug logs for the last sent url"
        )
        print("    :[exit, quit, q]                     Exits the REPL")


if __name__ == "__main__":
    response = ""
    while True:
        url = input("url> ")

        if not url:
            continue

        if url.startswith(":"):
            handle_commands(url, response)
            continue

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        html = requests.get(url).text

        if output_type == OutputType.SUMMARY:
            response = requests.post(
                "http://localhost:5000/api/summarize", json={"html": html}
            )
            print(response.content)
        else:
            rank = text_rank.TextRank()
            print(rank.process_html(html))

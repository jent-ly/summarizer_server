# summarizer-server

[![Build Status](https://travis-ci.com/jent-ly/summarizer_server.svg?branch=master)](https://travis-ci.com/jent-ly/summarizer_server)

## Development setup

Clone the repository:
```shell
[~/workspace] $ git clone summarizer_server
[~/workspace] $ cd summarizer_server
```

Our development environment is hosted in a Docker development container. We support `make` commands, to build the container and its dependencies:
```shell
[~/workspace/summarizer_server] $ make build
```

Run the following command to start the server and attach it to the current terminal. The server by default is hosted on port 5000 with `debug mode: on`
```shell
[~/workspace/summarizer_server] $ make run
```

Use the REPL (Read-Eval-Print-Loop) to interactively send requests to the local and production server. By default the REPL accepts a link to an article and will return the summary of the article produced by the local server. To view a complete set of REPL configurations, type `:help` in the REPL instance.
```shell
[~/workspace/summarizer_server] $ make repl
python3.7 summarizer_server/repl.py
url> :help

usage:
    <url>                                Outputs the summary for the article pointed to by the url
    :set <key> <value>                   Changes the configuration of the summarizer:
        output [ summary | text ]         - Sets the output type of the REPL
        server [http[s]://<addr>[:port]]  - Sets the location of the backend
    :debug                               Outputs debug logs for the last sent url
    :[exit | quit | q]                   Exits the REPL

url> https://www.washingtonpost.com/business/economy/senate-passes-two-year-budget-and-debt-ceiling-bill-sending-to-trump/2019/08/01/5b57dd38-b3de-11e9-8949-5f36ff92706e_story.html?utm_term=.713f63bb3311
But the Treasury Department can only issue debt up to a limit set by Congress, known as the debt ceiling.
[The budget deal is good politics — but terrible policy]Trump had — before coming president — suggested that the debt ceiling shouldn’t be raised.
If the debt ceiling is not lifted, the government could fall behind on some of its payments, which could spark another financial crisis.
“Budget Deal is phenomenal for our Great Military, our Vets, and Jobs, Jobs, Jobs!
The Senate passed a broad, two-year budget deal on Thursday that boosts spending and eliminates the threat of a debt default until after the 2020 election, while reducing the chances for another government shutdown.
(J. Scott Applewhite/AP)The deal passed on Thursday suspends the debt ceiling through July 31, 2021, removing the threat of default and the accompanying risk of political brinkmanship that typically accompanies debt limit negotiations.
url>
```

To open a bash terminal into the docker container:
```shell
[~/workspace/summarizer_server] $ docker exec -it summarizer_server bash
```

Now the API is live at `localhost:5000/api`.

To test a specific endpoint that is not covered by the REPL, consider using `curl`:
```shell
[~/workspace/summarizer_server] $ curl -i -H "Content-Type: application/json" ... http://localhost:5000/api/summarize
```

### Setting up the database

Create a directory for a mounted volume:
```shell
[~/workspace/summarizer_server] $ mkdir postgres_data
```

Set environment variables:
```shell
[~/workspace/summarizer_server] $ POSTGRES_USER=postgres
[~/workspace/summarizer_server] $ POSTGRES_PW=postgres
[~/workspace/summarizer_server] $ POSTGRES_URL=postgres
[~/workspace/summarizer_server] $ POSTGRES_DB=postgres
```

To POST data to the database, consider using `curl`:
```shell
[~/workspace/summarizer_server] $ curl -i --request POST -H "Content-Type: application/json" -d '{"url": "www.fake.com", "score": "1"}' http://localhost:5000/api/feedback/submit
```
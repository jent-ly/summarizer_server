# summarizer-server

[![Build Status](https://travis-ci.com/jent-ly/summarizer_server.svg?branch=master)](https://travis-ci.com/jent-ly/summarizer_server)

## Development setup

Using `docker-compose` (*recommended*):
```shell
[~/summarizer-server] $ docker-compose up -d --build api
```

To use a different port or to run with debug logging:
```shell
[~/summarizer-server] $ PORT=4000 DEBUG=true docker-compose up -d --build api
```

Using `docker`:
```shell
[~/summarizer-server] $ docker build -t summarizer-server ./docker
[~/summarizer-server] $ docker run --rm -p 5000:5000 summarizer-server
```

Note, if a mounted volume is needed then uncomment the commented out portions of the `docker-compose.override.yml` file. *Changes to this file should NOT be pushed, which is why it's in the `.gitignore`.*

To open a bash terminal into the docker container:
```shell
[~/summarizer-server] $ docker exec -it <container_name> bash
```

Now the API is live at `localhost:5000/api`.

To test a specific endpoint, consider using `curl`:
```shell
curl -i -H "Content-Type: application/json" -X POST -d '{"text":"Newspapers are published in many languages. They may be dailies, published every day, or weeklies, published each week. Printed on newsprint, newspapers contain news and views on varied topics. The news published may be on politics, economy, society, business, science, sports and entertainment from around the world. Newspaper publishers hire journalists as reporters and correspondents to write for them. Editors work with a team at newspaper offices to edit stories before they are published in the papers."}' http://localhost:5000/api/summarize
```

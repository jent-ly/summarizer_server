# summarizer-server

## Development setup

Using `docker`:
```shell
[~/summarizer-server] $ docker build -t summarizer-server ./docker/Dockerfile
[~/summarizer-server] $ docker run --rm -p 5000:5000 summarizer-server
```

Using `docker-compose`:
```shell
[~/summarizer-server] $ docker-compose up -d --build api
```

Note, if a mounted volume is needed then uncomment the commented out portions of the `docker-compose.override.yml` file.

To open a bash terminal into the docker container:
```shell
[~/summarizer-server] $ docker exec -it <container_name> bash
```

Now the API is live at `localhost:5000/api`.

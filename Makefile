all: run

build:
	docker-compose -f docker-compose.yml build

run: build
	DEBUG=true docker-compose -f docker-compose.yml up

install:
	pip3.7 install -r requirements.txt

test:
	python3.7 -m unittest discover summarizer_server

repl:
	python3.7 summarizer_server/repl.py

.PHONY: build run install test repl

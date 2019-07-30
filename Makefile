all: run

build:
	docker-compose build

run: build
	docker-compose up

install:
	pip3.7 install -r requirements.txt

test:
	python3.7 -m unittest discover summarizer_server

repl:
	python3.7 summarizer_server/repl.py

.PHONY: build run install test repl

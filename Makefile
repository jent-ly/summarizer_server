all: run

build:
	docker-compose build

run: build
	docker-compose up

install:
	pip3.7 install -r requirements.txt

test:
	python3.7 -m unittest discover summarizer_server

.PHONY: build run install test

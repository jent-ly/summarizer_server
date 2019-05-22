FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip

RUN python3.7 -m pip install pip

COPY ./requirements.txt /server/requirements.txt
WORKDIR /server
RUN python3.7 -m pip install -r requirements.txt

COPY . /server

ENV FLASK_APP=server.py
CMD ["flask", "run", "--host=0.0.0.0"]

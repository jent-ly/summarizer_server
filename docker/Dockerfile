FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip && \
    apt-get update -y && \
    apt-get install -y wget unzip

RUN mkdir /data

RUN wget -P /data http://nlp.stanford.edu/data/glove.6B.zip

RUN unzip /data/glove*.zip -d /data

RUN python3.7 -m pip install pip

COPY ./requirements.txt /server/requirements.txt
WORKDIR /server
RUN python3.7 -m pip install -r requirements.txt
# TODO: find out pip install isn't installing all of the modules
# RUN pip3 install -r requirements.txt

COPY . /server

ENV FLASK_APP=server.py
CMD ["flask", "run", "--host=0.0.0.0"]

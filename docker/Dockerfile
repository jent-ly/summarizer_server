FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common wget unzip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip

RUN mkdir /data

RUN wget -P /data http://nlp.stanford.edu/data/glove.6B.zip -q

RUN unzip /data/glove*.zip -d /data

RUN python3.7 -m pip install pip

COPY ./requirements.txt /server/requirements.txt
WORKDIR /server
RUN python3.7 -m pip install -r requirements.txt

COPY . /server

RUN python3.7 -c "import text_rank; text_rank.process_word_embeddings()"

ENV FLASK_APP=server.py
CMD ["flask", "run", "--host=0.0.0.0"]

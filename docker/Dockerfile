FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common wget unzip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip

RUN mkdir /data

RUN wget -P /data http://nlp.stanford.edu/data/glove.6B.zip -q

RUN unzip /data/glove*.zip -d /data && \
    rm /data/glove.6B.200d.txt /data/glove.6B.100d.txt /data/glove.6B.50d.txt \
    /data/glove.6B.zip

RUN python3.7 -m pip install pip

WORKDIR /server

# Python package dependencies
COPY ./requirements.txt /server/requirements.txt
RUN python3.7 -m pip install -r requirements.txt

# Set up local data
COPY ./image_setup.py /server/image_setup.py
RUN python3.7 -c "import image_setup; image_setup.setup_local_data()"

COPY . /server

# ENV FLASK_APP=server.py
CMD ["python3.7", "server.py"]

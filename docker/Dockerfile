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

RUN mkdir summarizer_server

# Set up local data
# The symlink has to be made because for some reason when the container is run
# in google cloud run, nltk checks for data at /home/nltk_data. When the
# container is run locally, it checks /root/nltk_data.
COPY ./summarizer_server/image_setup.py /server/summarizer_server/image_setup.py
RUN python3.7 -c "import summarizer_server.image_setup; summarizer_server.image_setup.setup_local_data()" && \
    ln -s /root/nltk_data /home/nltk_data

COPY . /server

CMD ["python3.7", "summarizer_server/server.py"]


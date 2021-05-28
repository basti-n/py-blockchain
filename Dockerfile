FROM python:3.9.4

ADD . /blockchain-py

WORKDIR /blockchain-py

RUN pip3 install -r requirements.txt
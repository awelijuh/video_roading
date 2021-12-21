FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get update ##[edited]

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
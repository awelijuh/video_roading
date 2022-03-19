FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get update

RUN apt install -y libx264-dev

RUN apt install ffmpeg libsm6 libxext6  -y

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# TODO костыль для youtube
RUN pip install -e git+https://github.com/mohamed-challal/pafy.git@develop#egg=pafy

COPY . /code/
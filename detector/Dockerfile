FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get update ##[edited]

RUN apt install -y libx264-dev

RUN apt install ffmpeg libsm6 libxext6  -y

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install torch==1.10.2+cpu torchvision==0.11.3+cpu torchaudio==0.10.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

RUN pip install -r requirements.txt

COPY . /code/



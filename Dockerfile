FROM python:3

COPY . /app

WORKDIR /app

RUN apt update && apt install -y ffmpeg git build-essential libffi-dev openssl libssl-dev && pip install --upgrade -r requirements.txt

CMD python -u main.py

FROM python:3

COPY . /app

WORKDIR /app

RUN pip install --upgrade -r requirements.txt
RUN apt -y update && \
    apt -y upgrade && \
    apt install -y ffmpeg

CMD python main.py
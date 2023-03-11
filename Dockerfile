FROM python:3.8

LABEL maintainer="Anthony Barente <anthony.barente@gmail.com>"
LABEL version="0.0.1"

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./deeppep deeppep
COPY ./server_config.py server_config.py
COPY ./DeepPepServer DeepPepServer

CMD ["./DeepPepServer"]

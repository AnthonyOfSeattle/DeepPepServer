FROM python:3.8

LABEL maintainer="Anthony Valente <valenta4@uw.edu>"
LABEL version="0.0.1"

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./deeppep deeppep
COPY ./server_config.py server_config.py
COPY ./DeepPepServer DeepPepServer

CMD ["/DeepPepServer"]

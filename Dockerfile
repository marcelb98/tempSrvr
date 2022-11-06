FROM debian:stable-slim

MAINTAINER Marcel Beyer "marcel.beyer@it-maker.eu"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install waitress==2.1.2

COPY . /app

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]


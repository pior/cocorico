FROM resin/raspberry-pi-python:3.6-slim

RUN apt-get update && apt-get install -yq \
    zlib1g-dev libjpeg-dev libfreetype6-dev libasound2-dev alsa-utils portaudio19-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cache some python packages build
RUN pip --disable-pip-version-check --no-cache-dir install Pillow RPi.GPIO

COPY ./requirements.txt ./requirements-target.txt /tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt -r /tmp/requirements-target.txt

COPY . ./

ENV INITSYSTEM on

CMD ["python", "-m", "cocorico"]

FROM resin/raspberry-pi-python:3.6-slim

# RUN apt-get update && apt-get install -yq \
#    alsa-utils libasound2-dev && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt ./requirements-target.txt /tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt -r /tmp/requirements-target.txt

COPY . ./

ENV INITSYSTEM on

CMD ["python", "-m", "cocorico"]

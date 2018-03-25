FROM resin/raspberry-pi-python:3.6-slim

RUN apt-get update && apt-get install -yq \
    zlib1g-dev libjpeg-dev libfreetype6-dev libasound2-dev alsa-utils portaudio19-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./Pipfile* ./requirements-target.txt ./
RUN pip --disable-pip-version-check --no-cache-dir install pipenv -r requirements-target.txt \
    pipenv install --system --deploy

COPY . ./

ENV INITSYSTEM on

CMD ["python", "-m", "cocorico"]

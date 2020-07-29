FROM balenalib/raspberrypi4-64-debian-python:3.7

WORKDIR /usr/src/app

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq --no-install-recommends \
	cron \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

#setup cronjob
RUN touch /usr/src/app/output-daily.log
RUN echo "0 3 * * * /usr/src/app/app.py >> output-daily.log 2>&1" | crontab


CMD ./app.py > output-daily.log 2>&1 && tail -f /usr/src/app/output-daily.log
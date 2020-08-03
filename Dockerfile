FROM balenalib/raspberrypi4-64-debian-python:3.7

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ./app.py > output-daily.log 2>&1
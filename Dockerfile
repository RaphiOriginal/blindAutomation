FROM balenalib/raspberrypi4-64-debian-python:3.7

RUN apt-get update && apt-get install build-essential

WORKDIR /usr/src/app

COPY blind_automation ./blind_automation
COPY data ./data
COPY requirements.txt .
RUN /usr/local/bin/python3.7 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ./blind_automation/app/app.py
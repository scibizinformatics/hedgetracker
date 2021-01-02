FROM nikolaik/python-nodejs:python3.7-nodejs15-slim

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

RUN cd /app/main/anyhedge && npm install

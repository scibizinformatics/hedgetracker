FROM nikolaik/python-nodejs:python3.7-nodejs15-slim

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

RUN cd /app/main/anyhedge && npm install

RUN wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/8ed92e8cab83cfed76ff012ed4a36cef74b28096/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

ENTRYPOINT [ "wait-for-it.sh", "postgres:5432", "--", "sh", "entrypoint.sh" ]
CMD [ "python", "manage.py", "runtracker" ]

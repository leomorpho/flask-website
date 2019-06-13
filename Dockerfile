FROM python:3.6-alpine

RUN adduser -D flask-website

WORKDIR /home/flask-website

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY myapp myapp
COPY migrations migrations
COPY main.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R flask-website:flask-website ./
# USER command makes a user the default for any subsequent 
# commands, even for the container in production.
USER flask-website

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]


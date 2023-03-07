FROM python:latest

RUN useradd trusted_middleware

WORKDIR /home/trusted_middleware

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY trusted_middleware.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP trusted_middleware.py

RUN chown -R trusted_middleware:trusted_middleware ./
USER trusted_middleware

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
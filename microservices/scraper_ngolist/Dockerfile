FROM python:3-alpine
WORKDIR /usr/src
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
CMD ["gunicorn", "run:app"]

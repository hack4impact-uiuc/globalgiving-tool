FROM python:3-alpine
WORKDIR /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
CMD ["gunicorn", "run:app", "--timeout", "5000000000000", "--log-level=DEBUG"]

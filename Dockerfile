FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

EXPOSE 80

CMD ["flask", "run"]
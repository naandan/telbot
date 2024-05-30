FROM python:3.10-buster

RUN apt-get update && apt-get update -y

RUN mkdir -p /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
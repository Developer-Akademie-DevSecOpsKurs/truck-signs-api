FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install netcat-openbsd -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app/src

EXPOSE 8020

ENTRYPOINT ["/app/entrypoint.sh"]

RUN chmod +x /app/entrypoint.sh
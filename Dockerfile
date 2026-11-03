FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh \
    && useradd --create-home appuser \
    && mkdir -p /app/src/staticfiles /app/src/mediafiles \
    && chown -R appuser:appuser /app

USER appuser

WORKDIR /app/src

EXPOSE 8020

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "tsa_app.wsgi:application", "--bind", "0.0.0.0:8020", "--workers", "4"]
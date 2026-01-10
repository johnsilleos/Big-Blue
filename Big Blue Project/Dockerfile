FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_pipeline.py .
COPY crontab /etc/cron.d/weather-cron

RUN chmod 0644 /etc/cron.d/weather-cron && crontab /etc/cron.d/weather-cron
RUN touch /var/log/weather.log

CMD ["cron", "-f"]

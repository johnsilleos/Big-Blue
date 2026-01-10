### GitHub Project 2 Dockerized Weather API on PosgreSQL

How to Run the Project
Prerequisites

Docker

Docker Compose

1) Start the pipeline

From the project root:

docker compose up -d --build


This command:

Builds the Python ingestion service

Starts PostgreSQL

Enables hourly execution via cron

2) Verify running containers
docker ps


You should see:

weather-pipeline-weather_app-1

weather-pipeline-postgres-1

3) Check pipeline logs
docker logs weather-pipeline-weather_app-1


You should see:

Pipeline run completed

4) Query the database

Connect to PostgreSQL:

docker exec -it weather-pipeline-postgres-1 psql -U weather_user -d weather_db


Example query:

SELECT *
FROM weather_readings
ORDER BY timestamp_utc DESC
LIMIT 5;


Exit PostgreSQL:

\q

5) Scheduling

The pipeline runs every hour using cron inside the Docker container:

0 * * * * python /app/weather_pipeline.py
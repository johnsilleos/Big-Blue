## GitHub Repository
Author: Giannis Syllaios

### Introduction
This my public repository that contains my Data Engineering Bootcamp Projects.

### Technologies Used
- **Python**: For scripting and running data analysis tasks.
- **Jupyter Notebooks**: For interactive data analysis and visualization.
- **Pandas**: For data manipulation and analysis.
- **SQL**: For data acquisition.

### Acknowledgements
I would like to thank the instructors for their support and guidance throughout the bootcamp.

### Disclaimer
This is a public repository as part of the learning process of Git tool at Big Blue Academy.

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
import requests
import pandas as pd
import psycopg2
from datetime import datetime, timezone

DB_CONFIG = {
    "host": "postgres",
    "dbname": "weather_db",
    "user": "weather_user",
    "password": "weather_pass",
    "port": 5432
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
            id SERIAL PRIMARY KEY,
            city_en TEXT,
            city_gr TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            timestamp_utc TIMESTAMPTZ,
            temperature_c DOUBLE PRECISION,
            wind_speed_kmh DOUBLE PRECISION,
            weather_description TEXT,
            carbon_monoxide DOUBLE PRECISION,
            dust DOUBLE PRECISION
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_weather(lat, lon):
    return requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "UTC"}
    ).json()

def fetch_air_quality(lat, lon):
    return requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={"latitude": lat, "longitude": lon, "hourly": "carbon_monoxide,dust", "timezone": "UTC"}
    ).json()

def get_latest_hour_index(times):
    times = pd.to_datetime(times, utc=True)
    now = pd.Timestamp.now(tz="UTC")
    valid = times[times <= now]
    return times.get_loc(valid[-1]) if len(valid) else -1

def insert_records(records):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for r in records:
        cur.execute("""
            INSERT INTO weather_readings (
                city_en, city_gr, latitude, longitude, timestamp_utc,
                temperature_c, wind_speed_kmh, weather_description,
                carbon_monoxide, dust
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            r["city_en"], r["city_gr"], r["latitude"], r["longitude"],
            r["timestamp_utc"], r["temperature_c"], r["wind_speed_kmh"],
            r["weather_description"], r["carbon_monoxide"], r["dust"]
        ))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    cities = [
        ("Athens", "Αθήνα", 37.9838, 23.7275),
        ("Thessaloniki", "Θεσσαλονίκη", 40.6401, 22.9444),
        ("Patras", "Πάτρα", 38.2466, 21.7346),
        ("Heraklion", "Ηράκλειο", 35.3387, 25.1442),
        ("Larissa", "Λάρισα", 39.6390, 22.4179)
    ]

    init_db()
    records = []

    for city_en, city_gr, lat, lon in cities:
        w = fetch_weather(lat, lon)
        aq = fetch_air_quality(lat, lon)
        idx = get_latest_hour_index(aq["hourly"]["time"])

        records.append({
            "city_en": city_en,
            "city_gr": city_gr,
            "latitude": lat,
            "longitude": lon,
            "timestamp_utc": datetime.now(timezone.utc),
            "temperature_c": w["current_weather"]["temperature"],
            "wind_speed_kmh": w["current_weather"]["windspeed"],
            "weather_description": str(w["current_weather"]["weathercode"]),
            "carbon_monoxide": aq["hourly"]["carbon_monoxide"][idx],
            "dust": aq["hourly"]["dust"][idx]
        })

    insert_records(records)
    print("Pipeline run completed")

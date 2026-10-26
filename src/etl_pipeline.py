import time
import uuid
import random
from datetime import datetime, timedelta
import polars as pl
from sqlalchemy import create_engine, text
from prefect import task, flow

DB_URL = "postgresql+psycopg2://admin:password123@db:5432/thermal_db"
engine = create_engine(DB_URL)

@task(retries=3, retry_delay_seconds=5)
def extract_telemetry():
    batch_id = str(uuid.uuid4())
    start_temp = 1200.0
    readings = []
    base_time = datetime.now()
    
    for minute in range(5):
        temp = start_temp - (minute * random.uniform(40.0, 60.0))
        readings.append({
            "batch_id": batch_id,
            "sensor_zone": minute + 1,
            "temp_celsius": temp,
            "reading_time": base_time + timedelta(minutes=minute)
        })
    return batch_id, readings

@task
def transform_data(readings):
    df = pl.DataFrame(readings)
    max_temp = df["temp_celsius"].max()
    min_temp = df["temp_celsius"].min()
    return (max_temp - min_temp) / 5.0

@task
def load_data(batch_id, readings, cooling_rate):
    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO batches (batch_id, material, target_cooling_rate) VALUES (:b, :m, :t)"
        ), {"b": batch_id, "m": "Carbon-Steel-1045", "t": 50.0})
        
        for row in readings:
            conn.execute(text(
                "INSERT INTO thermal_readings (batch_id, sensor_zone, temp_celsius, reading_time) VALUES (:b, :s, :t, :r)"
            ), {"b": row["batch_id"], "s": row["sensor_zone"], "t": row["temp_celsius"], "r": row["reading_time"]})
        
        if cooling_rate > 55.0:
            conn.execute(text(
                "INSERT INTO quality_flags (batch_id, deviation_type) VALUES (:b, :d)"
            ), {"b": batch_id, "d": "Cooled too fast"})
        conn.commit()

@flow(name="Thermal Monitoring Pipeline")
def factory_simulation_flow():
    # Wait for the database to boot on the very first run
    time.sleep(5) 
    batch_id, readings = extract_telemetry()
    cooling_rate = transform_data(readings)
    load_data(batch_id, readings, cooling_rate)

if __name__ == "__main__":
    # The serve method locks the script open and runs it exactly every 3600 seconds (1 hour)
    # We will set it to 60 seconds right now just so you can watch it trigger multiple times quickly.
    factory_simulation_flow.serve(name="hourly-batch-monitor", interval=60)
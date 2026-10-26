**Thermal Monitoring ETL Pipeline: Industrial IoT Automation**
This repository contains a fully containerized Data Engineering pipeline designed to simulate, process, and store thermal sensor telemetry from a manufacturing environment. The project models a factory quality control system where metal parts are monitored for cooling gradients to prevent metallurgical brittleness.
**Project Architecture**
The infrastructure is built on a multi container Docker Compose network, isolating the database layer from the execution environment.
 * Data Generation (Extract): A Python worker simulates IoT sensors capturing time series temperature data across 5 cooling zones for uniquely identified production batches.
 * Processing (Transform): Polars processes the raw arrays in memory calculating the overall cooling rate (°C/min) to determine material compliance.
 * Storage (Load): SQLAlchemy and psycopg2 manage connections to a PostgreSQL 15 database loading data into a relational schema while automatically flagging batches that exceed the safe cooling threshold (55 °C/min).
 * Orchestration: Prefect transforms the script into a resilient scheduled workflow, automatically triggering the ETL process on a predefined interval without manual intervention.
Technology Stack
 * Language: Python 3.11
 * Data Processing: Polars
 * Database: PostgreSQL 15, SQL
 * Orchestration: Prefect
 * Infrastructure: Docker, Docker Compose
Database Schema
The PostgreSQL database is initialized with three relational tables:
 * batches: Master record of production runs, material type (e.g., Carbon-Steel-1045), and target cooling rates.
 * thermal_readings: High-volume time-series log storing granular sensor data linked to each batch via foreign keys.
 * quality_flags: Automated defect tracking table that logs deviations when cooling rates exceed critical thresholds.
Local Deployment Setup
1. Clone the repository
git clone https://github.com/singhrishika0630/thermal-etl-pipeline.git
cd thermal-etl-pipeline

2. Launch the infrastructure
Ensure Docker Desktop is running on your machine, then build and start the containers:
docker compose up --build

3. Monitor the Orchestration
Once booted, Prefect will automatically initialize the scheduling server. The terminal will output live logs as the pipeline extracts, transforms, and loads the simulated factory data at the specified intervals.
4. Query the Database
To verify the loaded data, open a new terminal instance and bridge into the database container:
docker exec -it thermal_postgres psql -U admin -d thermal_db

Execute standard SQL commands to explore the telemetry:
SELECT * FROM quality_flags;

5. Teardown
To cleanly shut down the virtual network and stop all background processes:
docker compose down
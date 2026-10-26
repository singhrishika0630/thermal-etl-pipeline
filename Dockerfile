# Use a lightweight, official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install the libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The Python code will be injected via the volume we set in docker-compose.yml,
# but we tell the container to run our ETL script as its main command.
CMD ["python", "src/etl_pipeline.py"]
-- Table to track each manufacturing batch of metal parts
CREATE TABLE batches (
    batch_id UUID PRIMARY KEY,
    material VARCHAR(50),
    target_cooling_rate FLOAT
);

-- Table to store the raw temperature readings from the sensors
CREATE TABLE thermal_readings (
    reading_id SERIAL PRIMARY KEY,
    batch_id UUID REFERENCES batches(batch_id),
    sensor_zone INTEGER,
    temp_celsius FLOAT,
    reading_time TIMESTAMP
);

-- Table to flag any batches that cooled too fast or too slow
CREATE TABLE quality_flags (
    flag_id SERIAL PRIMARY KEY,
    batch_id UUID REFERENCES batches(batch_id),
    deviation_type VARCHAR(100)
);
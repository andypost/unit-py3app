# Flask vs FastAPI Performance Benchmark

A tool for comparing CPU and RAM consumption between Flask (WSGI) and FastAPI (ASGI) frameworks in a controlled Docker environment.

## Overview

This project contains two identical API services implemented with Flask and FastAPI that provide performance metrics and resource usage statistics. Both services run side-by-side in a single Docker container using NGINX Unit as the application server, allowing for direct comparison under identical conditions.

## Project Structure

- `flask-wsgi.py` - Flask API implementation (WSGI)
- `fastapi-asgi.py` - FastAPI implementation (ASGI)
- `start.sh` - Docker container launch script
- `up.sh` - Container initialization script
- `conf.json` - NGINX Unit configuration (not included in repo)

## API Endpoints

Both APIs provide identical endpoints:

- `/` - Simple greeting endpoint
- `/status` - Current resource usage metrics (system and process)
- `/stats` - Resource usage statistics for the last 10 minutes (60 samples at 10-second intervals)

## Metrics Collected

### System Metrics:
- CPU usage percentage
- Memory usage percentage
- Used memory (MB)
- Available memory (MB)

### Process Metrics:
- Process CPU usage percentage
- RSS memory usage (MB)
- VMS memory usage (MB)

## Running the Benchmark

1. Ensure Docker is installed
2. Create a `conf.json` file with NGINX Unit configuration
3. Run the benchmark:

```bash
chmod +x start.sh
./start.sh
```

After startup:
- Flask API available on port 8080
- FastAPI API available on port 8081

## Comparing Results

To compare performance:

1. Query both APIs and compare metrics:
```bash
curl http://localhost:8080/stats
curl http://localhost:8081/stats
```

2. Run load testing with tools like Apache Bench or wrk:
```bash
ab -n 10000 -c 100 http://localhost:8080/
ab -n 10000 -c 100 http://localhost:8081/
```

3. Compare statistics after load testing:
```bash
curl http://localhost:8080/stats
curl http://localhost:8081/stats
```

## Interpreting Results

When comparing metrics, note:
- CPU consumption difference between Flask and FastAPI
- Memory usage difference (RSS and VMS)
- Minimum, maximum, and average values under load

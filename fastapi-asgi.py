from fastapi import FastAPI
from collections import OrderedDict
import psutil
import os
import time
from collections import deque
import statistics

app = FastAPI()

# Get the current process
process = psutil.Process(os.getpid())

# Store historical metrics (last 10 minutes, one sample every 10 seconds = 60 samples)
MAX_SAMPLES = 60
metrics_history = deque(maxlen=MAX_SAMPLES)
last_sample_time = 0
SAMPLE_INTERVAL = 10  # seconds

def collect_metrics():
    """Collect system and process metrics."""
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    # Process metrics
    process_memory = process.memory_info()
    process_cpu = process.cpu_percent(interval=0.1)
    
    metrics = {
        "process": {
            "cpu_percent": process_cpu,
            "memory_rss_mb": round(process_memory.rss / (1024 * 1024), 2),
            "memory_vms_mb": round(process_memory.vms / (1024 * 1024), 2)
        },
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used_mb": round(memory.used / (1024 * 1024), 2),
            "memory_available_mb": round(memory.available / (1024 * 1024), 2)
        },
        "timestamp": time.time()
    }
    
    return metrics

def update_metrics_history():
    """Update metrics history if enough time has passed since last sample."""
    global last_sample_time
    current_time = time.time()
    
    if current_time - last_sample_time >= SAMPLE_INTERVAL:
        metrics = collect_metrics()
        metrics_history.append(metrics)
        last_sample_time = current_time
        return True
    
    return False

def calculate_stats(values):
    """Calculate statistics for a list of values."""
    if not values:
        return {"current": None, "min": None, "max": None, "avg": None}
    
    return {
        "current": values[-1],
        "min": min(values),
        "max": max(values),
        "avg": round(statistics.mean(values), 2)
    }

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/status")
async def status():
    """Get current metrics."""
    # Always collect current metrics
    current_metrics = collect_metrics()
    
    # Try to update history
    update_metrics_history()
    
    return current_metrics

@app.get("/stats")
async def stats():
    """Get statistical information from metrics history."""
    # Try to update metrics history
    update_metrics_history()
    
    # If no history available, return current metrics
    if not metrics_history:
        return jsonify({"stats": "No historical data available yet", "current": collect_metrics()})
    
    # Extract data for statistical analysis
    system_cpu = [m["system"]["cpu_percent"] for m in metrics_history]
    system_memory = [m["system"]["memory_percent"] for m in metrics_history]
    process_cpu = [m["process"]["cpu_percent"] for m in metrics_history]
    process_memory = [m["process"]["memory_rss_mb"] for m in metrics_history]
    
    return {
        "process": {
            "cpu_percent": calculate_stats(process_cpu),
            "memory_rss_mb": calculate_stats(process_memory)
        },
        "samples": len(metrics_history),
        "system": {
            "cpu_percent": calculate_stats(system_cpu),
            "memory_percent": calculate_stats(system_memory)
        },
        "time_span_seconds": round(metrics_history[-1]["timestamp"] - metrics_history[0]["timestamp"], 2) if len(metrics_history) > 1 else 0
    }

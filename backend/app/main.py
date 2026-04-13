from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram
import time

app = FastAPI()

requests_counter = Counter("requests_total", "Total de Requests", ["method", "endpoint"])
request_latency = Histogram("request_duration_seconds", "HTTP request latency",["method", "endpoint"] )

@app.middleware("http")
async def count_request(request: Request, call_next):
    response = await call_next(request)

    requests_counter.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    return response

async def measure_time(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    request_latency.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response


@app.get("/")
async def root():
    for metric in requests_counter.collect():
        for sample in metric.samples:
            return (sample)
  
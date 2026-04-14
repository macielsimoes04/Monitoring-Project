from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram
import time

app = FastAPI()

requests_counter = Counter("requests_total", "Total de Requests", ["method", "endpoint"])
request_latency = Histogram("request_duration_seconds", "HTTP request latency",["method", "endpoint"] )


def measure_time(method_request:str, endpoint_request:str): 

    start = time.time()

    duration = time.time() - start

    request_latency.labels(
        method=method_request,
        endpoint=endpoint_request
    ).observe(duration)

@app.middleware("http")
async def count_request(request: Request, call_next):
    response = await call_next(request)

    requests_counter.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    measure_time(request.method, request.url.path)

    return response


@app.get("/")
async def root():
    for metric in requests_counter.collect():
        for sample in metric.samples:
            return (sample)1
  
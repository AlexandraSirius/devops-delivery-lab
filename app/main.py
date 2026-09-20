import os
from time import perf_counter

from fastapi import FastAPI, Request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from starlette.responses import Response


app = FastAPI(title="DevOps Delivery Lab")


HTTP_REQUESTS_TOTAL = Counter(
    "devops_lab_http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "devops_lab_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    started_at = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - started_at

    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    ).inc()

    HTTP_REQUEST_DURATION_SECONDS.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration)

    return response


@app.get("/")
def root():
    return {
        "service": "devops-lab",
        "version": os.getenv("APP_VERSION", "dev"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

# DevOps Delivery Lab

A small FastAPI service used to practice a complete DevOps delivery workflow.

## Implemented

- FastAPI application with health endpoint
- Pytest automated tests
- Docker image with a non-root user and health check
- GitHub Actions CI pipeline
- Automated test execution and Docker image build

## Run tests

```bash
python -m pytest -v
```

## Build and run with Docker

```bash
docker build -t devops-lab:1.0 .
docker run --rm -p 8000:8000 -e APP_VERSION=1.0 devops-lab:1.0
```

Endpoints:

- `GET /`
- `GET /health`

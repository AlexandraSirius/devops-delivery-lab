import os

from fastapi import FastAPI

app = FastAPI(title="DevOps Lab")


@app.get("/")
def root():
    return {
        "service": "devops-lab",
        "version": os.getenv("APP_VERSION", "dev")
    }


@app.get("/health")
def health():
    return {"status": "ok"}

FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid 10001 appgroup \
    && adduser --uid 10001 --ingroup appgroup --disabled-password --gecos "" --no-create-home appuser

COPY --chown=10001:10001 app ./app

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

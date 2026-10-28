# Multi-stage build: dependencies are installed in a builder stage and only the
# virtual environment and the code reach the final image.
FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
LABEL org.opencontainers.image.source="https://github.com/luizgustavocs/grc-privacy-portfolio"
LABEL org.opencontainers.image.description="VitaClin appointments API (fictitious), DevSecOps lab"
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=builder /venv /venv
COPY main.py .
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD ["/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"]
CMD ["/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

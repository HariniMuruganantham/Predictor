FROM python:3.11-slim

WORKDIR /app

# Install curl so the HEALTHCHECK below can actually run.
# python:3.11-slim does NOT ship curl by default — this is a common
# gotcha the guide's original healthcheck line glossed over.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CACHEBUST forces Docker to re-run COPY . . on every build, even if
# requirements.txt hasn't changed. Without this, an unchanged
# requirements.txt means Docker reuses the cached COPY layer from a
# previous build — your new code never actually makes it into the image.
ARG CACHEBUST=1
RUN echo "Cache bust: $CACHEBUST"

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]

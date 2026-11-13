# ==============================================================================
# Multi-Stage Dockerfile for Campus Lab Resources Management API
# Stage 1: Build stage (Installs dependencies and prepares virtual environment)
# Stage 2: Slim runtime stage (Only packages app code and dependencies, no build tools)
# ==============================================================================

# -------- STAGE 1: Builder --------
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and create an isolated virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# -------- STAGE 2: Slim Runtime --------
FROM python:3.12-slim AS runtime

# Set metadata and environment flags
LABEL maintainer="Campus Lab DevOps Team" \
      version="1.0.0" \
      description="Campus Lab Resources Management REST Microservice"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_PORT=5000 \
    APP_ENV=production

WORKDIR /app

# Create a non-root system user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY src/ /app/src/

# Set file permissions for the non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose internal port
EXPOSE 5000

# Docker native health check
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; sys_exit = 0 if urllib.request.urlopen('http://localhost:5000/health').getcode() == 200 else 1; exit(sys_exit)" || exit 1

# Launch microservice
CMD ["python", "src/app.py"]

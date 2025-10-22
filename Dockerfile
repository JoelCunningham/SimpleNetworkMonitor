# Stage 1: build dependencies
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip wheel --wheel-dir=/wheels -r requirements.txt

# Stage 2: final image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy wheels and install
COPY --from=builder /wheels /wheels
# Ensure requirements.txt is present in the final image (copied from build context)
COPY requirements.txt ./
# Install all requirements from the pre-built wheels. Avoid installing extras
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Install runtime system dependencies required by scanning utilities (e.g. ping)
RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy app
COPY . /app

# Expose port for FastAPI
EXPOSE 8000

# Default command to run the app using uvicorn
CMD ["uvicorn", "app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

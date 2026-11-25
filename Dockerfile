# Stage 1: Build Python dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install tools required to compile mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Production runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install MySQL runtime library and apply available security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    libmariadb3 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

RUN groupadd --system appuser && \
    useradd --system --gid appuser --uid 10001 --create-home appuser

COPY --chown=appuser:appuser . .

RUN mkdir -p /app/app/static/uploads/profiles && \
    chown -R appuser:appuser /app/app/static/uploads

EXPOSE 5000

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]

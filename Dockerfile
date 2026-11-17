FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_DIR=/dados

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create an unprivileged user
RUN groupadd --system --gid 10001 appuser \
    && useradd --system \
       --uid 10001 \
       --gid 10001 \
       --home-dir /app \
       --no-create-home \
       --shell /usr/sbin/nologin \
       appuser

# Copy application files
COPY --chown=10001:10001 app/ .

# Prepare the data directory
RUN mkdir -p /dados \
    && chown 10001:10001 /dados

# Run the application as non-root
USER 10001:10001

CMD ["python", "coletor.py"]

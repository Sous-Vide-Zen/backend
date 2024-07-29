# Build stage step
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

COPY . .

COPY start.sh /app/start.sh

ARG SOUS_VID_ENV
WORKDIR /config
RUN touch .env && \
    echo "SOUS_VID_ENV" >> .env

RUN chmod +x /app/start.sh

# Production stage
FROM python:3.11-alpine

WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY --from=builder /app /app
COPY --from=builder /config/.env /config/.env

# Set PYTHONPATH explicitly
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "/app/start.sh"]

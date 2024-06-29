# Use a lightweight Python image
FROM python:3.11-alpine

# Setting workdir to /app
WORKDIR /app

# Copying requirements to use them
COPY src/requirements.txt .

# Upgrading pip and installing requirements
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copying the project folder to the image
COPY . .

# Explicitly copying start.sh to the working directory
COPY start.sh /app/start.sh

# Setting the environment variable
ENV PYTHONPATH=/app:$PYTHONPATH

# Making start.sh executable
RUN chmod +x /app/start.sh

# Exposing port 8000 for dev mode
EXPOSE 8000

# Container starting parameters
CMD ["sh", "/app/start.sh"]


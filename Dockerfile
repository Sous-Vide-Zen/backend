# adding python3 slim, lesser image size
FROM python:3.11-slim

# setting workdir to /app
WORKDIR /app

# copying requirements to use them with venv
COPY src/requirements.txt .

# creating, activating, updating venv and installing requirements
RUN python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt
# copying the project folder to the image
COPY . .

# changing dir to copy env examples
WORKDIR /app/config
RUN touch .env
RUN cat .env.example > .env

#going back
WORKDIR /app

# exposing port 8000 for dev mode
EXPOSE 8000

# running migrations
RUN /app/venv/bin/python3 manage.py migrate

# comment out for now, getting errors
# RUN /app/venv/bin/python3 manage.py loaddata src/fixtures/*

# container starting parameters
ENTRYPOINT ["/app/venv/bin/python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]


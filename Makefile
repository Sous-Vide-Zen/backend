                                      DC = docker compose
EXEC = docker exec -it
MANAGE_PY = python manage.py

APP_CONTAINER = svz-django
KEYCLOAK_CONTAINER = svz-db

APP_SERVICE = django
KEYCLOAK_SERVICE = keycloak

DOCKER_COMPOSE_FILE = docker-compose.yaml

.PHONY: start
start: stop build
	$(DC) -f $(DOCKER_COMPOSE_FILE) up

.PHONY: stop
stop:
	$(DC) -f $(DOCKER_COMPOSE_FILE) down

.PHONY: build
build:
	$(DC) -f $(DOCKER_COMPOSE_FILE) build

.PHONY: migrate
migrate:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: create-superuser
create-superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: loaddata-linux
loaddata-linux:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} loaddata $(ls -d -1 "$PWD/"src/fixtures/**)
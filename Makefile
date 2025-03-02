EXEC = docker exec -it
MANAGE_PY = python manage.py

APP_DEV_NAME = svz-backend:dev
APP_NAME_PROD = vbamnup/svz-backend:v0.1amd64
APP_DEV_CONTAINER_NAME = svz-backend-dev
APP_CONTAINER_NAME = svz-backend
APP_SERVICE = django

DOCKER_COMPOSE_FILE = docker-compose.yml

# Собираем образ для разработки
.PHONY: dev-build
dev-build:
	cp .docker/.dockerignore.dev .dockerignore
	docker build -t $(APP_DEV_NAME) -f .docker/Dockerfile.dev .

# Запускаем контейнер для разработки и применяем миграции
.PHONY: dev-run
dev-run:
	docker run -d --name $(APP_DEV_CONTAINER_NAME) -p 8000:8000 $(APP_DEV_NAME)
	$(EXEC) $(APP_DEV_CONTAINER_NAME) $(MANAGE_PY) makemigrations
	$(EXEC) $(APP_DEV_CONTAINER_NAME) $(MANAGE_PY) migrate

# Останавливаем контейнер для разработки
.PHONY: dev-stop
dev-stop:
	docker stop $(APP_DEV_CONTAINER_NAME)
	docker rm $(APP_DEV_CONTAINER_NAME)

# Собираем образ для продакшена
.PHONY: build
build:
	cp .docker/.dockerignore.prod .dockerignore
	docker buildx build -t $(APP_NAME_PROD) -f .docker/Dockerfile.prod --platform linux/amd64 --load .

# Пушим образ в репозиторий
.PHONY: push
push:
	docker push $(APP_NAME_PROD)


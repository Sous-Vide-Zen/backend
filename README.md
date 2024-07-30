# Sous-Vide Zen Backend

[![linter](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml/badge.svg)](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml) [![PyTest](https://github.com/Sous-Vide-Zen/backend/actions/workflows/pytest.yml/badge.svg)](https://github.com/Sous-Vide-Zen/backend/actions/workflows/pytest.yml)

Sous-Vide Zen is a website for sharing and discovering recipes for sous-vide cooking, a technique that involves cooking food in vacuum-sealed bags at precise temperatures. Users can create their own recipes, browse popular and featured recipes, follow other users, react and comment on recipes, and save their favorites.

### Features

- Registration and authorization on the site
- Share recipes
- Popular recipes feed
- Subscription feed
- Share recipes
- Comment recipes
- Reactions to recipes and comments
- Favorite recipes
- Hash tags
- Search recipe database

### Technologies

- Python 3.11
- Django 4.2.6
- Django REST Framework 3.14.0
- PostgreSQL
- Djoser
- Black

### How to start a project:

Clone the repository and navigate to it on the command line:

```shell
git clone git@github.com:Sous-Vide-Zen/backend.git
```

Activate the virtual environment and install dependencies

```shell
python3.11 -m venv venv
. venv/bin/activate
pip install -r src/requirements.txt
```

Navigate to the config directory

```shell
cd config/
```

Create an .env file

```shell
touch .env
```

`Copy all from env.example to .env file`

Return to main directory

```shell
cd ..
```

Launch a project

```shell
python manage.py migrate
python manage.py runserver
```

Fill the database

```shell
python manage.py loaddata src/fixtures/*
```

### Documentation url

```djangourlpath
http://127.0.0.1:8000/api/v1/swagger/
```

### Oauth endpoints:

```text
Эндпоинты регистрации через соц.сети
http://127.0.0.1:8000/api/v1/login/yandex-oauth2/ - регистрация через яндекс
http://127.0.0.1:8000/api/v1/login/vk-oauth2 - регистрация через вк

Настройка редиректа, на проде нужно поменять 127.0.0.1:8000 на домен
http://127.0.0.1:8000/api/v1/complete/yandex-oauth2/
http://127.0.0.1:8000/api/v1/complete/vk-oauth2/ - настраивается в vk.com/dev
```

Для локального запуска нашего Sous Vide Backend в Docker необходимо сделать следующее:

### **1. Установить Docker**

Если докер еще не установлен, его необходимо установить. Следуйте инструкциям для вашей ОС:

- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

После установки убедитесь что Docker запущен и работает.

### **2. Авторизация в DockerHUB**

Так как наш image приватный, необходимо залогиниться в DockerHUB. Запустите терминал ивыполняйте команды:

```bash
docker login [registry-1.docker.io] -u sousvidzen
```

Пароль: Спрашиваем у Леры и Андрея

### **3. Pull Docker Image**

Для того чтобы запустить image необходимо его скачать

```bash
docker pull sousvidzen/backend:dev
```

### **4. Запустить Docker Container**

После загрузки image необходимо его запустить

```bash
docker run -d --name sous-vid-zen-backend -p 8000:8000 sousvidzen/backend:dev
```

- `d`: Запускает контейнер в фоновом режиме.
- `-name sous-vid-zen-backend`: Задает имя контейнера чтобы для понимания.
- `p 8000:8000`: Делает контейнер доступным на 8000 порту.

### **5. Убеждаемся что контейнер запустился и работает**

Для проверки:

```bash
docker ps
```

Вы должны увидеть что `sous-vid-zen-backend` есть в списке, со статусом "Up."

### **6. Остановка и удаление контейнера**

Когда закончили тестировать или хотите спулить новую версию

```bash
docker stop sous-vid-zen-backend
docker rm sous-vid-zen-backend
```

### **8. Полезные команды**

- **Логи**: Чтобы посмотреть логи нашего контейнера
    
    ```bash
    docker logs sous-vid-zen-backend
    ```
    
- **Interactive Shell Access**: Для попадания в шелл самого контейнера
    
    ```bash
    docker exec -it sous-vid-zen-backend /bin/sh
    ```
    
    Полезно для дебага приложения
# Sous-Vide Zen Backend

[![linter](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml/badge.svg)](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml)

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

```dotenv
DEBUG=TRUE
SECRET_KEY=django-insecure-_$i&ghy42$5ki+155q9$dpz6e410wec7adv*c3u0@6tjn7&yv+

SOCIAL_AUTH_VK_OAUTH2_KEY=51788997
SOCIAL_AUTH_VK_OAUTH2_SECRET=03jnhOQgeNVfU0HMdr2Y
SOCIAL_AUTH_YANDEX_OAUTH2_KEY=b57308fc10884dc5ab8e5f39d728c99d
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET=60921ea4d2e94741888d5a9ba4009811
```

Return to main directory

```shell
cd ..
```

Launch a project
```shell
python manage.py migrate
python manage.py runserver
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

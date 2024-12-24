# Sous-Vide Zen Backend

[![linter](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml/badge.svg)](https://github.com/Sous-Vide-Zen/backend/actions/workflows/linter.yml) [![PyTest](https://github.com/Sous-Vide-Zen/backend/actions/workflows/pytest.yml/badge.svg)](https://github.com/Sous-Vide-Zen/backend/actions/workflows/pytest.yml)

Sous-Vide Zen is a website for sharing and discovering recipes for sous-vide cooking, a technique that involves cooking
food in vacuum-sealed bags at precise temperatures. Users can create their own recipes, browse popular and featured
recipes, follow other users, react and comment on recipes, and save their favorites.

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

Clone the repository:

```shell
git clone git@github.com:Sous-Vide-Zen/backend.git
```

Navigate to the project directory:

```shell
cd backend
```

<h3>By Docker:</h3>

<ol>
<li>If you don’t have Docker installed, please <a href="https://docs.docker.com/engine/install/">install it</a>.</li>
<li>Then execute it

```shell
docker build -t svz-back .
```
</li>

<li>After it was built execute it

```shell
docker run -p 8000:8000 svz-back
```
</li>
</ol>

<h3>By Docker Compose</h3>
<ol>
<li>
Use need to install Docker and Makefile(if use windows) 
<a href="https://ftp.gnu.org/gnu/make/">Install page for Makefile</a>
and 
<a href="https://medium.com/@samsorrahman/how-to-run-a-makefile-in-windows-b4d115d7c516">Example Tutorial</a>
</li>
<li>Create env files and, if necessary, fill it with your variables.

```shell
cp config/.env.example  config/.env
cp config/keycloak.env.example config/keycloak.env
```
</li>
<li>Then execute command

```shell
make start
```
</li>
<li>Connecting keycloak<br>
    - Open page <a href="http://localhost:8080">keycloak localhost</a> and pass login: admin, password: admin<br>
    - Create new client, set access urls mask to 'http://localhost:8000/*'<br>
    - Add client secret key to config/.env<br>
    - Allow registration in realms settings
</li>
<li>Auth with keycloak<br>
    - Restart docker compose with command

```shell
make start
```
<br>
    - Open page <a href="http://localhost:8000/api/v1/oids/authenticate/">Auth page</a> and create a new user or log in by admin<br>
</li>
</ol>


<h3>By venv:</h3>
Create and activate the virtual environment, install dependencies:

- Windows

```shell
python -m venv venv
. venv/Scripts/activate
pip install -r src/requirements.txt
```

- Linux and macOS

```shell
python3.11 -m venv venv
. venv/bin/activate
pip install -r src/requirements.txt
```

Navigate to the config directory

```shell
cd config/
```

Create an env file and, if necessary, fill it with your variables or use default values.

```shell
cp .env.example .env
```

Return to the project directory:

```shell
cd ..
```

Launch a project:

```shell
python manage.py migrate
python manage.py runserver
```

Fill the database:

```shell
python manage.py loaddata $(ls src/fixtures/)
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

# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в контейнер
COPY .. /app

# Устанавливаем переменную окружения для управления Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Открываем порт, если требуется доступ извне
EXPOSE 8000

# Указываем команду для запуска сервера разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

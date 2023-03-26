# foodgram

### Описание

Проект Foodgram - это сервис с созданием и просмотром рецептов.

### Технологии

Python 3.7
Django 2.2.19

### Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndrewYatskevich/foodgram-project-react.git
```

- Перейти в нужную дерикторию и создать файл окружения:

```
cd infra/
touch .env
```

- Прописать в файле окружения необходимые переменные:

SECRET_KEY
ALLOWED_HOSTS
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT

- Запустить файл docker-compose.yaml:

```
docker-compose up -d
```

- Провести миграции, создать суперюзера, собрать статику:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

![foodgram_workflow](https://github.com/AndrewYatskevich/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Автор: Андрей Яцкевич https://github.com/AndrewYatskevich
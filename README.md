# Бронирование отелей
![](https://img.shields.io/badge/Python-0.104.0-blue?logo=python) 
![](https://img.shields.io/badge/FastAPI-0.104.0-orange?logo=fastapi)
![](https://img.shields.io/badge/SQLAlchemy-2.0.21-a0c500?logo=SQLAlchemy)
![](https://img.shields.io/badge/Redis-7.2-red?logo=Redis)
![](https://img.shields.io/badge/Gunicorn-20.1.0-blue?logo=gunicorn)
![](https://img.shields.io/badge/-Nginx-464646??style=flat-square&amp;logo=NGINX)
![](https://img.shields.io/badge/-Docker-464646??style=flat-square&amp;logo=docker)

## Приложение "Бронирование"
Приложение API помогает пользователям забронировать номер в отеле на желаймую дату. Пользователи могут проверять свои бронирования, выбрать желаемый отель и тип комнаты. После бронирования отправляется сообщение на почту с информацией о бронировании. Реализовано администрирование и модерирование. Используеться Docker comnpose, позволяющий развернуть приложение на сервере с контейнерами базы данных PostgreSQL, in-memory базой данных Redis, очередью задач на Celery + Flower. 

## Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:

```
uvicorn application.main:app --reload
```  

Так же может быть использована библиотека gunicorn. Команда для запуска:

```
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
```

## Файл конфигурации
Для запуска контейнеров необходим файл **.env** в папке с проектом.
Содержание файла:

```
POSTGRES_PASSWORD = {{Postgres password}}
POSTGRES_USER = {{Postgres user}}
POSTGRES_PORT = {{Postgres port}}
DB_HOST = {{Database host}}
DB_NAME = {{Database name}}
SECRET_KEY = {{FastAPI secret key}}
SECRET_ALGORITHM = {{FastAPI secret key}}(HS256:default)
REDIS_PASSWORD = {{Redis password}}
REDIS_PORT = {{Redis password}}
REDIS_DATABASES = {{Redis databases amount}}
REDIS_HOST = {{Redis host}}
SMTP_HOST = {{smtp URL}}
SMTP_USER = {{smtp login}}
SMTP_PORT = {{smtp port}}
SMTP_PASS = {{smtp password}}
TEST_MODE = {{Test mode}}(True)/(False:default)
```

Дополнительные параметры для подключения тестовой базы данных (TEST_MODE = True):

```
TEST_POSTGRES_PASSWORD = {{Postgres password}}
TEST_POSTGRES_USER = {{Postgres user}}
TEST_POSTGRES_PORT = {{Postgres port}}
TEST_DB_HOST = {{Database host}}
TEST_DB_NAME = {{Database name}}
```
## Celery & Flower
Для запуска Celery используется команда  

```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```

Обратите внимание, что `-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.  
Для запуска Flower используется команда

```
celery --app=app.tasks.celery:celery flower
``` 

## Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:

```
docker build .
```  
Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

## Docker compose
Для запуска всех сервисов (Postgresql, Redis, веб-сервер (FastAPI), Celery, Flower) необходимо использовать файл docker-compose.yml и команды

```
docker compose up -d
```

После создания и запуска образа выполнить команду

```
docker compose exec backend alembic upgrade head
```

## Docs
Документация хранится по адресу: [http://localhost:8000/api/docs].
В случае запуска на сервер замените localhost на адрес своего сервера

## Управление базой данных

Администрирование базы данных по адресу: [http://localhost:8000/api/admin].

## Flower

Администрирование базы данных по адресу: [http://localhost:8000/flower].


## Об авторах
Александр Зубарев
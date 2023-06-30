# album_factory
## Описание
В проекте настроен docker-compose, что упрощает начало работы
## Запуск
1. Установить:
* <a href=https://www.docker.com/get-started>Docker</a>
* <a href=https://docs.docker.com/compose/install/>Docker-compose</a>  
2. Создать и заполнить ".env"
<br><pre>cp .env.dist .env</pre><br>
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=album_factory
POSTGRES_USER=album_factory
POSTGRES_PASSWORD=album_factory
DB_HOST=db # имя контейнера базы данных
DB_PORT=5432
SECRET_KEY= # секретный ключ Django
RABBITMQ_DEFAULT_USER=album_factory
RABBITMQ_DEFAULT_PASS=album_factory
```
3. Собрать контейнеры. Запуск из папки docker.  
<br><pre>docker-compose up --build</pre><br>
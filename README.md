# web_development_project

## Quick start
The easiest way to start the Django server is through [docker-compose.yml](docker-compose.yml) or [docker-compose.postgre.yml](docker-compose.postgre.yml). Before running Django with the following commands, make sure that [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed on your machine:

```bash
docker-compose up
```

After running, you can access the Django app in your browser at [http://localhost:8000](http://localhost:8000) 


The default database is sqlite3, if you need postgresql, you can start the service with the following command

```bash
docker-compose -f docker-compose.postgre.yml -p web_development_prject_postgre  up
```
### environment variable

The default superuser settings are as follows, which you can change in [docker-compose.yml](docker-compose.yml) or [docker-compose.postgre.yml](docker-compose.postgre.yml)

```yml
DJANGO_SUPERUSER_USERNAME: admin
DJANGO_SUPERUSER_PASSWORD: adminpassword
DJANGO_SUPERUSER_EMAIL: admin@example.com
```

The docker-compose method of startup creates docker volumes by default to store database data, if you need to use an existing database, here are some examples.
### sqlite
```yml
services:
  django:
    build: .
    environment:
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: adminpassword
      DJANGO_SUPERUSER_EMAIL: admin@example.com
      DATABASE_URL: sqlite:////app/storage/db.sqlite3
    volumes:
      - ./project/manage.py:/app/manage.py
      - ./project/mysite:/app/mysite
      - ./project/myapp:/app/myapp
      # here
      - path/to/your/db.sqlite3:/app/storage/db.sqlite3
    ports:
      - "8000:8000"
    command: python manage.py runserver 0.0.0.0:8000
#volumes:
#  db_data:
```
### postgresql

```yml
services:
  django:
    build:
      context: .
      dockerfile: Dockerfile.postgre
    environment:
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: adminpassword
      DJANGO_SUPERUSER_EMAIL: admin@example.com
      # here
      DATABASE_URL: YOUR_POSTGRESQLURL
    volumes:
      - ./project/manage.py:/app/manage.py
      - ./project/mysite:/app/mysite
      - ./project/myapp:/app/myapp
    ports:
      - "8000:8000"
    # depends_on:
    #   - postgres
    command: python manage.py runserver 0.0.0.0:8000
#   postgres:
#     image: postgres:latest
#     environment:
#       POSTGRES_USER: admin
#       POSTGRES_PASSWORD: adminpassword
#       POSTGRES_DB: mydatabase
#     volumes:
#       - posgre_data:/var/lib/postgresql/data
#     ports:
#       - "5432:5432"
# volumes:
#   posgre_data:
```

# important
If you are using a customized postgresql, you need to modify [docker_entrypoint_postgre.sh](project/docker_entrypoint_postgre.sh)
```sh
while ! nc -z postgres 5432; do
  sleep 1
done
```
Change the address and port where nc checks for postgre connectivity to the address and port of your postgre database, for example.
This code is because docker-compose sometimes depends_on doesn't work and starts django before postgresql is fully started causing an exception solution, there is no better solution at this time.
```sh
while ! nc -z 127.0.0.1 5432; do
  sleep 1
done
```

---

### You can also start the service via docker run 

### for sqlite3
#### first build docker image
```bash
docker build -t web_development_project:1.0 .
```

```bash
docker run -p 8000:8000 \
-v ./project/storage:/app/storage \
-v ./project/myapp:/app/myapp \
-v ./project/mysite:/app/mysite \
-v ./project/manage.py:/app/manage.py \
-e DJANGO_SUPERUSER_USERNAME=admin \
-e DJANGO_SUPERUSER_PASSWORD=admin \
-e DATABASE_URL=sqlite:////app/storage/db.sqlite3 \
-e DJANGO_SUPERUSER_EMAIL=admin@example.com \
web_development_project:1.0
```

use docker volume

```bash
docker volume create db_data
```
```bash
docker run -p 8000:8000 \
-v db_data:/app/storage \
-v ./project/myapp:/app/myapp \
-v ./project/mysite:/app/mysite \
-v ./project/manage.py:/app/manage.py \
-e DJANGO_SUPERUSER_USERNAME=admin \
-e DJANGO_SUPERUSER_PASSWORD=admin \
-e DATABASE_URL=sqlite:////app/storage/db.sqlite3 \
-e DJANGO_SUPERUSER_EMAIL=admin@example.com  \
web_development_project:1.0
```

### for postgre
#### first build docker image
```bash
docker build -f docker-compose.postgre.yml -t web_development_project_postgre:1.0 .
```

```bash
docker run -p 8000:8000 \
-v ./project/myapp:/app/myapp \
-v ./project/mysite:/app/mysite \
-v ./project/manage.py:/app/manage.py \
-e DJANGO_SUPERUSER_USERNAME=admin \
-e DJANGO_SUPERUSER_PASSWORD=admin \
-e DATABASE_URL=postgres://admin:adminpassword@localhost:5432/mydatabase \
-e DJANGO_SUPERUSER_EMAIL=admin@example.com \
web_development_project_postgre:1.0
```


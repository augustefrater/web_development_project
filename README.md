# web_development_project


How to run this project with docker compose(sqlit3):
```bash
docker-compose up
```

How to run this project with docker compose(postgresql):
```bash
docker-compose -f docker-compose.postgre.yml -p web_development_prject_postgre  up
```

How to run this project with docker run (with your local sqlite3 file):
```bash
# build docker image
docker build -t web_development_project:1.0 .
# docker run
docker run -p 8000:8000 -v ./project/storage:/app/storage -v ./project/myapp:/app/myapp -v ./project/mysite:/app/mysite -v ./project/manage.py:/app/manage.py -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=admin -e DATABASE_URL=sqlite:////app/storage/db.sqlite3 -e DJANGO_SUPERUSER_EMAIL=admin@example.com  web_development_project:1.0
```

How to run this project with docker run (with docker volume)(sqlite3):

```bash
# build docker image
docker build -t web_development_project:1.0 .
# create docker volume
docker volume create db_data
# docker run
docker run -p 8000:8000 -v db_data:/app/storage -v ./project/myapp:/app/myapp -v ./project/mysite:/app/mysite -v ./project/manage.py:/app/manage.py -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=admin -e DATABASE_URL=sqlite:////app/storage/db.sqlite3 -e DJANGO_SUPERUSER_EMAIL=admin@example.com  web_development_project:1.0
```

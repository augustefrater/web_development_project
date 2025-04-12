FROM python:3.13.3-alpine

WORKDIR /app

COPY /project/manage.py .

# install app dependencies
COPY /project/requirements.txt .
RUN pip install -r requirements.txt

# setup entrypoint
COPY /project/docker_entrypoint.sh .
RUN chmod +x docker_entrypoint.sh

ENTRYPOINT ["/app/docker_entrypoint.sh"]

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Inside project/Dockerfile
FROM python:3.13.3-alpine

WORKDIR /app

# Create necessary folders
RUN mkdir -p /app/storage

# Env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Copy requirements from local dir
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the current project files (this works because we are inside /project)
COPY . /app/

# Setup env variables for Django superuser
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DATABASE_URL=sqlite:////app/storage/db.sqlite3

# Make sure entrypoint is executable
RUN chmod +x /app/docker_entrypoint.sh

ENTRYPOINT ["/app/docker_entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

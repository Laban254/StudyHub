FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 80 (HTTP)
EXPOSE 80

# Run migrations and add crontab jobs
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python3 manage.py crontab add

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "studyHub.wsgi:application"]

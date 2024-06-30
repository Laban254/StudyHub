#!/bin/bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Apply migrations
python3 manage.py makemigrations
python3 manage.py makemigrations studyApp
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --no-input

python3 manage.py crontab add



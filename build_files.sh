#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run collectstatic from the Django project directory
cd core
python manage.py collectstatic --noinput

#!/bin/bash

echo "Waiting for PostgreSQL to become ready..."
sleep 10

echo "Apply database migrations"
python src/manage.py makemigrations
python src/manage.py migrate
echo "Apply database migrations end"

echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000

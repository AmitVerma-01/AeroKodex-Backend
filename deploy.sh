#!/bin/bash
set -e

echo "Starting deployment process..."

# Pull latest changes (assuming git)
# git pull origin main

echo "Building Docker image..."
docker build -t aerokodex-backend .

echo "Applying database migrations..."
docker run --rm --env-file .env.production aerokodex-backend python manage.py migrate

echo "Collecting static files..."
docker run --rm --env-file .env.production -v $(pwd)/staticfiles:/app/staticfiles aerokodex-backend python manage.py collectstatic --noinput

echo "Restarting services..."
# If using a compose stack:
# docker compose -f docker-compose.prod.yml up -d

echo "Deployment complete!"

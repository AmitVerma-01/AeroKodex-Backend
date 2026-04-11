# AeroKodex Backend

This is the Django REST Framework backend for the AeroKodex platform. 
It uses PostgreSQL for the database and provides API endpoints for the frontend.

## Prerequisites

- **Python**: 3.11+
- **Docker & Docker Compose**: For running the PostgreSQL database.
- **Heroku CLI**: For deployment (`brew tap heroku/brew && brew install heroku`).

## Setup Instructions

### 1. Database Setup (Docker)

The project uses a PostgreSQL database. The easiest way to run it locally is using the `docker-compose.yml` file located in the root of the monorepo.

Navigate to the project root and start the database:
```bash
cd ..
docker-compose up -d db
```

*Note: This will spin up a Postgres 16 container with the credentials specified in the compose file.*

### 2. Environment Variables

Navigate to the `backend` directory and create your `.env` file based on the provided example:

```bash
cd backend
cp .env.example .env
```

Ensure the database settings in `.env` match the ones in `docker-compose.yml` (they are pre-configured to match by default).

### 3. Virtual Environment & Dependencies

Create and activate a Python virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Database Migrations

Apply the database migrations to set up your local PostgreSQL database schemas:

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)

To access the Django Admin panel and other administrative endpoints, create a superuser account:

```bash
python manage.py createsuperuser
```
Follow the prompts to set your details and password.

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

**API Documentation:**
You can typically browse the interactive API documentation (provided by drf-spectacular) at:
- Swagger UI: `http://127.0.0.1:8000/api/docs/` or `http://127.0.0.1:8000/api/schema/swagger-ui/`

## Running with Docker (Production Mode)

The production `Dockerfile` uses a multi-stage build, runs as a non-root user, and serves Django with `gunicorn`.

```bash
# Build the image
docker build -t aerokodex-backend:prod .

# Run in production mode
docker run -d \
	--name aerokodex-backend \
	--env-file .env \
	-e DJANGO_DEBUG=False \
	-e DJANGO_ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1 \
	-e GUNICORN_WORKERS=3 \
	-e GUNICORN_THREADS=2 \
	-e GUNICORN_TIMEOUT=60 \
	-p 8000:8000 \
	aerokodex-backend:prod
```

The container startup command automatically runs migrations and `collectstatic`, then starts Gunicorn.

## Deploy to Heroku

### 1. Login and create Heroku app

```bash
heroku login
heroku create <your-app-name>
```

### 2. Provision PostgreSQL

```bash
heroku addons:create heroku-postgresql:essential-0 -a <your-app-name>
```

This automatically sets `DATABASE_URL` in Heroku config vars.

### 3. Set required config vars

```bash
heroku config:set \
	DJANGO_SECRET_KEY="replace-with-a-secure-random-secret" \
	DJANGO_DEBUG=False \
	DJANGO_ALLOWED_HOSTS="<your-app-name>.herokuapp.com" \
	DJANGO_CSRF_TRUSTED_ORIGINS="https://<your-app-name>.herokuapp.com" \
	CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com" \
	DJANGO_SECURE_SSL_REDIRECT=True \
	-a <your-app-name>
```

### 4. Deploy

```bash
git add .
git commit -m "Prepare Heroku deployment"
git push heroku main
```

### 5. Verify release and open app

```bash
heroku logs --tail -a <your-app-name>
heroku open -a <your-app-name>
```

### 6. Optional admin user

```bash
heroku run python manage.py createsuperuser -a <your-app-name>
```

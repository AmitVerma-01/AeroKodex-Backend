# AeroKodex Backend

This is the Django REST Framework backend for the AeroKodex platform. 
It uses PostgreSQL for the database and provides API endpoints for the frontend.

## Prerequisites

- **Python**: 3.11+
- **Docker & Docker Compose**: For running the PostgreSQL database.

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

## Running with Docker (Production/Staging)

A `Dockerfile` is provided for building the backend image for deployment. It uses `gunicorn` to serve the app.

```bash
# Build the image
docker build -t aerokodex-backend .

# Run the container (Make sure .env contains the correct DB_HOST for Docker networking)
docker run --env-file .env -p 8000:8000 aerokodex-backend
```

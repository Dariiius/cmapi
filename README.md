# Candidate Management API

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, containerized using **Docker**. This API manages candidates and their job applications.

## Tech Stack

- **FastAPI** – High-performance Python web framework
- **SQLAlchemy (Async)** – Database ORM
- **PostgreSQL** – Relational database
- **Alembic** – DB migrations
- **Docker & Docker Compose** – Containerization
- **Pytest** – Unit testing

---

## Features

- Candidate creation and listing
- Application submission per candidate
- Update application status
- Database migrations via Alembic
- Fully async implementation with `asyncpg`
- Token-based authentication (JWT-ready)
- API docs (Swagger UI / Redoc) at `/docs` and `/redoc`

---

## Setup & Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/candidate-management-api.git
cd candidate-management-api
```

### 2. Create venv and activate

```bash
# Windows
python -m venv ./venv
.\venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```


### 4. Create .env and .env.local Files

```bash
# .env
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=desired_host
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_TEST_DB=test_database_name
DATABASE_URL=postgresql+asyncpg://<your_postgres_user>:<your_postgres_password>@<desired_host>:5423/<database_name>
DATABASE_URL_SYNCH=postgresql+psycopg2://<your_postgres_user>:<your_postgres_password>@<desired_host>:53432/<database_name>

SECRET_KEY=secret_key
ALGORITHM=HS256
EXPIRATION=30
```

```bash
# .env.local
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_TEST_DB=test_database_name
DATABASE_URL=postgresql+asyncpg://<your_postgres_user>:<your_postgres_password>@host.docker.internal:5432/<database_name>
DATABASE_URL_SYNCH=postgresql+psycopg2://<your_postgres_user>:<your_postgres_password>@host.docker.internal:5432/<database_name>


SECRET_KEY=secret_key
ALGORITHM=HS256
EXPIRATION=30
```

To generate **SECRET_KEY**, run this in bash

```bash
openssl rand -base64 64
```

### 5. Build and Run with Docker

```cmd
docker-compose up --build
```
Once running, access the API documentation:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc


To use the API with a local postgresql database, run the following command:

```cmd
docker build -t <IMAGE_NAME>:<TAG> .
docker run -p <PORT>:<PORT> --env-file .env.local --add-host=host.docker.internal:host-gateway <IMAGE_NAME>:<TAG>
```

**Notes**: 
-  Make sure the database is initialized and running and environment variables are properly configured for your setup. 
-  Create your own admin in the database with these data:
    - email: admin@example.com
    - password: $2b$12$hF0X9Spqf5NKRUKeJBlEE.0wbqYL5EShCDzNp2W1RDzP/kmTD0dmi

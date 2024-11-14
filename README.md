# Irrigation System

### Tech stack:

#### Backend:

- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Docker and Docker Compose**

#### Before using this project, make sure you have the following components installed

- Docker
- Docker Compose
- GNU Make

### Conf .env file

```env
JWT_SECRET=your_secret_key
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_DB=IrrigationSystemDB
```

### For run

- `make all`: Start the project.
- `make migrations`: Make migrations.
- `make migrate`: Apply migrations.
- `make app-logs`: Follow the logs in api container.

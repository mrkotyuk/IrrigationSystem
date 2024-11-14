# Irrigation System

### Tech stack:

#### Backend:

- **FastAPI**
- **SQLAlchemy**
- **Alembic**

### Conf .env file

```env
JWT_SECRET=your_secret_key
URL_DB=your_postgres_url
```

### For run:

```sh
$ python -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ alembic revision --autogenerate -m "initial migration"
$ alembic upgrade head
$ uvicorn main:app --host 0.0.0.0 --port 8000
```

# Irrigation System

### Tech stack:

- **FastAPI**
- **SQLAlchemy**

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
$ uvicorn main:app --reload
```

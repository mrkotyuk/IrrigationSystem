import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET")
URL_DB = os.environ.get("URL_DB")
